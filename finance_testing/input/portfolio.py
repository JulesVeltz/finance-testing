from typing import List
import numpy as np

from finance_testing.input.data import Data


class Portfolio:
    def __init__(
        self,
        asset: List[str],
        quantity: List[float],
        source: str = "stooq",
        name: str = "",
    ) -> None:
        self.name = name
        self.asset = asset
        self.quantity = np.array(quantity)
        self.price_0 = None
        self.data = Data(assets=asset, source=source)
        self.mean_return = None
        self.cov_mat = None
        self.aum = 0
        self.max_horizon = 0

    def process(self):
        """process some calulcation (aum) for the simulation
        """
        self.mean_return, self.cov_mat = self.data.get_data()
        self.price_0 = np.array(self.data.prices.iloc[0])
        self.aum = self.price_0 @ self.quantity.T

    def set_max_horizon(self, max_horizon: int) -> None:
        """set time_stamp (aka the total number of step for the simulation)"""
        self.max_horizon = max_horizon

