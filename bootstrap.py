import numpy as np
import random 
import scipy.stats
from scipy.special import erfinv
import matplotlib.pyplot as plt

def errfunction(mu,sigma,points):
	x=np.zeros(points)
	for i in range(0,points):
		x[i]=mu+sigma*np.sqrt(2)*erfinv(2*(random.uniform(0,1))-1)
	output=np.array(x)
	return output


