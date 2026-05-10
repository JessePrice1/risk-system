import numpy as np
import pandas as pd

from src.utils.covariance import covariance_matrix


# ---------------------------------------------------
# Generate sample returns data
# ---------------------------------------------------

np.random.seed(42)

returns_df = pd.DataFrame({
    "AAPL": np.random.normal(0, 0.02, 100),
    "MSFT": np.random.normal(0, 0.015, 100),
    "TSLA": np.random.normal(0, 0.03, 100)
})


# ---------------------------------------------------
# Test 1 — Symmetry Test
# ---------------------------------------------------

cov_matrix = covariance_matrix(returns_df)

symmetry_error = np.max(np.abs(cov_matrix - cov_matrix.T))

print("TEST 1 — Symmetry Test")
print(f"Maximum symmetry error: {symmetry_error:.12f}")

if symmetry_error < 1e-8:
    print("PASS: Covariance matrix is symmetric.\n")
else:
    print("FAIL: Covariance matrix is not symmetric.\n")


# ---------------------------------------------------
# Test 2 — Benchmark Accuracy
# ---------------------------------------------------

cov_numpy = np.cov(returns_df.dropna().values, rowvar=False)

max_difference = np.max(np.abs(cov_matrix - cov_numpy))

print("TEST 2 — Benchmark Accuracy")
print(f"Maximum difference vs NumPy: {max_difference:.12f}")

if max_difference < 1e-10:
    print("PASS: Covariance matches NumPy benchmark.\n")
else:
    print("FAIL: Covariance differs from benchmark.\n")


# ---------------------------------------------------
# Test 3 — Positive Semi-Definite Check
# ---------------------------------------------------

eigenvalues = np.linalg.eigvals(cov_matrix)

min_eigenvalue = np.min(eigenvalues)

print("TEST 3 — Positive Semi-Definite Check")
print(f"Minimum eigenvalue: {min_eigenvalue:.12f}")

if min_eigenvalue >= -1e-10:
    print("PASS: Covariance matrix is positive semi-definite.\n")
else:
    print("FAIL: Covariance matrix is not PSD.\n")


# ---------------------------------------------------
# Test 4 — Missing Data Robustness
# ---------------------------------------------------

returns_nan = returns_df.copy()

returns_nan.iloc[0, 0] = np.nan
returns_nan.iloc[5, 2] = np.nan

print("TEST 4 — Missing Data Robustness")

try:
    cov_nan = covariance_matrix(returns_nan)

    if np.any(np.isnan(cov_nan)) or np.any(np.isinf(cov_nan)):
        print("FAIL: Output contains NaN or infinite values.\n")
    else:
        print("PASS: Missing data handled successfully.\n")

except Exception as e:
    print(f"FAIL: Runtime error occurred: {e}\n")