<img src="https://github.com/javiserna/Periodize/blob/main/periodize_logo.png?raw=true"/>

# A perfect python repository for estimating the rotation period of light curves files


### Features
This repository uses the Lomb-Scargle periodogram to estimate the rotation period of the signal and statistical techniques for estimating the uncertainty of the period.

This repo contains three executable modes:
* (Period.py) Simple estimation of the period 
* (Periodize.py) Estimation of the period and uncertainty using the bootstrap method to resample the light curve within the flux error bars.
* (Periodize_paralelized.py) Same as the periodize.py but using multithreads, notoriously improve the computing time.

### Input requirement

* A CSV file with three columns called ("time", "magnitude or flux", "magnitude_err or flux_err").

Periodize was think to be used with the light curves files from the TESSExtractor application. So, search for the target of interest in the app and download the input file to feed Periodize.

### Output

Period and period uncertainty 

#### How to use?
Locate at the repository folder and execute in terminal:

```zsh
$ python periodize.py "input_file.csv"
```

Feel free to use this app in any scientific project!

Any question or comments just email me:
jserna@astro.unam.mx

>#### Please cite:
>
>- _Serna et al (2021)_. [ApJ 923 177](https://doi.org/10.3847/1538-4357/AC300A)
> 

Copyright© 2023.
Javier Serna, Jesús Hernandez and ARYSO group.
