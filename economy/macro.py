from functools import lru_cache

import numpy as np
import pandas as pd
import statsmodels.api as sm

from .services import get_fred_series


ACTIVITY_SERIES = {
    "IPMAN": "Manufacturing Production",
    "W875RX1": "Real Personal Income",
    "CMRMTSPL": "Manufacturing & Trade Sales",
    "PAYEMS": "Nonfarm Payrolls",
}


INFLATION_SERIES = {
    "CPIAUCSL": "Headline CPI",
    "CPILFESL": "Core CPI",
    "PCEPI": "PCE Price Index",
    "WPSFD4131": "Core Finished Goods PPI",
}


def _load_monthly_panel(series_map, start="1975-01-01"):
    series = {}

    for fred_id, name in series_map.items():
        df = get_fred_series(fred_id)

        s = df.set_index("date")["value"]
        s = s.loc[start:]

        # Normalize all dates to monthly timestamps
        s.index = s.index.to_period("M").to_timestamp()
        s = s.groupby(level=0).last()

        series[name] = s

    return pd.DataFrame(series).dropna()


def _fit_factor(panel, orientation_series):
    # Monthly percentage log changes
    growth = np.log(panel).diff() * 100
    growth = growth.dropna()

    standardized = (
        growth - growth.mean()
    ) / growth.std(ddof=0)

    model = sm.tsa.DynamicFactor(
        standardized,
        k_factors=1,
        factor_order=2,
        error_order=1,
        error_cov_type="diagonal",
    )

    result = model.fit(
        disp=False,
        maxiter=500,
    )

    factor = pd.Series(
        result.factors.filtered[0],
        index=standardized.index,
    )

    # Factor sign is arbitrary mathematically.
    # Make positive values mean stronger activity/inflation.
    if factor.corr(standardized[orientation_series]) < 0:
        factor *= -1

    factor = (
        factor - factor.mean()
    ) / factor.std(ddof=0)

    return factor, standardized


@lru_cache(maxsize=1)
def get_activity_factor():
    panel = _load_monthly_panel(
        ACTIVITY_SERIES,
        start="1975-01-01",
    )

    factor, components = _fit_factor(
        panel,
        orientation_series="Manufacturing Production",
    )

    factor.name = "Macro Activity Factor"

    return factor, components


@lru_cache(maxsize=1)
def get_inflation_factor():
    panel = _load_monthly_panel(
        INFLATION_SERIES,
        start="1975-01-01",
    )

    factor, components = _fit_factor(
        panel,
        orientation_series="Core CPI",
    )

    factor.name = "Inflation Pressure Factor"

    return factor, components