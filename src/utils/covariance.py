import numpy as np
import pandas as pd

def covariance_matrix(returns: pd.DataFrame) -> np.ndarray:
    """
    Compute covariance matrix of asset returns.

    Parameters
    ----------
    returns : pd.DataFrame
        Rows = time, Columns = assets

    Returns
    -------
    np.ndarray
        Covariance matrix (N x N)
    """

    # Drop missing values just in case
    returns_clean = returns.dropna()

    # Convert to numpy
    data = returns_clean.values

    # Compute covariance matrix
    cov_matrix = np.cov(data, rowvar=False)

    return cov_matrix