# Source: https://github.com/aloctavodia/Doing_bayesian_data_analysis

import numpy as np

def calc_min_interval(x, alpha):
    """ Internal method to determine the minimum interval of a given width. 
    Assumes that x is sorted numpy array.
    """
    
    n = len(x)
    cred_mass = 1.0 - alpha
    
    interval_idx_inc = int(np.floor(cred_mass * n))
    n_intervals = n - interval_idx_inc
    interval_width = x[interval_idx_inc:] - x[:n_intervals]
    
    if len(interval_width) == 0:
        raise ValueError('Too few elements for interval calculation')
        
    min_idx = np.argmin(interval_width)
    hdi_min = x[min_idx]
    hdi_max = x[min_idx + interval_idx_inc]
    return hdi_min, hdi_max
    
    
def hdp(x, alpha = 0.05):
    '''Calculate Highest Posterior Density (HDP) of an array for given alpha.
    The HDP is the minimum width Bayesian Credible Interval (BCI).
    Arguments:
        X : Numpy array (An array containing MCMC samples)
        alpha : float (Desired probability of type-I error)
    '''
    
    # Make a copy of trace
    x = x.copy()
    
    # for multi-variate node
    if x.ndim > 1:
        # Transpose first, then sort
        tx = np.transpose(x, list(range(x.ndim))[1:] + [0])
        dims = np.shape(tx)
        # Container list for intervals
        intervals = np.resize(0.0, dims[:-1] + (2,))
        
        for index in make_indices(dims[:-1]):
            try:
                index = tuple(index)
            except TypeError:
                pass
            
            # Sort trace
            sx = np.sort(tx[index])
            # Append to list
            intervals[index] = calc_min_interval(sx, alpha)
            
        # Transpose back before returning
        return np.array(intervals)
    else:
        # Sort univariate node
        sx = np.sort(x)
        
        return np.array(calc_min_interval(sx, alpha))