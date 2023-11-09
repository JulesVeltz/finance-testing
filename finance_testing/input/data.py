from typing import List
import datetime as dt
import numpy as np
import pandas as pd
import requests_cache
import pandas_datareader.data as web


class Data:
    """class where we searching for the data needed
    """
    def __init__(
        self, assets: List[str], source: str = "", business_days: bool = True
    ) -> None:
        self.assets = assets
        self.source = source
        self.business_days = business_days
        self.days = None
        self.prices = None

    def get_data(self):
        """retrieve data for the computation

        Args:
            self.assets (List[float]): list of the self.assets we are looking for
            online (bool, optional): if we looking online or simuating the data. Defaults to True.

        Returns:
            _type_: _description_
        """
        # for now only with pandas_reader
        if self.source != "excel":
            end_date = dt.datetime.now()
            # depends on data source (but generally we gonna have only business days)
            # TODO: voir quelle periode prendre pour calculer mu et Sigma
            start_date = end_date - dt.timedelta(days=5 * 365)
            # retrieve data
            expire_after = dt.timedelta(days=1)
            session = requests_cache.CachedSession(
                cache_name="cache", backend="sqlite", expire_after=expire_after
            )
            stock_data = web.DataReader(
                self.assets, self.source, start_date, end_date, session=session
            )["Close"].reset_index()
            time = pd.date_range(start=start_date, end=end_date)
            # sort data
            stock_data = stock_data.sort_values(by="Date").set_index("Date")
            stock_data = stock_data.reindex(index=time, method="ffill")
            self.prices = stock_data
            returns = stock_data.pct_change()
            mean_returns = returns.mean()
            cov_mat = returns.cov()
        else:
            np.random.seed(777)
            returns = pd.DataFrame(
                np.random.normal(
                    loc=0.01, scale=1, size=(5*365, len(self.assets))
                )
                / 1e2,
                columns=self.assets,
            )
            mean_returns = returns.mean()
            cov_mat = returns.cov()
        return mean_returns, cov_mat
