from typing import List
import datetime as dt
import pandas as pd
from finance_testing.input.portfolio import Portfolio


class Model:
    def __init__(
        self,
        ptf: Portfolio,
        time_horizon: List[int],
        nb_sims: int = 100,
        name: str = "base model",
    ):
        self.name = name
        self.assets = ptf.asset
        self.ptf = ptf
        self.time_horizon = max(time_horizon)
        self.liste_time_horizon = time_horizon
        self.nb_sims = nb_sims
        self.date_range = self.calculate_date_range()

    def calculate_return(self):
        """to calculate the returns (based on the different model)"""
        pass

    def calculate_date_range(self):
        """def date range used by the model"""
        start_date = dt.datetime.now()
        timestamp = self.time_horizon * 365
        end_date = start_date + dt.timedelta(days=timestamp)
        return pd.date_range(start=start_date, end=end_date)
