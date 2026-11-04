"""Data collection: Ken French international factors, ETF total returns, USD factor.

Every series is returned as monthly decimal returns indexed by ``pd.Period`` (freq ``M``),
in USD. Downloads are cached in ``data/cache`` so the notebook reruns offline and is
reproducible; pass ``refresh=True`` to re-download.
"""
from __future__ import annotations

import io
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import requests

CACHE = Path(__file__).resolve().parent.parent / "data" / "cache"
FRENCH_URL = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/{}_CSV.zip"
FRED_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={}"
USD_SERIES = "DTWEXBGS"  # Nominal Broad U.S. Dollar Index (Fed H.10), daily, from 2006

REGIONS = ["Developed", "Developed_ex_US", "Europe", "Japan",
           "Asia_Pacific_ex_Japan", "North_America", "Emerging"]

# ticker -> (description, Ken French region whose factors are the "local" model)
ETFS = {
    "EFA": ("MSCI EAFE (developed ex US & Canada)", "Developed_ex_US"),
    "VGK": ("FTSE Developed Europe", "Europe"),
    "EWJ": ("MSCI Japan", "Japan"),
    "EPP": ("MSCI Pacific ex Japan", "Asia_Pacific_ex_Japan"),
    "EEM": ("MSCI Emerging Markets", "Emerging"),
    "EWZ": ("MSCI Brazil", "Emerging"),
}


def _download(url: str, cache_name: str, refresh: bool = False) -> bytes:
    """GET ``url`` with an on-disk cache. Raises on HTTP errors or empty bodies."""
    path = CACHE / cache_name
    if path.exists() and not refresh:
        return path.read_bytes()
    try:
        r = requests.get(url, timeout=60, headers={"User-Agent": "intl-factor-lab/1.0"})
        r.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Download failed for {url}: {e}") from e
    if not r.content:
        raise RuntimeError(f"Empty response from {url}")
    CACHE.mkdir(parents=True, exist_ok=True)
    path.write_bytes(r.content)
    return r.content


def parse_french_csv(text: str) -> pd.DataFrame:
    """Parse the *monthly* block of a Ken French CSV into decimal returns.

    The files hold a text preamble, a header line starting with ',' and YYYYMM rows,
    then an annual block. Values are percent; -99.99 marks missing data.
    """
    lines = text.splitlines()
    try:
        h = next(i for i, line in enumerate(lines) if line.strip().startswith(","))
    except StopIteration:
        raise ValueError("No header row found in Ken French file") from None
    columns = [c.strip() for c in lines[h].split(",")[1:]]
    rows = []
    for line in lines[h + 1:]:
        cells = [c.strip() for c in line.split(",")]
        if len(cells[0]) != 6 or not cells[0].isdigit():
            break  # blank line or start of the annual block
        rows.append(cells)
    if not rows:
        raise ValueError("No monthly rows found in Ken French file")
    df = pd.DataFrame([r[1:] for r in rows], columns=columns, dtype=float)
    df.index = pd.to_datetime([r[0] for r in rows], format="%Y%m").to_period("M")
    return df.replace(-99.99, np.nan) / 100


def _french_file(name: str, refresh: bool) -> pd.DataFrame:
    raw = _download(FRENCH_URL.format(name), f"{name}.zip", refresh)
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        text = z.read(z.namelist()[0]).decode("latin-1")
    return parse_french_csv(text)


def french_factors(region: str, refresh: bool = False) -> pd.DataFrame:
    """Fama-French 5 factors + momentum (MOM) + RF for one region, decimals, USD."""
    if region not in REGIONS:
        raise ValueError(f"Unknown region {region!r}; choose from {REGIONS}")
    five = _french_file(f"{region}_5_Factors", refresh)
    mom = _french_file(f"{region}_Mom_Factor", refresh)
    mom.columns = ["MOM"]  # French names it WML
    return five.join(mom, how="inner")


def _drop_partial_month(s: pd.DataFrame | pd.Series) -> pd.DataFrame | pd.Series:
    """Drop the current calendar month: its month-end value is not final yet."""
    return s[s.index < pd.Timestamp.today().to_period("M")]


def _closes(tickers: list[str], start: str, refresh: bool) -> pd.DataFrame:
    """Daily adjusted closes (total return) from Yahoo, cached per ticker set."""
    import yfinance as yf  # imported lazily: only needed when not cached

    path = CACHE / f"etf_close_{'_'.join(sorted(tickers))}.csv"
    if path.exists() and not refresh:
        close = pd.read_csv(path, index_col=0, parse_dates=True)
    else:
        close = yf.download(tickers, start=start, auto_adjust=True,
                            progress=False)["Close"]
        if close.empty:
            raise RuntimeError(f"yfinance returned no prices for {tickers}")
        close = close.dropna(how="all")
        CACHE.mkdir(parents=True, exist_ok=True)
        close.to_csv(path)
    missing = set(tickers) - set(close.columns)
    if missing:
        raise RuntimeError(f"No price data for {sorted(missing)}")
    return close[tickers]


def etf_returns(tickers: list[str], start: str = "2005-01-01",
                refresh: bool = False) -> pd.DataFrame:
    """Monthly total returns (dividends reinvested via Yahoo adjusted close)."""
    monthly = _closes(tickers, start, refresh).resample("ME").last()
    # fill_method=None: never invent returns across gaps or before inception
    rets = monthly.pct_change(fill_method=None)
    rets.index = rets.index.to_period("M")
    return _drop_partial_month(rets).iloc[1:]


def last_day_returns(ticker: str = "SPY", start: str = "2005-01-01",
                     refresh: bool = False) -> pd.Series:
    """Daily return of ``ticker`` on each month's last trading day.

    Proxy for US-hours news that arrives after Asian/European markets have closed: the
    US-listed ETF prices it this month, the local factor only next month."""
    daily = _closes([ticker], start, refresh)[ticker].pct_change(fill_method=None)
    last = daily.groupby(daily.index.to_period("M")).last()
    return _drop_partial_month(last).dropna().rename(f"{ticker}_last_day")


def usd_factor(refresh: bool = False) -> pd.Series:
    """Monthly % change of the broad trade-weighted dollar (positive = USD stronger).

    Non-traded factor: it captures currency translation risk for a USD investor, but
    its coefficient is a sensitivity, not a priced premium (alpha stays comparable only
    within models that include it).
    """
    raw = _download(FRED_URL.format(USD_SERIES), f"{USD_SERIES}.csv", refresh)
    s = pd.read_csv(io.BytesIO(raw), index_col=0, parse_dates=True,
                    na_values=".").iloc[:, 0]
    m = s.resample("ME").last().pct_change(fill_method=None)
    m.index = m.index.to_period("M")
    return _drop_partial_month(m).dropna().rename("USD")


def load_all(etfs: dict = ETFS, start: str = "2005-01-01",
             refresh: bool = False) -> tuple[pd.DataFrame, dict, pd.Series]:
    """Returns (etf_returns, {region: factors}, usd). Always includes 'Developed'
    as the global benchmark model."""
    rets = etf_returns(list(etfs), start, refresh)
    regions = sorted({region for _, region in etfs.values()} | {"Developed"})
    factors = {r: french_factors(r, refresh) for r in regions}
    return rets, factors, usd_factor(refresh)
