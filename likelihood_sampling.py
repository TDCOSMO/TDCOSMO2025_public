import os
os.environ["HDF5_USE_FILE_LOCKING"] = "FALSE"
import emcee
import numpy as np
import pickle
import copy
import pandas as pd
import pickle
import time 
from mpi4py import MPI
import yaml
import argparse
import sys

from pylab import rc
rc('axes', linewidth=2)
rc('xtick',labelsize=15)
rc('ytick',labelsize=15)

# set relative paths to working directory and data
dir_path = '/cluster/home/mmillon/modules/7LensMilestone/Likelihoods/MilestoneLikelihood/'

dir_path_tdcosmo = os.path.join(dir_path, 'TDCOSMO_sample')
dir_path_slacs = os.path.join(dir_path, 'ExternalLenses/SLACS')
dir_path_sl2s = os.path.join(dir_path, 'ExternalLenses/SL2S')

# if using Planck posterior for joint inference, add the path to the Planck chain. The Planck chain can be downloaded from http://esdcdoi.esac.esa.int/doi/html/data/astronomy/planck/Cosmology.html
dir_path_Planck_chain = "/cluster/work/refregier/mmillon/Planck_chain/COM_CosmoParams_fullGrid_R3.01" 

from hierarc.Sampling.mcmc_sampling import MCMCSampler
from hierarc.Diagnostics.blinding import blind_posterior
from hierarc.Diagnostics.goodness_of_fit import GoodnessOfFit

# this cell contains top level setting for the sampling. It is tagged "parameters" for the access from papermill (https://github.com/nteract/papermill) 
comm = MPI.COMM_WORLD
rank = comm.Get_rank()

parser = argparse.ArgumentParser(description="Parse a YAML config file.")
parser.add_argument("-f", "--file", type=str, required=True, help="Path to the YAML config file.")
args = parser.parse_args()

with open(args.file, "r") as file:
    config = yaml.safe_load(file)

# Extract values
anisotropy = config.get("anisotropy")
anisotropy_parameterization = config.get("anisotropy_parameterization")
kin_axi_correction = config.get("kin_axi_correction")
run_chain = config.get("run_chain")
n_run_emcee = config.get("n_run_emcee")
n_burn_emcee = config.get("n_burn_emcee")
continue_from_backend = config.get("continue_from_backend")
run_name = config.get("run_name")
output_dir = config.get("output_dir")
sampling_index = config.get("sampling_index")
lambda_mst_sampling = config.get("lambda_mst_sampling", True)
alpha_lambda_sampling = config.get("alpha_lambda_sampling", True)
anisotropy_sampling = config.get("anisotropy_sampling", True)
individual_lens = config.get("individual_lens", None)
boost_vel_disp_error = config.get("boost_vel_disp_error", None)
fixed_Om = config.get("fixed_Om", False)

if rank == 0:
    # Print the parsed values
    print(f"anisotropy = {anisotropy}")
    print(f"anisotropy_parameterization = {anisotropy_parameterization}")
    print(f"kin_axi_correction = {kin_axi_correction}")
    print(f"run_chain = {run_chain}")
    print(f"n_run_emcee = {n_run_emcee}")
    print(f"n_burn_emcee = {n_burn_emcee}")
    print(f"continue_from_backend = {continue_from_backend}")
    print(f"run_name = {run_name}")
    print(f"output_dir = {output_dir}")
    print(f"sampling_index = {sampling_index}")
    print(f"lambda_mst_sampling = {lambda_mst_sampling}")
    print(f"alpha_lambda_sampling = {alpha_lambda_sampling}")
    print(f"anisotropy_sampling = {anisotropy_sampling}")
    print(f"individual_lens = {individual_lens}")
    print(f"boost_vel_disp_error = {boost_vel_disp_error}")
    print(f"fixed_Om = {fixed_Om}")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

