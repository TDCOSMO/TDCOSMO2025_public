# SL2S lenses

The files sl2s_all_params.csv and sl2s_all_params_ws.csv include all the relevant meta data and parameter fits.

The jupyter notebook kinematics_sample_sl2s_preprocessing.ipynb hosts the code and scripts to process the meta data in sl2s_all_params.csv, turning them into likelihood objects for hierArc, including the kinematic modeling.


### Columns in sl2s_all_params.csv

- flag_imaging_tan23 : Flags for system with lens models from Tan23 
- sigma_v, sigma_v_error : updated velocity dispersion 
- r_eff_auger : V-band effective radius measurements 
- theta_E, theta_E_error : einstein radius measurements
- gamma : logarithmic slope of the power-law profile
- gamma_error_stat : statistical error on gamma estimated from mcmc chains
- gamma_error_sys : systematic error on gamma (refer to DINOS I paper), total error on gamma is obtained by adding both errors by quadrature
- e1_mass, e2_mass : the eccentricity parameters for the Power law ellipse mass density profile (PEMD)
- r_eff: the effective half-light radius from double/single Sersic fits by Chin Yi using HST F555W/F606W/F814W image with the lowest background rms
- r_sersic_1, n_sersic_1, amp_sersic_1: associated Sersic function parameters for the first Sersic
- r_sersic_2, n_sersic_2, amp_sersic_2: associated Sersic function parameters for the second Sersic
- e1_sersic , e2_sersic :  eccentricity parameters for the Sersic function. The ellipticity is joint for both Sersic profiles
- lensing_information_dinosi : lensing information determined by the flux strength of the lensed arcs (see eq 9 in Dinos-I; using a=15, b=0.)
- lensing_information_dinosii : lensing information determined by the flux strength of the lensed arcs (see eq 2 in Dinos-II; using a=1.7963459409128497, b=0.2401960341440724). This value is equivalent to lensing_information column in sl2s_all_params_ws.csv
#### below columns are added by pritom
- sigma_v_pritom, sigma_v_error_pritom : BIC weighted average velocity dispersion and error (statistical and systematic uncertainties are added in quadrature)
- snr_pritom : measured signal-to-noise ratio per Angstrom of the used spectrum for fit
- instrument_resolution_pritom, instrument_resolution_err_pritom : measured resolution (sigma, not FWHM) and associated uncertainty of the instrument in km/s


### Columns in sl2s_all_params_ws.csv

- sigma_v, sigma_v_error : updated velocity dispersion from Sonnenfeld+2013 and Sonnenfeld+2014
- theta_E, theta_E_error : einstein radius measurements
- gamma : logarithmic slope of the power-law profile
- gamma_error_stat : statistical error on gamma estimated from mcmc chains
- gamma_error_sys : systematic error on gamma (refer to DINOS I paper), total error on gamma is obtained by adding both errors by quadrature
- e1_mass, e2_mass : the eccentricity parameters for the Power law ellipse mass density profile (PEMD)
- e1_sersic1_CFHT , e1_sersic1_CFHT :  eccentricity parameters for the Sersic function using CFHT r-band imaging.
- r_sersic1_CFHT, n_sersic1_CFHT, amp_sersic1_CFHT: associated Sersic function parameters for the Sersic profile fitted using CFHT r-band imaging
- e1_sersic_F475X , e2_sersic_F475X :  eccentricity parameters for the Sersic function using HST F475X imaging. The ellipticity is joint for both Sersic profiles
- r_eff_F475X: the effective half-light radius from double/single Sersic fits using HST F475X imaging.  As the CFHT light fitting is done using a single Sersic profile, the corresponding effective half-light radius is r_sersic1_CFHT
- r_sersic_1_F475X, n_sersic_1_F475X, amp_sersic_1_F475X: associated Sersic function parameters for the first Sersic profile fitted using HST F475X imaging
- r_sersic_2_F475X, n_sersic_2_F475X, amp_sersic_2_F475X: associated Sersic function parameters for the second Sersic profile fitted using HST F475X imaging (if applicable)
- lensing_information: lensing information determined by the flux strength of the lensed arcs (see eq 2 in Dinos-II; using a=1.7963459409128497, b=0.2401960341440724)
#### below columns are added by Pritom
- sigma_v_pritom, sigma_v_error_pritom : BIC weighted average velocity dispersion and error (statistical and systematic uncertainties are added in quadrature)
- snr_pritom : measured signal-to-noise ratio per Angstrom of the used spectrum for fit
- instrument_resolution_pritom, instrument_resolution_err_pritom : measured resolution (sigma, not FWHM) and associated uncertainty of the instrument in km/s

### Columns in sl2s_sample_kinematics_pritom.csv

- Name : Name of the lens system
- Instrument : Name of the spectrograph used to collect the spectrum
- SNR : measured signal-to-noise ratio per Angstrom
- Instrument_sigma, Instrument_sigma_un : measured resolution (sigma, not FWHM) and associated uncertainty of the instrument in km/s
- BIC_weighted_sigma, BIC_weighted_stat_un, BIC_weighted_sys_un : BIC weighted average velocity dispersion, statistical and systematic uncertainty
- eq_weighted_sigma, eq_weighted_stat_un, eq_weighted_sys_un : average velocity dispersion, statistical and systematic uncertainty with equal weight on measurements from all template library

Note : Two template library was used - 'Indo-Us' and 'MILES'. Bessel correction was applied to the systematic uncertainties.

Note 5/16/25: The SL2SJ0959+0206 values in sl2s_all_params_ws.csv has been updated, as we changed the source light model from a Sersic + shapelets to Sersic + shapelets + point source. This change is in response to how dense the source galaxy core is, which we speculate could introduce fluctuation in the point-source-like images. To account for this, we add additional degrees of freedom into our model to account for these potential flux anomalies.
