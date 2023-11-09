from typing import List
import numpy as np
import pandas as pd
import datetime as dt
from finance_testing.input.portfolio import Portfolio

from finance_testing.models import Model


class GeometricBownienMotion(Model):
    """Parent Model for the Geometrical Brownien Motion

    Need to use Child method in order to chose how calculate the drift and the volatility

    Args:
        Model (_type_): _description_
    """
    def __init__(
        self,
        ptf: Portfolio,
        time_horizon: List[int],
        nb_sims: int = 1000,
        name: str = "Geometric Brownien Motion",
    ):
        super().__init__(ptf, time_horizon, nb_sims, name)

    def calculate_return(self):
        time_stamp = len(self.date_range)
        #mean vector
        mu = self.get_mu()
        #volatility vector
        sigma = self.get_simga()
        #Standard Brownien motion (to shock the volatility)
        T = self.time_horizon
        nb_assets = len(self.assets)
        times = np.linspace(0, T, time_stamp)
        dt = times[1] - times[0]
        np.random.seed(777)
        db = np.sqrt(dt) * np.random.normal(size=(time_stamp, nb_assets))
        B0 = np.zeros(shape=(1, nb_assets))
        B = np.concatenate((B0, db), axis=0)
        #nota bene : not returns but didn't find proper name
        daily_return = []
        for t in range(time_stamp):
            exp = (mu-sigma**2/2)*t + sigma * B[t]
            # We add a "-1" because in the simulation we add 1
            daily_return.append(list(np.exp(exp)-1))
        print(daily_return[1])
        return daily_return

    def get_mu(self) -> np.array:
        """to be define in the child model
        (mean vector)
        """
        pass

    def get_simga(self) -> np.array:
        """to be define ine the child model
        WARNING : not the covariance matrix, the volatility vector !
        """

class GeometricBrownienMotionStatic(GeometricBownienMotion):
    """We supposed in this model that the drift and the volatility used in GBM is static
     and calculted historically
    """
    def __init__(self, ptf: Portfolio, time_horizon: List[int], nb_sims: int = 1000, name: str = "Geometric Brownien Motion Static"):
        super().__init__(ptf, time_horizon, nb_sims, name)

    def get_mu(self) -> np.array:
        return np.array(self.ptf.mean_return)

    def get_simga(self) -> np.array:
        return np.array(self.ptf.cov_mat).diagonal()