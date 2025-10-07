# Axisymmetric JAM correction to modeled velocity dispersion

The files "correction_beta0_oblate_aperture.pickle", "correction_beta0_prolate_aperture.pickle", "correction_beta0_oblate_annuli.pickle", "correction_beta0_prolate_annuli.pickle" contains multiplicative correction factors sigma_axi/sigma_sph forward-modeled under certain assumptions on the galaxy model (for details, see [Huang et al. 2025](https://ui.adsabs.harvard.edu/abs/2025arXiv250300235H/abstract)). 

Since the prolate and oblate population have different projection effects with their convergence and surface luminosity profiles, the axisymmetric correciton factors are models individually for both populations. 

The correction factor shows a slight radial variation whether the velocity dispersion is integrated within an aperture or within an annulus. This radial dependence is smooth when we added a PSF component when modeling the correction factor. 

For axisymmetric correction to be applied to the IFU data in this repo, one should use the "correction_beta0_\*_annuli.pickle" files. For axisymmetric correction to be applied to the slit/fiber spectra, one should use the "correction_beta0_\*_aperture.pickle" 

### Keys in "correction_beta0_oblate_aperture.pickle", "correction_beta0_prolate_aperture.pickle"

- sigma_e_axi: an array of velocity dispersions predicted with axisymmetric JAM integrated within apertures of different radii.
- sigma_e_sph: an array of velocity dispersions predicted with spherical JAM integrated within apertures of different radii.
- inc: inclination angle. Drawn from a prior which is randomly distributed on a sphere. 
- qintr: intrinsic axis ratio of the galaxy's density and stellar light profile. Drawn from a prior from [Li et al 2018](https://ui.adsabs.harvard.edu/abs/2018ApJ...863L..19L/abstract)
- qobs: projected axis ratio. 
- reff: effective radius of the aixsymmetric galaxy model.
- reff_sph: effective radius of the spherical galaxy model.
- r_scale: an array of dimensionless scale radius: r_scale * reff are the radii at which we draw apertures and calculate the velocity dispersion within. 

The multiplicative axisymmetric JAM correction factor is defined as sigma_e_axi/sigma_e_sph.

### Keys in "correction_beta0_oblate_annuli.pickle", "correction_beta0_prolate_annuli.pickle"

- sigma_e_axi: an array of velocity dispersions predicted with axisymmetric JAM integrated within annuli of radii.
- sigma_e_sph: an array of velocity dispersions predicted with spherical JAM integrated within annuli of different radii.
- inc: inclination angle. Drawn from a prior which is randomly distributed on a sphere. 
- qintr: intrinsic axis ratio of the galaxy's density and stellar light profile. Drawn from a prior from [Li et al 2018](https://ui.adsabs.harvard.edu/abs/2018ApJ...863L..19L/abstract)
- qobs: projected axis ratio. 
- reff: effective radius of the aixsymmetric galaxy model.
- reff_sph: effective radius of the spherical galaxy model.
- r_scale: an array of dimensionless radial bin edges: r_scale * reff are the radial bin edges of circular annuli in which we calculate the velocity dispersion. 

The multiplicative axisymmetric JAM correction factor is defined as sigma_e_axi/sigma_e_sph.


