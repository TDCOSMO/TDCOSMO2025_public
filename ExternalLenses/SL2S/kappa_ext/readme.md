# Readme

This folder contains results for the estimate of $`\kappa_{\rm{ext}}`$ for 15 lenses in the SL2S sample. These results were computed with a 45” aperture with a magnitude cut of 24 in the i band. The weighted number count distributions were computed by comparing to a $64 arcsec^2$ region in the CFHTLS dataset, defined by $` 30.25 \space\rm{deg} < RA < 38.75 \space\rm{deg}`$ and $` -11.25 \space\rm{deg} < Dec < -3.75 \space\rm{deg} `$

The final inference was done using three weighted nubmer counts: $w_{1/r} = 1/r$, $w_z = z_s z_i - z_i^2$ and $w_p = m_{*}/r$

### Reading Data

This folder includes convenience function for loading result for all lenses

```python
from Likelihoods.MilestoneLikelihood.ExternalLenses.SL2S.kappa_ext import read_kappa
sl2s_kappa_ext = read_kappa.load_sl2s_lenses()
``` 

If the data and code are separated (make sure "lenses.toml" stays with the data):

```python
from pathlib import Path
from new.path.to.code import read_kappa
path = Path("/new/path/to/data/folder")
sl2s_kappa_ext = read_kappa.load_kappa_folder(path)


```

In either case, returns a dictionary of the form:

```
{
lens_name:
      {
       "bins": [-0.2, -0.195...],
       "pdf": [0.0, 0.1, 0.2...]
       },
...
}
``` 
"bins" contains the bin edges. "pdf" contains the associated probability in each bin. Probability is normalized to integrate to 1.


### Line of sight data of 25 SL2S lenses with extreme value statistics

sl2s_los_gev.csv is constitute of external convergence distributions and measured weighted number counts of 25 SL2S lenses. The external kappa distributions are expressed with general extreme value fits. The fitting parameters (shape, scale, and mean) are from table A.1 of Wells et al (2024)[https://arxiv.org/pdf/2403.10666]. The weights included are pure number count $w = N$ and inverse distance weighting $w = 1/r$. The column named "NoverRmed" corresponds to the overdensity defined as eq.(56) in TD4, with the weighting summary statistics of the lens field being the summation of individual weights (eq.). The column named 'NoverRmed_med" corresponds to the overdensity defined as eq.(56) in TD4, with the weighting summary statistics of the lens field being defined as eq.(28) in Birrer et al 2019.

These results were computed with a 120” aperture with a magnitude cut of 24 in the i band. The weighted number count distributions were computed by comparing to a $50 deg^2$ region in the CFHTLS dataset, defined by $` 31 \space\rm{deg} < RA < 38.5 \space\rm{deg}`$ and $` -11 \space\rm{deg} < Dec < -4 \space\rm{deg} `$. The external convergence are read out from kappa maps produced by Hilbert et al (2009) for the Millennium simulation. 