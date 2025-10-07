The `rxj1131_<instrument>_binned_<quantity>_binned.h5` files contain radially binned resolved velocity dispersion or second moment measurements for RXJ1131. The `v_rms` files contain the dispersion and velocities (after subtracting the systemic velocities) added in quadrature.


The files can be read with, for example:

```
with h5.File(
    "/Users/ajshajib/Downloads/rxj1131_jwst_binned.h5",
    "r",
) as f:
    jwst_dispersions = f["binned_dispersion"][()]
    jwst_radial_bins = f["radial_bins"][()]
    jwst_covariance = f["covariance"][()]
```

The `radial_bins` are in the unit of arcseconds, and the `binned_disperson` is in the unit of km/s. The PSF FHM is 0.1476" (circularized from a 2D Gaussian profile fit) for JWST/NIRSpec, and 0.96" for Keck/KCWI.
