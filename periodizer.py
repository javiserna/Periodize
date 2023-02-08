import scipy
import sys
import os
import scipy.signal
import random 
import scipy.stats
#######################################
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from astropy.table import Table
from astropy.io import ascii
from scipy.interpolate import interp1d, UnivariateSpline
from scipy.signal import find_peaks_cwt
from scipy.signal import hilbert
from scipy.signal import find_peaks
from scipy.fftpack import fft,fftfreq
#from PyAstronomy.pyasl import foldAt
from scipy.interpolate import interp1d
#from PyAstronomy.pyasl import foldAt
from astropy.stats import median_absolute_deviation
import bootstrap
import scipy.optimize
from concurrent.futures import ProcessPoolExecutor


__all__ = ["robust_periodogram", "plot_periodogram"]

def robust_periodogram(time, flux, flux_err=None, periods=None, loss="linear", scale=1):

    if flux_err is None:
        flux_err = np.ones_like(flux)

    # set up period grid
    if periods is None:
        periods = _period_grid(time)

    # compute periodogram
    psd_data = _robust_regression(time, flux, flux_err, periods, loss, scale)

    # find period of highest periodogram peak
    best_period = periods[np.argmax(psd_data)]

    return {"periods": periods, "power": psd_data, "best_period": best_period}



def _period_grid(time):

    number_obs = len(time)
    length_lc = np.max(time) - np.min(time)

    dt = 2 * length_lc / number_obs
    max_period = np.rint(length_lc / dt) * dt
    min_period = dt

    periods = np.arange(min_period, max_period + dt, dt)

    return periods


def _model(beta0, x, period, t, y, dy):

    x[:, 1] = np.cos(2 * np.pi * t / period)
    x[:, 2] = np.sin(2 * np.pi * t / period)

    return (y - np.dot(x, beta0.T)) / dy


def _noise(mu, t, y, dy):

    return (mu * np.ones(len(t)) - y) / dy


def _robust_regression(time, flux, flux_err, periods, loss, scale):

    beta0 = np.array([0, 1, 0])
    mu = np.median(flux)
    x = np.ones([len(time), len(beta0)])
    chi_model = np.empty([len(periods)])
    chi_noise = np.empty([len(periods)])

    for i in range(len(periods)):
        chi_model[i] = scipy.optimize.least_squares(
            _model,
            beta0,
            loss=loss,
            f_scale=scale,
            args=(x, periods[i], time, flux, flux_err),
        ).cost
        chi_noise[i] = scipy.optimize.least_squares(
            _noise, mu, loss=loss, f_scale=scale, args=(time, flux, flux_err)
        ).cost
    power = 1 - chi_model / chi_noise

    return power


def plot_periodogram(
    time, flux, periods, power, flux_err=None, best_period=None, fap=None
):

    if flux_err is None:
        flux_err = np.zeros_like(flux)

    # set up the figure & axes for plotting
    fig = plt.figure(figsize=(16, 9))
    grid_spec = plt.GridSpec(2, 1)

    # plot the light curve
    ax = fig.add_subplot(grid_spec[0, :])
    ax.errorbar(
        time, flux, flux_err, fmt="ok", label="light curve", elinewidth=1.5, capsize=0
    )
    ax.set_xlabel("time")
    ax.set_ylabel("flux")
    ax.legend()

    # plot the periodogram
    ax = fig.add_subplot(grid_spec[1, :])
    ax.plot(periods, power, c="k", label="periodogram")
    # mark the best period and label with significance
    if best_period is not None:
        if fap is None:
            raise ValueError(
                "Must give a false alarm probability if you give a best_period"
            )

        # set precision for period format
        pre = int(abs(np.floor(np.log10(np.max(np.diff(periods))))))
        label = "Detected period p = {:.{}f} with {:.2E} FAP".format(
            best_period, pre, fap
        )
        ymax = power[periods == best_period]
        ax.axvline(best_period, ymin=0, ymax=ymax, label=label, c="r")

    ax.set_xlabel("period")
    ax.set_ylabel("power")
    ax.set_xlim(0, np.max(periods))
    ax.legend()

    return fig


if __name__ == "__main__":

	lc=pd.read_csv(sys.argv[1])
	time=lc['time']
	flux=lc['mag']
	flux_err=lc['mag_err']
	newlc=[]
	Prot=[]
	n=100 # Synthetic light curve number for Bootstrap

	for i in range(len(flux)):
		y=bootstrap.errfunction(flux[i], flux_err[i], n)
		newlc.append(y)
	newlc=np.array(newlc)
	periods = np.logspace(-1, 1.4, num=100) #100 steps in the period range. May you consider to change by 1000 in particular cases (increase the computing time).


	for j in range(n):
		periodogram = robust_periodogram(time, newlc[:,j], periods=periods)
		periodogram_curve=interp1d(periodogram['periods'], periodogram['power'])
		zper=periodogram_curve(periods)
		neg_to_pos = (np.diff(zper[1:])<=0) & (np.diff(zper[:-1])>=0)
		maxima = periods[1:-1][neg_to_pos]
		periodogram_inverse=interp1d(periodogram['power'],periodogram['periods'])
		fm=max(periodogram_curve(maxima))
		period=periodogram_inverse(fm)
		Prot.append(period) #Period array

	Prot=np.array(Prot)
	if np.std(Prot)==0:
		print(u'Period=%.2f days\n' %(np.median(Prot)))
		print("Uncertainty quite low, please consider 1000 steps for the period range!")
	if np.std(Prot)!=0:
		print(u'Period=%.2f\u00B1%.2f days' %(np.median(Prot),np.std(Prot)))

