<img src="https://github.com/javiserna/Periodize/blob/main/periodizer_logo.png?raw=true"/>

# A perfect python repository for estimating the rotation period of light curve files


### Features
This repository uses the Lomb-Scargle periodogram to estimate the rotation period of the signal and statistical techniques for estimating the uncertainty of the period.

This repo contains three executable modules:
* (Period.py) Simple estimation of the period 
* (Periodizer.py) Estimation of the period and uncertainty using the bootstrap method to resample the light curve within the flux error bars.
* (Periodizer_parallelized.py) Same as the periodize.py but using multithreads, notoriously improve the computing time.

### Input requirement

* A CSV file with three columns called: "time", "magnitude or flux", "magnitude_err or flux_err".

Periodizer was made to be used with the light curves files from the TESSExtractor application. However, that is not a  prerequisite, it really could be used with any data file in the format previously described. 
A straightforward way to search the light curve of the target of interest is by using the app TESSExtractor and downloading the input file to feed Periodizer.

### Output

The period and its uncertainty

#### How to use?
Locate at the repository folder and execute in terminal the module you desire:

```zsh
$ python period.py "input_file.csv"

$ python periodizer.py "input_file.csv"

$ python periodizer_parallelized.py "input_file.csv"

```

Feel free to use this app in any scientific project!

Any question or comments just email me:
jserna@astro.unam.mx

>#### Please cite:
>
>- Serna et al (2021) [ApJ 923 177](https://doi.org/10.3847/1538-4357/AC300A)
> 

Copyright© 2023.
Javier Serna, Jesús Hernandez and ARYSO group.
