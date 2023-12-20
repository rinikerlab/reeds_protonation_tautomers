import numpy as np
import matplotlib.pyplot as plt

from sklearn.metrics import mean_absolute_error, mean_squared_error
import scipy


from scipy.stats import pearsonr
from scipy.stats import kendalltau
from scipy.stats import spearmanr

from scipy.stats import bootstrap

def get_rel_ddGs(dgs):
    """
    Convert a list of dg values into a list (linearized matrix)
    of all possible n * (n-1) relative values (excluding self terms)
    
    """
    n = len(dgs)
    num_rel = int(n*(n-1)/2)
    ddgs = np.zeros(num_rel)
    
    beg = 0
    for i in range(n-1):
        delta = (n - (i+1))
        end = beg + delta
        ddgs[beg:end] = (dgs - dgs[i])[i+1:]
        beg = end
        
    return np.array(ddgs)

def bootstrap_metric_with_errors(fct, x_values, y_values, y_errors, p_value=False):
    bootstrapped_metric = []
    # bootstrap metric to generate test distribution
    for _ in range(1000):
        drawn_y = y_values + np.random.normal(loc=0, scale=y_errors, size = len(y_errors))
        
        if p_value:
            r = fct(x_values, drawn_y)[0]
        else:
            r = fct(x_values, drawn_y)
        bootstrapped_metric.append(r)
        
    # define 95% CI
    alpha = 5.0
    lower_p = alpha / 2.0
    # get value at or near percentile (take a look at the definition of percentile if
    # you have less than 100 values to make sure you understand what is happening)
    lower = np.percentile(bootstrapped_metric, lower_p)
    upper_p = (100 - alpha) + (alpha / 2.0)
    upper = np.percentile(bootstrapped_metric, upper_p)
    # calculate true mean
    if p_value:
        mean = fct(x_values, y_values)[0]
    else:
        mean = fct(x_values, y_values)
    return mean, lower, upper

def bootstrap_relative_rmses(x_values, y_values, y_errors, p_value=False):
    bootstrapped_metric = []
    # bootstrap metric to generate test distribution
    
    def calc_rmse(x_values, y_values):
        return np.sqrt(mean_squared_error(x_values, y_values))

    ddgs_exp = get_rel_ddGs(x_values)
    
    for _ in range(1000):
        drawn_y = y_values + np.random.normal(loc=0, scale=y_errors, size = len(y_errors))
        ddgs_drawn = get_rel_ddGs(drawn_y)
        r = calc_rmse(ddgs_exp, ddgs_drawn)
        bootstrapped_metric.append(r)
        
    # define 95% CI
    alpha = 5.0
    lower_p = alpha / 2.0
    # get value at or near percentile (take a look at the definition of percentile if
    # you have less than 100 values to make sure you understand what is happening)
    lower = np.percentile(bootstrapped_metric, lower_p)
    upper_p = (100 - alpha) + (alpha / 2.0)
    upper = np.percentile(bootstrapped_metric, upper_p)
    
    # calculate true mean
    mean = calc_rmse(ddgs_exp, get_rel_ddGs(y_values))
    return mean, lower, upper


def calculate_statistics_with_errors(x_values, y_values, y_errors, output=False):

    rmse = bootstrap_relative_rmses(x_values, y_values, y_errors,)
    
    # bootstrap MAE
    mae = bootstrap_metric_with_errors(
        mean_absolute_error, x_values, y_values, y_errors,
    )
    
    # bootstrap Pearson
    pearson = bootstrap_metric_with_errors(
        scipy.stats.pearsonr, x_values, y_values, y_errors, p_value=True
    )

    # bootstrap Spearman
    spearman = bootstrap_metric_with_errors(
        scipy.stats.spearmanr, x_values, y_values, y_errors, p_value=True
    )

    # bootstrap Kendalltau
    kendall = bootstrap_metric_with_errors(
        scipy.stats.kendalltau, x_values, y_values, y_errors, p_value=True
    )
    if output:
        print(f"RMSE: {rmse=}")
        print(f"MAE: {mae=}")
        #print(f"{pearson=}")
        print(f"Spearman: {spearman=}")
        print(f"Kendall: {kendall=}")
    return (
        tuple([float("{0:.2f}".format(n)) for n in rmse]),
        tuple([float("{0:.2f}".format(n)) for n in mae]),
        #tuple([float("{0:.2f}".format(n)) for n in pearson]),
        tuple([float("{0:.2f}".format(n)) for n in spearman]),
        tuple([float("{0:.2f}".format(n)) for n in kendall]),
    )