sampling_list = [# lensing-only constraints on FLCDM
                {'cosmology': 'FLCDM', 'with_tdcosmo': True, 'with_slacs_kcwi': False, 'with_sl2s': False, 'with_pantheon': False, 'with_planck': False}, #0
                {'cosmology': 'FLCDM', 'with_tdcosmo': True, 'with_slacs_kcwi': True, 'with_sl2s': False, 'with_pantheon': False, 'with_planck': False}, #1
                {'cosmology': 'FLCDM', 'with_tdcosmo': True, 'with_slacs_kcwi': False, 'with_sl2s': True, 'with_pantheon': False, 'with_planck': False}, #2
                {'cosmology': 'FLCDM', 'with_tdcosmo': True, 'with_slacs_kcwi': True, 'with_sl2s': True, 'with_pantheon': False, 'with_planck': False}, #3
                # lensing+pantheon in FLCDM
                {'cosmology': 'FLCDM', 'with_tdcosmo': True, 'with_slacs_kcwi': False, 'with_sl2s': False, 'with_pantheon': True, 'with_planck': False, 'with_DESSNIa': False}, #4
                {'cosmology': 'FLCDM', 'with_tdcosmo': True, 'with_slacs_kcwi': True, 'with_sl2s': False, 'with_pantheon': True, 'with_planck': False, 'with_DESSNIa': False}, #5
                {'cosmology': 'FLCDM', 'with_tdcosmo': True, 'with_slacs_kcwi': False, 'with_sl2s': True, 'with_pantheon': True, 'with_planck': False, 'with_DESSNIa': False},  #6
                {'cosmology': 'FLCDM', 'with_tdcosmo': True, 'with_slacs_kcwi': True, 'with_sl2s': True, 'with_pantheon': True, 'with_planck': False, 'with_DESSNIa': False},   #7
                # lensing+DES in FLCDM
                {'cosmology': 'FLCDM', 'with_tdcosmo': True, 'with_slacs_kcwi': False, 'with_sl2s': False, 'with_pantheon': False, 'with_planck': False, 'with_DESSNIa': True}, #8
                {'cosmology': 'FLCDM', 'with_tdcosmo': True, 'with_slacs_kcwi': True, 'with_sl2s': False, 'with_pantheon': False, 'with_planck': False, 'with_DESSNIa': True}, #9
                {'cosmology': 'FLCDM', 'with_tdcosmo': True, 'with_slacs_kcwi': False, 'with_sl2s': True, 'with_pantheon': False, 'with_planck': False, 'with_DESSNIa': True}, #10
                {'cosmology': 'FLCDM', 'with_tdcosmo': True, 'with_slacs_kcwi': True, 'with_sl2s': True, 'with_pantheon': False, 'with_planck': False, 'with_DESSNIa': True}, #11
                # lensing+BAO in FLCDM
                {'cosmology': 'FLCDM', 'with_tdcosmo': True, 'with_slacs_kcwi': False, 'with_sl2s': False, 'with_pantheon': False, 'with_planck': False, 'with_DESSNIa': False, 'with_BAO': True},  #12
                {'cosmology': 'FLCDM', 'with_tdcosmo': True, 'with_slacs_kcwi': True, 'with_sl2s': True, 'with_pantheon': False, 'with_planck': False, 'with_DESSNIa': False, 'with_BAO': True}, #13


                ### LCDM extension ### 
                # Open LCDM # 
                {'cosmology': 'oLCDM', 'with_tdcosmo': True, 'with_slacs_kcwi': True, 'with_sl2s': True, 'with_pantheon': False, 'with_planck': False}, #14
                {'cosmology': 'oLCDM', 'with_tdcosmo': True, 'with_slacs_kcwi': True, 'with_sl2s': True, 'with_pantheon': False, 'with_planck': True}, #15
                # FwCDM #
                {'cosmology': 'FwCDM', 'with_tdcosmo': True, 'with_slacs_kcwi': True, 'with_sl2s': True, 'with_pantheon': False, 'with_planck': False}, #16
                {'cosmology': 'FwCDM', 'with_tdcosmo': True, 'with_slacs_kcwi': True, 'with_sl2s': True, 'with_pantheon': False, 'with_planck': True}, #17
                {'cosmology': 'FwCDM', 'with_tdcosmo': True, 'with_slacs_kcwi': True, 'with_sl2s': True, 'with_pantheon': False, 'with_planck': False, 'with_BAO':True}, #18
                {'cosmology': 'FwCDM', 'with_tdcosmo': True, 'with_slacs_kcwi': True, 'with_sl2s': True, 'with_pantheon': True, 'with_planck': False, 'with_BAO':False}, #19
                # w0waCDM #
                {'cosmology': 'w0waCDM', 'with_tdcosmo': True, 'with_slacs_kcwi': True, 'with_sl2s': True, 'with_pantheon': False, 'with_planck': False}, #20
                {'cosmology': 'w0waCDM', 'with_tdcosmo': True, 'with_slacs_kcwi': True, 'with_sl2s': True, 'with_pantheon': False, 'with_planck': True}, #21
                {'cosmology': 'w0waCDM', 'with_tdcosmo': True, 'with_slacs_kcwi': True, 'with_sl2s': True, 'with_pantheon': False, 'with_planck': False, 'with_BAO':True}, #22
                {'cosmology': 'w0waCDM', 'with_tdcosmo': True, 'with_slacs_kcwi': True, 'with_sl2s': True, 'with_pantheon': True, 'with_planck': False, 'with_BAO':False}, #23
                # wphiCDM # 
                {'cosmology': 'wphiCDM', 'with_tdcosmo': True, 'with_slacs_kcwi': True, 'with_sl2s': True, 'with_pantheon': False, 'with_planck': False}, #24
                {'cosmology': 'wphiCDM', 'with_tdcosmo': True, 'with_slacs_kcwi': True, 'with_sl2s': True, 'with_pantheon': False, 'with_planck': True}, #25
                {'cosmology': 'wphiCDM', 'with_tdcosmo': True, 'with_slacs_kcwi': True, 'with_sl2s': True, 'with_pantheon': False, 'with_planck': False, 'with_BAO':True}, #26
                {'cosmology': 'wphiCDM', 'with_tdcosmo': True, 'with_slacs_kcwi': True, 'with_sl2s': True, 'with_pantheon': True, 'with_planck': False, 'with_BAO':False}, #27

                # additional test
                {'cosmology': 'w0waCDM', 'with_tdcosmo': True, 'with_slacs_kcwi':True, 'with_sl2s': True, 'with_pantheon': True, 'with_planck': False, 'with_BAO':True}, #28
                {'cosmology': 'w0waCDM', 'with_tdcosmo': True, 'with_slacs_kcwi':True, 'with_sl2s': True, 'with_pantheon': True, 'with_planck': True, 'with_BAO':True}, #29
                {'cosmology': 'wphiCDM', 'with_tdcosmo': True, 'with_slacs_kcwi': True, 'with_sl2s': True, 'with_pantheon': True, 'with_planck': False, 'with_BAO':True}, #30

]

use_quality_data_only = True # use only lenses with imaging lens models or with IFU spectroscopy

