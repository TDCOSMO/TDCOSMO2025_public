# TDCOSMO 2025 — Cosmological Analysis

This repository contains the notebooks and script to reproduce the analysis of [arXiv:2506.03023](https://arxiv.org/abs/2506.03023)
`likelihood_sampling.py` provides the same functionality as `likelihood_sampling.ipynb` but can be run in parallel on a cluster. 
Change the parameter in the `parameter_config_example.yaml` config file.

## Kinematics pre-processing (optional)
Pickle files containing the pre-processed kinematic information are already included in this repository.
If you want to regenerate or modify them, use the notebooks below (each subfolder includes its own README):

### Time-delay sample
```
./TDCOSMO_sample/tdcosmo_sample.ipynb
```

### External lenses 
External lenses (SLACS or SL2S): 
```
./ExternalLenses/SLACS/kinematic_sample_slacs_preprocessing.ipynb
./ExternalLenses/SL2S/kinematic_sample_sl2s_preprocessing.ipynb
```

### Axisymetric correction
```
./kin_axi_jam_scaling/preprocess_axi_jam_correction.ipynb
```

## Sample selection (optional)
If you want to change the selection criterion of the SL2S and SLACS sample, see 
```
./sample_selection.ipynb
```

## Usage 
To run the MCMC chains, edit `parameter_config_example.yaml` and run: 

`python likelihood_sampling.py -f parameter_config_example.yaml` 

## Attribution

If you use these notebooks in your work, please cite:
```
@ARTICLE{2025arXiv250603023T,
       author = {{TDCOSMO Collaboration} and {Birrer}, Simon and {Buckley-Geer}, Elizabeth J. and {Cappellari}, Michele and {Courbin}, Fr{\'e}d{\'e}ric and {Dux}, Fr{\'e}d{\'e}ric and {Fassnacht}, Christopher D. and {Frieman}, Joshua A. and {Galan}, Aymeric and {Gilman}, Daniel and {Huang}, Xiang-Yu and {Knabel}, Shawn and {Langeroodi}, Danial and {Lin}, Huan and {Millon}, Martin and {Morishita}, Takahiro and {Motta}, Veronica and {Mozumdar}, Pritom and {Paic}, Eric and {Shajib}, Anowar J. and {Sheu}, William and {Sluse}, Dominique and {Sonnenfeld}, Alessandro and {Spiniello}, Chiara and {Stiavelli}, Massimo and {Suyu}, Sherry H. and {Tan}, Chin Yi and {Treu}, Tommaso and {Van de Vyvere}, Lyne and {Wang}, Han and {Wells}, Patrick and {Williams}, Devon M. and {Wong}, Kenneth C.},
        title = "{TDCOSMO 2025: Cosmological constraints from strong lensing time delays}",
      journal = {arXiv e-prints},
     keywords = {Cosmology and Nongalactic Astrophysics},
         year = 2025,
        month = jun,
          eid = {arXiv:2506.03023},
        pages = {arXiv:2506.03023},
          doi = {10.48550/arXiv.2506.03023},
archivePrefix = {arXiv},
       eprint = {2506.03023},
 primaryClass = {astro-ph.CO},
       adsurl = {https://ui.adsabs.harvard.edu/abs/2025arXiv250603023T},
      adsnote = {Provided by the SAO/NASA Astrophysics Data System}
}
```

Corresponding author: [Martin Millon](mailto:martin.millon@unige.ch), Simon Birrer, Anowar Shajib
