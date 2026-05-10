"""
Configuration defaults for the risk system.
"""

# Default parameters
DEFAULT_CONFIDENCE = 0.99
DEFAULT_HORIZON_DAYS = 10  # Basel standard
DEFAULT_N_SIM = 50000
DEFAULT_RISK_FREE_RATE = 0.05

# Market regimes for testing
REGIMES = {
    "Dot-com Crash":     ("2000-03-01", "2002-10-01"),
    "GFC 2008":          ("2007-10-01", "2009-03-31"),
    "Post-GFC Recovery": ("2009-04-01", "2011-12-31"),
    "Normal (2017-19)":  ("2017-01-01", "2019-12-31"),
    "COVID Crash":       ("2020-02-01", "2020-06-30"),
    "Rate Hikes 22-23":  ("2022-01-01", "2023-12-31"),
}

# EWMA
EWMA_LAMBDA = 0.94  # RiskMetrics standard