use_selected_lens_only = True # use only the sample of selected lenses; lens selected for TDCOSMO Milestone analysis are from './sample_selection.ipynb' notebook

lens_selected_slacs = ['SDSSJ0029-0055', 'SDSSJ0037-0942', 'SDSSJ1112+0826', 'SDSSJ1204+0358', 'SDSSJ1250+0523', 'SDSSJ1306+0600', 'SDSSJ1402+6321', 'SDSSJ1531-0105', 'SDSSJ1621+3931', 'SDSSJ1627-0053', 'SDSSJ1630+4520']

lens_selected_sl2s = ['SL2SJ0226-0420', 'SL2SJ0855-0147', 'SL2SJ0904-0059', 'SL2SJ2221+0115']

lens_selected_tdcosmo = ['B1608+656', 'RXJ1131-1231', 'HE0435-1223', 'SDSS1206+4332', 'WFI2033-4723', 'PG1115+080', 'DES0408-5354', 'WGD2038-4008']
if individual_lens is not None:
    lens_selected_tdcosmo = [lens for lens in lens_selected_tdcosmo if lens in individual_lens]

# 7 TDCOSMO lenses
tdcosmo_likelihood = 'tdcosmo2025_likelihood_processed_' + anisotropy + '_.pkl'
file = open(os.path.join(dir_path_tdcosmo, tdcosmo_likelihood), 'rb')
tdcosmo7_likelihood_processed = pickle.load(file)
file.close()


# SLACS with KCWI
slacs_kcwi_likelihood = 'slacs_kcwi_' + anisotropy + '_processed.pkl'
file = open(os.path.join(dir_path_slacs, slacs_kcwi_likelihood), 'rb')
slacs_kcwi_likelihood_processed = pickle.load(file)
file.close()


# SL2S
sl2s_likelihood = 'sl2s_' + anisotropy + '_processed_all.pkl' # the sl2s sample has two lens model sets (see Likelihoods/MilestoneLikelihood/ExternalLenses/SL2S/readme.md), here the pre-processed likelihoods are combined 
file = open(os.path.join(dir_path_sl2s, sl2s_likelihood), 'rb')
sl2s_likelihood_processed = pickle.load(file)
file.close()


# =================
# apply quality cut
# =================

def quality_cut(likelihood_list):
    """whether or not to use only the lenses with lens models of imaging data or with ifu spectra

    Args:
        likelihood_list (_type_): _description_

    Returns:
        _type_: _description_
    """
    likelihood_list_cut = []
    for likelihood in likelihood_list:
        if 'flag_imaging' in likelihood:
            flag_imaging = copy.deepcopy(likelihood['flag_imaging'])
            del likelihood['flag_imaging']
        else:
            flag_imaging = 1
        if 'flag_ifu' in likelihood:
            flag_ifu = copy.deepcopy(likelihood['flag_ifu'])
            del likelihood['flag_ifu']
        else:
            flag_ifu = 1

        if use_quality_data_only is True:
            if flag_imaging < 1 or flag_ifu < 1:
                pass
            else:
                likelihood_list_cut.append(likelihood)
        else:
            likelihood_list_cut.append(likelihood)
    return likelihood_list_cut


slacs_kcwi_likelihood_processed = quality_cut(slacs_kcwi_likelihood_processed)
sl2s_likelihood_processed = quality_cut(sl2s_likelihood_processed)
    

# ================================
# add external convergence profile
# ================================

def add_kappa_dist(likelihood_list, sample_name):
    """add external kappa distribution for the SL2S and the SLACS sample

    Args:
        likelihood_list (_type_): likelihood list
        sample_name (_type_): 'SLACS' or 'SL2S'

    Returns:
        _type_: updated likelihood list
    """
    lens_name_list = [x['name'] for x in likelihood_list]
    list_kappa_ext = []
    lens_list = []

    if sample_name == 'SLACS':
        kappa_choice_ending = '_computed_1innermask_nobeta_zgap-1.0_-1.0_fiducial_120_gal_120_oneoverr_23.0_med_increments2_2_emptymsk.cat'
        kappa_bins = np.linspace(-0.05, 0.2, 50)
        
        for name in lens_name_list:
            try:
                filepath = os.path.join(dir_path_slacs+'/kappa_ext/', 'kappahist_'+name+kappa_choice_ending)
                output = np.loadtxt(filepath, delimiter=' ', skiprows=1)
                kappa_sample = output[:, 0]
                kappa_weights = output[:, 1]
                kappa_pdf, kappa_bin_edges = np.histogram(kappa_sample, weights=kappa_weights, bins=kappa_bins, density=True)
                list_kappa_ext.append({'los_distribution_individual': 'PDF', 'kwargs_los_individual': {'bin_edges': kappa_bin_edges, 'pdf_array': kappa_pdf}})
                lens_list.append(name)
            except:
                print('lens %s does not have a kappa_ext file %s' % (name, filepath))
    elif sample_name == 'SL2S':
        df_sl2s_los_gev = os.path.join(dir_path_sl2s, 'kappa_ext', 'sl2s_los_gev.csv')
        df_sl2s_los_gev = pd.read_csv(df_sl2s_los_gev) # read in sl2s los data with GEV fit
        log_sigma_kappa_ext = df_sl2s_los_gev['log_sigma_kext'].values
        xi_kappa_ext = df_sl2s_los_gev['xi_kext'].values
        mu_kappa_ext = df_sl2s_los_gev['mu_kext'].values
        name_gev_los = list(df_sl2s_los_gev['name'].values)
        
        for name in lens_name_list:
            if name in name_gev_los: 
                pos = name_gev_los.index(name)
                lens_list.append(name)
                list_kappa_ext.append({'kwargs_los_individual': {'mean': mu_kappa_ext[pos], 'xi': xi_kappa_ext[pos], 'sigma': np.exp(log_sigma_kappa_ext[pos])}, 'los_distribution_individual': 'GEV'}) 
            else: 
                print('lens %s does not have a kappa_ext distribution' % name)
    
    likelihood_list_new = []
    for i, name in enumerate(lens_list):
        pos = lens_name_list.index(name)
        kwargs_lens = likelihood_list[pos]
        kwargs_lens['kwargs_los_individual'] = list_kappa_ext[i]['kwargs_los_individual']
        kwargs_lens['los_distribution_individual'] = list_kappa_ext[i]['los_distribution_individual']
        likelihood_list_new.append(kwargs_lens)
    return likelihood_list_new


