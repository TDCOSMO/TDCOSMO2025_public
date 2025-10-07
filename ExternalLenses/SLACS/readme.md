# SLACS lenses

The file slacs_all_params.csv includes all the relevant meta data and parameter fits.
Further KCWI kinematic data is in the slacs_kcwi_data folder.

The jupyter notebook kinematics_sample_slacs_preprocessing.ipynb hosts the code and scripts to process the meta data
turn them into likelihood objects for hierArc, including the kinematic modeling.

### Columns in slacs_all_params.csv

- flag_imaging_tan23 : Flags for system with lens models from Tan23 
- flag_imaging_shajib20 : Flags for system with lens models from Shajib20
- sigma_v,sigma_v_error : updated velocity dispersion from TDCOSMO/hierarchy_analysis_2020_public/SLACS_sample/vdisp_slacs_asb.fits
- r_eff_auger : V-band effective radius measurements from Auger09 (Fitted using Heinquist profiles)
- theta_E_auger : einstein radius measurements from Auger09
- gamma_error_stat : statistical error on gamma estimated from mcmc chains
- gamma_error_sys : systematic error on gamma (refer to DINOS I paper), total error on gamma is obtained by adding both errors by quadrature
- e1_mass, e2_mass : the eccentricity parameters for the Power law ellipse mass density profile (PEMD)
- r_eff: the effective half-light radius from double/single Sersic fits by Chin Yi using HST F555W/F606W/F814W image with the lowest background rms
- r_sersic_1, n_sersic_1, amp_sersic_1: associated Sersic function parameters for the first Sersic
- r_sersic_2, n_sersic_2, amp_sersic_2: associated Sersic function parameters for the second Sersic
- e1_sersic , e2_sersic :  eccentricity parameters for the Sersic function. The ellipticity is joint for both Sersic profiles
- lensing_information_dinosi : lensing information determined by the flux strength of the lensed arcs (see eq 9 in Dinos-I; using a=15, b=0.).
- lensing_information_dinosii : lensing information determined by the flux strength of the lensed arcs (see eq 2 in Dinos-II; using a=1.7963459409128497, b=0.2401960341440724). This value is equivalent to lensing_information column in SL2S/sl2s_all_params_ws.csv
- n_bin_kcwi, psf_ifu_kcwi, flag_ifu_kcwi : Number of radial bins for KCWI data for object, average PSF of datacubes, and flag for use (1 is positive)
- spectra_snr_flag : Flags for SNR > 15 for SDSS spectra of this system (from vdisp_slacs_smk.fits from Shawn Knabel shawnknabel@gmail.com)
- sigma_v_smk, sigma_v_error_smk : updated velocity dispersions from Shawn Knabel (shawnknabel@gmail.com) from vdisp_slacs_smk.fits
- sdss_spectra_snr : SNR per AA for SDSS spectra (from vdisp_slacs_smk.fits from Shawn Knabel)
- sigma_v_kcwi_half_reff,sigma_v_kcwi_half_reff_error : "effective" velocity dispersions from KCWI within 1/2 the effective radius integrated over the datacube before extraction; suitable for comparison with other single-aperture kinematics; uncertainties include 0.9% systematic uncertainties added in quadrature (same as for the radially binned KCWI data, see note below)


#####################################

SLACS KCWI data (e.g. slacs_kcwi_data/SDSSJ0029-0055/SDSSJ0029-0055_kinmap.csv)

14 SLACS lenses from Knabel et al. 2025 - Spatially Resolved Kinematics of SLACS Lenses I. KCWI data is an IFU datacube that has spatial and spectral information. So the "map" is 2D, showing where bins in different parts of the galaxy result in different velocities (mean and dispersion). These maps are rebinned to radial shells by luminosity-weighted contributions from the spatial bins, where Vrms_shell^2 = sqrt( weight * Vrms_bin^2 ). They are recentered bit fitting the light profile of the inner bins to ensure the radial profile is not offset. The "kinmap.csv' file contains three columns: bin_inner_edge, bin_outer_edge, binned_Vrms. Units are [arcssec, arcsec, km/s]. Each should have 6 or 7 bins. The covariance matrix (e.g. SDSSJ0029-0055_kinmap_cov.csv) gives the covariance between the bins, where the diagonal includes the statistical and systematic uncertainties added in quadrature (sigma^2 = sigma_syst^2 + sigma_stat^2). The systematic uncertainty is the combined effect of the template libraries and the continuum polynomial degrees (sigma_syst^2 = sigma_temp^2 + sigma_poly^2) and is on average 0.9%.

