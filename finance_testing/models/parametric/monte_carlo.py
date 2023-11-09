from typing import List
import numpy as np
import pandas as pd
import datetime as dt
from finance_testing.input.portfolio import Portfolio

from finance_testing.models import Model


class MonteCarlo(Model):
    """ In this model we suppose that the return of each stock follow a Multivariate Normal Law
 And we use Monte Carlo Simulation in order to use the "Theorem central limite"
    Args:
        Model (_type_): _description_
    """
    def __init__(
        self,
        ptf: Portfolio,
        time_horizon: List[int],
        nb_sims: int = 1000,
        name: str = "Monte Carlo",
    ):
        super().__init__(ptf, time_horizon, nb_sims, name)

    def calculate_return(self):
        time_stamp = len(self.date_range)
        returns = self.ptf.mean_return
        sigma = self.ptf.cov_mat
        mu = np.full(shape=(time_stamp, len(self.assets)), fill_value=returns)
        daily_returns = []
        for _ in range(self.nb_sims):
            z = np.random.normal(size=(time_stamp, len(self.assets)))
            l = np.linalg.cholesky(sigma)
            daily_returns.append(mu.T + l @ z.T)
        print(daily_returns[1])
        return daily_returns