slacs_kcwi_likelihood_processed = add_kappa_dist(slacs_kcwi_likelihood_processed, 'SLACS')
sl2s_likelihood_processed = add_kappa_dist(sl2s_likelihood_processed, 'SL2S')


# ========================
# use selected lenses only
# ========================

def selected_likelihood(lens_list_selected, likelihood_list):
    """select the likelihoods of selected lenses

    Args:
        lens_list_selected (_type_): list of lens names 
        likelihood_list (_type_): list of lens likelihoods containing selected lenses

    Returns:
        _type_: list of lens likelihoods of selected lenses
    """
    likelihood_new = []
    name_all = [x['name'] for x in likelihood_list]
    for name in lens_list_selected:
        try:
            pos = name_all.index(name)
            likelihood_new.append(likelihood_list[pos])
        except ValueError:
            pass
    print('selected lens sample has {} lenses' .format(len(likelihood_new)))
    return likelihood_new


if use_selected_lens_only:
    slacs_kcwi_likelihood_processed = selected_likelihood(lens_selected_slacs, slacs_kcwi_likelihood_processed)
    sl2s_likelihood_processed = selected_likelihood(lens_selected_sl2s, sl2s_likelihood_processed)
    tdcosmo7_likelihood_processed = selected_likelihood(lens_selected_tdcosmo, tdcosmo7_likelihood_processed)

if boost_vel_disp_error is not None:
    print('WARNING boosting the velocity dispersion error by a factor of %s' % boost_vel_disp_error)
    for likelihood in tdcosmo7_likelihood_processed:
        likelihood['error_cov_measurement'] *= 100

# ================================= 
# apply axisymmetric JAM correction
# ================================= 

def read_kin_correction(likelihood_list_selected, sample_name):
    if sample_name == "SLACS_IFU":
        file_name = os.path.join(dir_path, "kin_axi_jam_scaling/kcwi_correction.pickle")
    if sample_name == "SL2S":
        file_name = os.path.join(dir_path,"kin_axi_jam_scaling/sl2s_correction.pickle")
    if sample_name == "TDCOSMO":
        file_name = os.path.join(dir_path,"kin_axi_jam_scaling/tdcosmo_correction.pickle")

    with open(file_name, "rb") as f:  # read in pre-saved correction file
        jam_scaling = pickle.load(f)

    likelihood_list_new = copy.deepcopy(likelihood_list_selected)

    name_list = [x["name"] for x in likelihood_list_new]
    for name in name_list:
        if name not in [x["name"] for x in jam_scaling]:
            print("no axisymmetric jam scaling for lens %s" % name)
        else:
            pos = name_list.index(name)
            correction = [
                x["correction_combined"] for x in jam_scaling if x["name"] == name
            ]
            likelihood_list_new[pos]["vel_disp_scaling_distributions"] = correction[0]

    return likelihood_list_new


if kin_axi_correction is True:
    slacs_kcwi_likelihood_processed = read_kin_correction(slacs_kcwi_likelihood_processed, 'SLACS_IFU')
    sl2s_likelihood_processed = read_kin_correction(sl2s_likelihood_processed, 'SL2S')
    tdcosmo7_likelihood_processed = read_kin_correction(tdcosmo7_likelihood_processed, 'TDCOSMO')


# =============================================
# remove the gamma_pl prior for the KCWI lenses
# =============================================

remove_ifu_gammapl_prior = True

if remove_ifu_gammapl_prior:
    # remove the gamma_pl prior for the KCWI lenses
    for likelihood in slacs_kcwi_likelihood_processed:
        for item in likelihood['prior_list']:
            if 'gamma_pl' in item:
                likelihood['prior_list'].remove(item)
                break

