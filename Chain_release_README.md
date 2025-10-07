# TDCOSMO 2025 MCMC Chain Release

This repository contains the **posterior MCMC samples** from the TDCOSMO collaboration analysis.  
Each file corresponds to one cosmological model/dataset and is stored in **HDF5 (`.h5`) format**

---

## File structure

Each file is named after the model identifier, e.g.:
```
---chains_export/
├── UoLambdaCDM.h5
├── UoFlatwCDM.h5
├── UoFlatw0waCDM.h5
└── ...
```

## File content

Each `.h5` file contains the following **datasets** and **attributes**:

### **Datasets**

| Dataset name | Shape | Description |
|---------------|--------|-------------|
| `samples` | `(n_samples, n_parameters)` | 2D array containing the MCMC samples. Each row corresponds to one posterior sample, and each column to one model parameter. |
| `parameters` | `(n_parameters,)` | List of parameter names (stored as byte strings). These correspond to the columns of `samples`. |

### **Attributes**

| Attribute | Type | Description |
|------------|------|-------------|
| `description` | string | Human-readable text describing the model, experiment, list of lenses, and the meaning of each parameter. |
| `dataset` | string | Name of the dataset combination. |
| `ModelID` | string | Identifier of the cosmological model (same as filename). |

---

## Parameter descriptions

Common parameters appearing across models include:

| Parameter | Description |
|------------|-------------|
| `h0` | Hubble constant in km s⁻¹ Mpc⁻¹ |
| `om` | Matter density parameter Ωₘ |
| `ok` | Curvature density parameter Ωₖ |
| `w`, `w0`, `wa` | Dark energy equation-of-state parameters |
| `lambda_mst` | Mean of the internal mass-sheet transformation (MST) population |
| `lambda_mst_sigma` | Gaussian scatter (1 σ) in internal MST |
| `a_ani`, `a_ani_sigma` | Mean and scatter of the stellar anisotropy parameter |
| `alpha_lambda` | Slope of the internal MST with respect to effective radius / Einstein radius |
| `rd` | Sound horizon (in Mpc) |

Additional parameters of the form `gamma_pl_<i>` correspond to the **power-law slope of the total mass density profile** for lens *i*, where the mapping to the actual system name is:

| Index | Lens name |
|:--:|:----------------|
| 0 | RXJ1131-1231 |
| 1 | SDSSJ0029-0055 |
| 2 | SDSSJ0037-0942 |
| 3 | SDSSJ1112+0826 |
| 4 | SDSSJ1204+0358 |
| 5 | SDSSJ1250+0523 |
| 6 | SDSSJ1306+0600 |
| 7 | SDSSJ1402+6321 |
| 8 | SDSSJ1531-0105 |
| 9 | SDSSJ1621+3931 |
| 10 | SDSSJ1627-0053 |
| 11 | SDSSJ1630+4520 |

---

## How to read the files

Here is a minimal Python example using **h5py**:

```python
import h5py
import numpy as np

# Load an example file
with h5py.File("chains_export/w_0w_aCDM3.h5", "r") as f:
    samples = f["samples"][:]                # MCMC samples
    parameters = [p.decode() for p in f["parameters"][:]]  # parameter names
    description = f.attrs["description"]
    model_id = f.attrs["ModelID"]
    dataset_name = f.attrs["dataset"]

print("Description:", description)
print('Sample shape:', samples.shape)
print(f"Model: {model_id}")
print(f"Dataset: {dataset_name}")
```

## Attribution 

If you use these chains in your work, please cite:
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

DOI: [to be assigned upon Zenodo release]