#####################################

SLACS KCWI table (slacs_kcwi_kinematics_table.csv) from Shawn M Knabel (up to date as of 2025/04/02)

Table 2 from Knabel et al. 2025 - Spatially Resolved Kinematics of SLACS Lenses I (arxiv version not up to date, currently in referee's hands)

14 SLACS lenses. KCWI data is an IFU datacube that has spatial and spectral information. So the "map" is 2D, showing where bins in different parts of the galaxy result in different velocities (mean and dispersion). The table contains velocity dispersions integrated from different apertures (and techniques) from the datacube as well as SDSS velocity dispersions from myself, Adam Bolton, and the SDSS catalog (as in SLACS-IX and -X). Also contains kinematic classifications from V-sigma and Lambda_R, defined below.

Columns:
- obj_name : SDSS name
- zlens : redshift of lens
- VD_half_reff, dVD_half_reff : KCWI velocity dispersion integrated over the 2D velocity dispersion map within half the effective radius; IMPORTANT: not the same thing as an "effective" velocity dispersion measured from a single aperture, where the line disperion is also due to the mean rotational velocity that is positive and negative on different sides of the galaxy... If you want the effecitve velocity dispersion suitable for comparison with other single-aperture kinematics, see the columns "sigma_v_kcwi_half_reff,sigma_v_kcwi_half_reff_error" in slacs_all_params.csv
- VD_reff, dVD_reff : KCWI velocity dispersion integrated over the 2D velocity dispersion map within the effective radius; IMPORTANT: not the same thing as an "effective" velocity dispersion measured from a single aperture, where the line disperion is also due to the mean rotational velocity that is positive and negative on different sides of the galaxy
- VD_sdssap_kcwi, dVD_sdssap_kcwi : KCWI velocity dispersion from spectrum integrated over 1.5'' (SDSS fiber aperture size) from the datacube; different from integrating over the 2D kinematic map; IMPORTANT: has been convolved with mock seeing from SDSS to compare with SDSS velocity dispersions
- VD_sdss_smk, dVD_sdss_smk : SDSS velocity dispersion measured by Shawn Knabel with pPXF; same as in vdisp_slacs_smk.fits
- VD_sdss_asb, dVD_sdss_asb : SDSS velocity dispersion measured by Adam Bolton; same as in vdisp_slacs_asb.fits; OUT OF DATE
- VD_slacs_ix, dVD_slacs_ix : SDSS velocity disperions from SDSS pipeline that were used in SLACS-IX and -X; used Elodie stellar template library; OUT OF DATE
- reff : effective radius in V-band (or close) from SLACS-X; sorry, I'll have to check
- ellipticity : observed ellipticity (2D projected, not intrisic) from Shawn Knabel's MGE fits to B-spline models at the half-light isophote of the surface brightness profile; this is basically an effective ellipticity because my MGE models allow for radial variation of the ellipticity; in future models (and JAM dynamical models) I will fix the ellipticity because it's simpler
- V_sigma : average of V / sigma within the effective radius; V is the rotational velocity of each bin/pixel, and sigma is the velocity dispersion for that bin/pixel; helpful for classifying early-type galaxies as fast rotators with high V_sigma against slow rotators with low V_sigma; this value is averaged from the bin values, but pixel values agree very closely
- lambda_R : average angular momentum normalized by Vrms = sqrt( V**2 + sigma**2 ); standard classifying tool for fast vs slow rotators (as V_sigma above); we calculate this from bins (as with V_sigma above); we use this for our lambda_R_class below
- lambda_R_class : "fast" or "slow" rotator determined by value of lambda_R and ellipticity; where λR < 0.08 + ϵ/0.4 and ϵ < 0.4 are slow rotators


#####################################

Updated SLACS SDSS velocity dispersions from Shawn M Knabel (up to date as of 2025/03/19)

Velocity dispersions for 341 objects measured with pPXF to succeed the ones from Adam Bolton. Most of the spectra aren't great. We consider S/N per AA > 15 to be reliable. There are only 6 from "slacs_all_params.csv" that pass this threshold. "slacs_all_params.csv" has these velocity dispersions as "sigma_v_smk", and SNR as "sdss_spectra_snr" with flags "spectra_snr_flag=1" if S/N per pixel > 15. I would not trust anything S/N < 5. Between 5 and 10 is as likely to be bad as it is good. - Shawn Knabel

vdisp_slacs_smk.fits

No.    Name      Ver    Type      Cards   Dimensions   Format

0  PRIMARY       1 PrimaryHDU      11   ()      

1  DATA          1 BinTableHDU     62   341R x 10C   ['J', 'J', 'J', 'D', 'D', 'D', 'D', 
'14A', 'D', 'D']   

2  SYST_UNC      1 BinTableHDU     47   3R x 7C   ['20A', 'D', 'D', 'D', 'D', 'D', 'D']   
  
Extension 1 "DATA"
ColDefs(
    
    name = 'PLATE'; format = 'J' --- SDSS plate
    
    name = 'FIBERID'; format = 'J' --- SDSS fiber ID
    
    name = 'MJD'; format = 'J' --- modified julian date
    
    name = 'RA'; format = 'D' --- right ascension
    
    name = 'DEC'; format = 'D' --- declination
    
    name = 'VDISP_SMK'; format = 'D' --- Shawn's measured velocity dispersion
    
    name = 'VDISP_SMK_ERR'; format = 'D' --- error on velocity dispersion
    
    name = 'SDSS_NAME'; format = '14A' --- SDSS identifier
    
    name = 'SN_PER_PIXEL'; format = 'D' --- S/N per pixel in range 3600-6000A (not preferred, use the SN_PER_AA)
    
    name = 'SN_PER_AA'; format = 'D' --- S/N per AA in range 4000-4500A
)

25/03/19 - Shawn M Knabel(shawnknabel@gmail.com): I took the vdisp_slacs_asb.fits file from TDCOSMO 2024 Milestone paper repository to replace Adam Bolton velocity dispersion measurements for the 341 SLACS lenses. If I couldn't find it, I didn't fit it. They will not have necessarily used exactly the same fiber id, because some of them have multiple pointings (see e.g. J1538 in Knabel 24a). I used pPXF (M. Cappellari) with the cl ean XSL DR3 stellar template library (as in TDCOSMO-XIX kinematic method s paper Knabel & Mozumdar et al. 2025). For a subset of high S/N objects (38 of them), XSL was by far preferred in BIC weighting. The wavelength range of fitting was 3600-5350A to account for the XSL dichroic. I also included additive polynomial degree 6, and multiplicative degree 2. \ SN_PER_AA is extracted and given in the range 4000-4500A, for helping make sense of et al. SN_PER_PIXEL was taken in range 3600-6000A and should not really be used. \ Some objects have NaN values for VD but have SNR, which means the fits failed. Others have NaN for VD and for SNR, whic h means I couldn't find them. \You can use astroquery with these plate, fiberid and mjd to get exactly the same spectra that I used. I hope this helps you if you inherit this table in the future. :)

Extension 2 "SYST_UNC"

ColDefs(
    
    name = 'index'; format = '20A' --- SNR bin index
    
    name = 'average_statistical'; format = 'D' --- mean statistical error over the bin sample
    
    name = 'average_systematic_diagonal'; format = 'D' --- sqrt of mean of diagonal of covariance matrix for bin (estimate of the relative uncertainty due to library systematics)
    
    name = 'average_systematics_off_diagonal'; format = 'D' --- sqrt of mean of off-diagonal of covariance matrix for bin (estimate of the sample-level covariance due to library systematics)
    
    name = 'average_systematic_diagonal_bessel_corrected'; format = 'D' --- same as above but with Bessel correction
    
    name = 'average_systematic_off_diagonal_bessel_corrected'; format = 'D' --- same as above but with Bessel correction
    
    name = 'bin_median_snr_per_AA'; format = 'D' --- median SNR per AA in range (4000-4500A) for bin sample.
)

"03/19/25 - Shawn M Knabel (shawnknabel@gmail.com): I binned the 341 SLACS candidates in SNR bins of 5-10, 10-15, and > 15. I then calculated the average relative statistical and systematic uncertainties over that bin sample. The Bessel correction is just the diagonal multiplied by the sqrt ( (N + 1)/N ) where N is the number of libraries (3). I also give the median signal-to-noise ratio for each bin (as in the SNR_PER_AA given in extension 1)."