def run_sampling(run_name, cosmology, with_tdcosmo, with_slacs_kcwi, with_sl2s, with_pantheon, with_planck=False, with_BAO=False, with_DESSNIa=False,
                run_chain = True):
    """
    :param run_name: (string) name of files
    :param cosmology: (string) currently supported models within hierArc: 'FLCDM', "FwCDM", "w0waCDM", "oLCDM"
    :param with_tdcosmo: TDCOSMO sample included
    :param with_slacs_kcwi: (boolean) SLACS KCWI kinematics included
    :param with_sl2s: (boolean) SL2S kinematics included
    :param with_pantheon: (boolean) Pantheon+ data included
    :param with_DESSNIa: (boolean) DESSN Ia Y5 sample included
    :param with_planck: Planck 2018 likelihood included
    :param with_BAO: (boolean) BAO likelihood included
    :param raun_chain: run a new mcmc chain, or start from backend 
    """
    # =============================
    # EMCEE SAMPLING CONFIGURATIONS
    # =============================

    # file name of chains. ATTENTION!!! Do not store them in version control and chose a different path!
    filename = os.path.join(output_dir, run_name)
    if with_tdcosmo is True:
        filename += '_tdcosmo'
    if with_slacs_kcwi is True:
        filename += '_slacsKCWI'
    if with_sl2s is True:
        filename += '_sl2s'
    if with_pantheon is True:
        filename += '_pantheon'
    if with_planck is True:
        filename += '_planck'
    if with_BAO is True:
        filename += '_DESIdr2'
    if with_DESSNIa is True:
        filename += '_DES5YR'

    filename += '_'+ cosmology
    if individual_lens is not None:
        filename += '_indlens'
        filename += '_'.join(lens_selected_tdcosmo)
    filename += '_chain.h5'

    # Set up the backend
    # Don't forget to clear it in case the file already exists
    backend = emcee.backends.HDFBackend(filename)
    
    mcmc_sampler, kwargs_mean_start, kwargs_sigma_start, kwargs_sampler = initialization(cosmology=cosmology, 
                                                                                        with_tdcosmo=with_tdcosmo, with_slacs_kcwi=with_slacs_kcwi, with_sl2s=with_sl2s, with_pantheon=with_pantheon, 
                                                                                        with_planck=with_planck, 
                                                                                        with_BAO=with_BAO, with_DESSNIa=with_DESSNIa)
    

    # these configs are such that you can locally execute it in few hours, not meant to provide converged chains!
    kwargs_emcee = {'n_walkers':100,  # number of walkers
                    'n_run': n_run_emcee,  # number of iterations saved in the file
                    'n_burn': n_burn_emcee,  # number of iterations as burn-in prior to start saving the chain
                    'continue_from_backend': continue_from_backend,  # boolean, if True, continues sampling the emcee chain from a backend (if exists), otherwise deletes previous chains and starts from scratch
                    'kwargs_mean_start': kwargs_mean_start,  # starting positions as configured
                    'kwargs_sigma_start': kwargs_sigma_start,  # starting position as configured
                    'backend': backend,
                   }
    
    multiprocessing = True
    use_MPI = True
    if multiprocessing is True:
        if use_MPI: 
            from schwimmbad import MPIPool
            pool = MPIPool()
            if not pool.is_master():
                pool.wait()
                sys.exit(0)
            kwargs_emcee['pool'] = pool

        else: 
            from multiprocessing import Pool
            pool = Pool()
            kwargs_emcee['pool'] = pool
    
    if run_chain is True:
        mcmc_samples, log_prob = mcmc_sampler.mcmc_emcee(**kwargs_emcee)
    else:
        backend = emcee.backends.HDFBackend(filename=filename)
        mcmc_samples = backend.get_chain(discard=kwargs_emcee["n_burn"], flat=True, thin=1)
        log_prob = backend.get_log_prob(discard=kwargs_emcee["n_burn"], flat=True, thin=1)
        
    return mcmc_samples, log_prob, filename, kwargs_sampler



class CustomPrior(object):
    def __init__(self, log_scatter=False, anisotropy='const'):
        """Costomized prior distribution

        Args:
            log_scatter (bool, optional): _description_. Defaults to False.
            anisotropy (str, optional): _description_. Defaults to 'const'.
        """
        self._log_scatter = log_scatter
        # we use flat priors on constant anisotropy, and 1/a_ani prior for Osipkov-Merrit anisotropy
        if anisotropy == 'const': 
            self._ani_log = False
        else:
            self._ani_log = True


    def __call__(self, kwargs_cosmo, kwargs_lens, kwargs_kin, kwargs_source, kwargs_los):
        return self.log_likelihood(kwargs_cosmo, kwargs_lens, kwargs_kin, kwargs_source, kwargs_los)

    def log_likelihood(self, kwargs_cosmo, kwargs_lens, kwargs_kin, kwargs_source, kwargs_los):

        logL = 0

        if self._log_scatter is True:
            lambda_mst_sigma = kwargs_lens.get('lambda_mst_sigma', 1)
            logL += np.log(1/lambda_mst_sigma)
            a_ani_sigma = kwargs_kin.get('a_ani_sigma', 1)
            logL += np.log(1/a_ani_sigma)
            sigma_v_sys_error = kwargs_kin.get('sigma_v_sys_error', 1)
            logL += np.log(1/sigma_v_sys_error)
        if self._ani_log is True:
            a_ani = kwargs_kin.get('a_ani', 1)
            logL += np.log(1/a_ani)
        return logL

    
    
