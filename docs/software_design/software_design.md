risk_system/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── inputs/
│
├── docs/
│   ├── model_documentation/
│   ├── software_design/
│   ├── test_plan/
│   └── test_results/
│
├── src/
│   ├── main.py
│   ├── config.py
│   │
│   ├── data_loader/
│   │   └── loader.py
│   │
│   ├── pricing/
│   │   ├── stock_pricer.py
│   │   ├── option_pricer.py
│   │   └── greeks.py
│   │
│   ├── risk/
│   │   ├── historical_var.py
│   │   ├── parametric_var.py
│   │   ├── monte_carlo_var.py
│   │   ├── expected_shortfall.py
│   │   └── backtesting.py
│   │
│   ├── volatility/
│   │   ├── ewma.py
│   │   ├── garch.py
│   │   └── implied_vol.py
│   │
│   ├── utils/
│   │   ├── statistics.py
│   │   ├── covariance.py
│   │   └── plots.py
│   │
│   └── tests/
│       ├── test_var.py
│       ├── test_es.py
│       └── test_pricing.py
│
├── reports/
│
├── requirements.txt
└── README.md