def initialization(cosmology, with_tdcosmo, with_slacs_kcwi, with_sl2s, with_pantheon, with_planck=False, with_BAO=False, with_DESSNIa=False):
    """
    :param cosmology: (string) currently supported models within hierArc: 'FLCDM', "FwCDM", "w0waCDM", "oLCDM"
    :param with_tdcosmo: TDCOSMO sample included
    :param with_slacs_kcwi: (boolean) SLACS KCWI kinematics included
    :param with_sl2s: (boolean) SL2S kinematics included
    :param with_pantheon: (boolean) Pantheon+ data included
    :param with_planck: Planck 2018 likelihood included
    :param with_BAO: (boolean) BAO likelihood included
    :param with_DESSNIa: (boolean) DESSN Ia Y5 sample included
    """
    # ==========================
    # COSMOLOGY SAMPLING OPTIONS
    # ==========================

    # currently supported models within hierArc: 'FLCDM', "FwCDM", "w0waCDM", "oLCDM"
    # parameters are: 'h0', 'om', 'ok', 'w', 'w0', 'wa'

    # we are sampling a flat LCDM cosmology with parameters 'h0' and 'om' as an example
    kwargs_lower_cosmo = {'h0': 0, 'om': 0.05, 'w': -1.5, 'ok': -0.5, 'w0': -1.5 ,'wa':-10, 'alpha':1.35}  # lower bounds on cosmology parameters
    kwargs_upper_cosmo = {'h0': 150, 'om': 0.5, 'w': 0.5, 'ok': 0.5, 'w0':0.5,'wa':10, 'alpha':1.55}  # upper bounds on cosmology parameters
    kwargs_cosmo_start_mean = {'h0': 70, 'om': 0.3, 'w': -1, 'ok': 0, 'w0':-1,'wa':0, 'alpha':1.45}  # mean start particles
    kwargs_cosmo_start_sigma = {'h0': 10, 'om': 0.1, 'w': 0.3, 'ok': 0.2, 'w0':0.3,'wa':1,'alpha':0.05}  # width of start particles

    # these values are held fixed throughout the entire sampling (optinal to add here)
    kwargs_fixed_cosmo = {}


    # ==================================================================
    # DEFAULT OPTIONS FOR NUISSANCES AND PRIORS (NO NEED TO TOUCH THOSE)
    # ==================================================================

    # these settings cast the chosen options above into the hierArc sampling options and completes them with the 
    # hyper-parameter settings and priors as chosen in TDCOSMO IV
    # you don't need to touch these configurations

    kwargs_lower_lens = {'lambda_mst': 0.5, 'lambda_mst_sigma': 0.001, 'alpha_lambda': -1, 'gamma_pl_list': np.ones(30) * 1.1}
    kwargs_upper_lens = {'lambda_mst': 1.5, 'lambda_mst_sigma': .5, 'alpha_lambda': 1, 'gamma_pl_list': np.ones(30)*2.9}

    if anisotropy == 'OM':
        kwargs_lower_kin = {'a_ani': 0.1, 'a_ani_sigma': 0.01, 'sigma_v_sys_error': 0.01}
        kwargs_upper_kin = {'a_ani': 5, 'a_ani_sigma': 1., 'sigma_v_sys_error': 0.5}
    if anisotropy == 'const':
        if anisotropy_parameterization == 'beta':
            kwargs_lower_kin = {'a_ani': -0.49, 'a_ani_sigma': 0.01, 'sigma_v_sys_error': 0.01} # 'a_ani' corresponds to 'beta'
            kwargs_upper_kin = {'a_ani': 1, 'a_ani_sigma': 1., 'sigma_v_sys_error': 0.5}
        elif anisotropy_parameterization == 'TAN_RAD':
            kwargs_lower_kin = {'a_ani': 0.87, 'a_ani_sigma': 0.01, 'sigma_v_sys_error': 0.01} # 'a_ani' corresponds to 'sigma_tan/sigma_rad'
            kwargs_upper_kin = {'a_ani': 1.12, 'a_ani_sigma': 1., 'sigma_v_sys_error': 0.5}

    # these values are held fixed throughout the entire sampling (optinal to add here)
    kwargs_fixed_lens = {}  # if you fix lambda_mst=1 here, you effectively assume the power-law mass profile used in Wong et al. Millon et al. Shajib et al.
    kwargs_fixed_kin = {}
    if not lambda_mst_sampling: 
        kwargs_fixed_lens['lambda_mst'] = 1.0
        kwargs_fixed_lens['lambda_mst_sigma'] = 0.0
    if not alpha_lambda_sampling:
        kwargs_fixed_lens['alpha_lambda'] = 0.0
    if not anisotropy_sampling:
        if anisotropy == 'OM':
            kwargs_fixed_kin['a_ani'] = 1.0
            kwargs_fixed_kin['a_ani_sigma'] = 0.0
        elif anisotropy == 'const':
            if anisotropy_parameterization == 'beta':
                kwargs_fixed_kin['a_ani'] = 0.0
                kwargs_fixed_kin['a_ani_sigma'] = 0.0
            elif anisotropy_parameterization == 'TAN_RAD':
                kwargs_fixed_kin['a_ani'] = 1.0
                kwargs_fixed_kin['a_ani_sigma'] = 0.0
    if fixed_Om:
        kwargs_fixed_cosmo['om'] = 0.3

    kwargs_kin_start = {'a_ani': 1, 'a_ani_sigma': 0.1, 'sigma_v_sys_error': 0.05}
    if anisotropy == 'const' and anisotropy_parameterization == 'beta':
        kwargs_kin_start['a_ani'] = 0

    kwargs_mean_start = {'kwargs_cosmo': kwargs_cosmo_start_mean,
                         'kwargs_lens': {'lambda_mst': 1., 'lambda_mst_sigma': .05, 'alpha_lambda': 0, 'gamma_pl_list': np.ones(30)* 2},
                         'kwargs_kin': kwargs_kin_start}

    kwargs_sigma_start = {'kwargs_cosmo': kwargs_cosmo_start_sigma,
                         'kwargs_lens': {'lambda_mst': .1, 'lambda_mst_sigma': .05, 'alpha_lambda': 0.1, 'gamma_pl_list': np.ones(30)*0.05},
                         'kwargs_kin': {'a_ani': 0.3, 'a_ani_sigma': 0.1, 'sigma_v_sys_error': 0.05}}

    log_scatter = True  # scatter parameters sampled in log space with linear prior in log space 


        
    # =================
    # Planck likelihood
    # =================

    if with_planck is True:
        from hierarc.Likelihood.KDELikelihood.chain import import_Planck_chain
        if cosmology == 'FLCDM':
            index_planck = 0
        elif cosmology == 'oLCDM':
            index_planck = 1
        elif cosmology == 'FwCDM':
            index_planck = 2
        elif cosmology == 'w0waCDM':
            index_planck = 6
        elif cosmology == 'wphiCDM':
            index_planck = 14
        else:
            raise ValueError('cosmology %s not supported for Planck likelihood implemented in hierArc' % cosmology)

        Planck_chain_list = [
            {"kw": "base", "probe":"plikHM_TTTEEE_lowl_lowE", "cosmology":"FLCDM", "free_params":["h0", "om"]},
            {"kw": "base_omegak", "probe":"plikHM_TTTEEE_lowl_lowE", "cosmology":"oLCDM", "free_params":["h0",  "om", "ok"]},
            {"kw": "base_w", "probe":"plikHM_TTTEEE_lowl_lowE", "cosmology":"FwCDM", "free_params":["h0", "om", "w"]},
            {"kw": "base_mnu", "probe":"plikHM_TTTEEE_lowl_lowE", "cosmology":"FLCDM", "free_params":["h0", "om"]},
            {"kw": "base_nnu", "probe":"plikHM_TTTEEE_lowl_lowE", "cosmology":"FLCDM", "free_params":["h0", "om"]},
            {"kw": "base_nnu_mnu", "probe":"plikHM_TTTEEE_lowl_lowE", "cosmology":"FLCDM", "free_params":["h0", "om"]},
            {"kw": "base_w_wa", "probe":"plikHM_TTTEEE_lowl_lowE_BAO", "cosmology":"w0waCDM","free_params":["h0", "om", "w0", "wa"]},
            {"kw": "base_omegak", "probe":"plikHM_TTTEEE_lowl_lowE_lensing", "cosmology":"oLCDM","free_params":["h0",  "om", "ok"]},
            {"kw": "base_omegak", "probe":"plikHM_TTTEEE_lowl_lowE_BAO", "cosmology":"oLCDM","free_params":["h0",  "om", "ok"]},   
            {"kw": "base_w", "probe":"plikHM_TTTEEE_lowl_lowE_BAO", "cosmology":"FwCDM", "free_params":["h0", "om", "w"]},
            {"kw": "base_nnu", "probe":"plikHM_TTTEEE_lowl_lowE_BAO", "cosmology":"FLCDM", "free_params":["h0", "om"]},
            {"kw": "base_mnu", "probe":"plikHM_TTTEEE_lowl_lowE_BAO", "cosmology":"FLCDM", "free_params":["h0", "om"]},
            {"kw": "base_mnu", "probe":"plikHM_TTTEEE_lowl_lowE_lensing", "cosmology":"FLCDM", "free_params":["h0", "om"]},
            {"kw": "base_nnu_mnu", "probe":"plikHM_TTTEEE_lowl_lowE_BAO", "cosmology":"FLCDM", "free_params":["h0", "om"]}, 
            {"kw": "base_wphi", "probe":"plikHM_TTTEEE_lowl_lowE", "cosmology":"wphiCDM", "free_params":["h0", "om", "w0", "alpha"]}, 
        ]

        assert cosmology == Planck_chain_list[index_planck]['cosmology'] # checking whether the same cosmology is being used
        cosmo_params = Planck_chain_list[index_planck]["free_params"]
        if cosmology == 'wphiCDM':
            # for wphiCDM, the chains are not part of the Planck data release, we import them manually
            from hierarc.Likelihood.KDELikelihood.chain import Chain
            chain = pd.read_csv(os.path.join(dir_path_Planck_chain, "planck_w_phicdm.txt"), delim_whitespace=True)
            params_dic = {cosmo_params[i]:chain[cosmo_params[i]] for i in range(len(cosmo_params))}
            params_dic['h0'] = params_dic['h0'] * 100.  # convert h0 to the same units as in hierArc, provided chains are h0/100
            planck_chain = Chain(kw=Planck_chain_list[index_planck]["kw"], probe=Planck_chain_list[index_planck]["probe"],
                                 default_weights=chain['weight'], 
                                params=params_dic, cosmology=cosmology, rescale=True) 
        else : 
            planck_chain = import_Planck_chain(datapath=dir_path_Planck_chain,
                                            kw=Planck_chain_list[index_planck]["kw"], 
                                            probe=Planck_chain_list[index_planck]["probe"], 
                                            params=cosmo_params, cosmology=cosmology, rescale=True)

        kwargs_kde_likelihood = {'likelihood_type':'kde_hist_nd',
                                'weight_type':'default',
                                'kde_kernel':'gaussian',
                                'bandwidth':0.01, 'nbins_hist':30}
    else:
        kwargs_kde_likelihood = None
        planck_chain = None

    # ==========================
    # BAO LIKELIHOOD
    # ==========================
    if with_BAO is True:
        bao_likelihood = 'DESI_DR2'
        kwargs_lower_cosmo['rd']=0.
        kwargs_upper_cosmo['rd']=300
        kwargs_mean_start['kwargs_cosmo']['rd']=150
        kwargs_sigma_start['kwargs_cosmo']['rd']=20
        rd_sampling = True
        interpolate_cosmo = False

    else:
        bao_likelihood = None
        rd_sampling = False
        interpolate_cosmo = True
        
        
    kwargs_bounds = {'kwargs_lower_cosmo': kwargs_lower_cosmo,
                    'kwargs_lower_lens': kwargs_lower_lens,
                    'kwargs_lower_kin': kwargs_lower_kin,
                    'kwargs_upper_cosmo': kwargs_upper_cosmo,
                    'kwargs_upper_lens': kwargs_upper_lens,
                    'kwargs_upper_kin': kwargs_upper_kin,
                    'kwargs_fixed_cosmo': kwargs_fixed_cosmo,
                    'kwargs_fixed_lens': kwargs_fixed_lens,
                    'kwargs_fixed_kin': kwargs_fixed_kin}


    kwargs_likelihood_list = []
    if with_tdcosmo:
        kwargs_likelihood_list += tdcosmo7_likelihood_processed
    if with_sl2s:
        kwargs_likelihood_list += sl2s_likelihood_processed
    if with_slacs_kcwi:
        kwargs_likelihood_list += slacs_kcwi_likelihood_processed
    

    # add num_distribution_draw and lambda_scaling_property
    num_distribution_draws = 200  # potentially should go up to 200 for more accurate likelihood calculation
    for likelihood in kwargs_likelihood_list:
        if 'num_distribution_draws' not in likelihood:
            likelihood['num_distribution_draws'] = num_distribution_draws
        if 'lambda_scaling_property' not in likelihood:
            likelihood['lambda_scaling_property'] = likelihood['kwargs_lens_properties'].get('r_eff') / likelihood['kwargs_lens_properties'].get('theta_E') - 1

    if with_pantheon and with_DESSNIa:
        raise ValueError('You cannot use both Pantheon and DESSN Ia Y5 likelihoods at the same time. Please choose one of them.')
    else: 
        sne_likelihood = None
        if with_pantheon is True:
            sne_likelihood = 'PantheonPlus'
        if with_DESSNIa is True:
            sne_likelihood = 'DES5YR'            
    
    if anisotropy in ["OM", "GOM"]:
        anisotropy_distribution = "GAUSSIAN_SCALED"
    elif anisotropy == 'const':
        anisotropy_distribution = "GAUSSIAN"

    if not anisotropy_sampling:
        anisotropy_distribution = "NONE"
    if not lambda_mst_sampling:
        lambda_mst_distribution = "NONE"
    else:
        lambda_mst_distribution = "GAUSSIAN"
        
    # dict of model parameters of lens and kinematics model
    kwargs_model = {'lambda_mst_sampling': True,
                      'lambda_mst_distribution': lambda_mst_distribution,
                      'anisotropy_sampling': True,
                      'sigma_v_systematics': False,
                      'anisotropy_model': anisotropy,
                      'anisotropy_distribution': anisotropy_distribution,  # for OM, GOM, use GAUSSIAN_SCALED, for const use GAUSSIAN
                      'alpha_lambda_sampling': alpha_lambda_sampling,
                      'anisotropy_parameterization': anisotropy_parameterization,
                      'rd_sampling': rd_sampling,
    }
    print('kwargs_model: %s' % kwargs_model)

    # patch all the options together into a keyword arguments list compatible with the hierArc MCMCSampler() class instance    

    kwargs_sampler = {'kwargs_likelihood_list': kwargs_likelihood_list,
                      'kwargs_model': kwargs_model,
                      'cosmology': cosmology,
                      'sne_likelihood': sne_likelihood,
                      'bao_likelihood': bao_likelihood,
                      'interpolate_cosmo': interpolate_cosmo, 
                      'num_redshift_interp': 100,
                      'custom_prior': CustomPrior(log_scatter=log_scatter, anisotropy=anisotropy),
                      'kwargs_bounds': kwargs_bounds,
                      'KDE_likelihood_chain': planck_chain,
                      'kwargs_kde_likelihood': kwargs_kde_likelihood,
                      }
    
    

    mcmc_sampler = MCMCSampler(**kwargs_sampler)
    return mcmc_sampler, kwargs_mean_start, kwargs_sigma_start, kwargs_sampler


kwargs_options = sampling_list[sampling_index]  # choose the first sampling option
print('SAMPLING OPTIONS: %s' % kwargs_options)

mcmc_sampler, kwargs_start_mean, kwargs_start_sigma, kwargs_sampler = initialization(**kwargs_options)

param = mcmc_sampler.param

args = param.kwargs2args(**kwargs_start_mean)

mcmc_sampler.chain.likelihood(args, verbose=True)

print(mcmc_sampler.param_names(latex_style=True))

# ============
# RUN SAMPLING
# ============

start = time.time()
mcmc_samples, log_prob, filename, kwargs_sampler = run_sampling(run_name, **kwargs_options, run_chain=run_chain)
end = time.time()
print('Total time: ', end-start)
print('Time per iteration: ', (end-start)/n_run_emcee)

print('backend filename: ', filename)

update_kwargs_sampler = not continue_from_backend

if update_kwargs_sampler:
    # sampler kwargs are needed to make diagnostic plots
    filename_kwargs_sampler = copy.deepcopy(filename)
    filename_kwargs_sampler = filename_kwargs_sampler.replace('_chain.h5', '_sampler_kwargs.pkl')
    print('sampler configuration filename: ', filename_kwargs_sampler)
    with open(filename_kwargs_sampler, 'wb') as f:
        pickle.dump(kwargs_sampler, f)
