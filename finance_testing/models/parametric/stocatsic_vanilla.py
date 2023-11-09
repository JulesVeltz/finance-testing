import numpy as np

from finance_testing.models import Model


class StocaticVanilla(Model):
    def calculate_return(self):
        T = self.time_horizon
        nb_assets = len(self.assets)
        times = np.linspace(0, T, self.nb_days * T)
        dt = times[1] - times[0]
        np.random.seed(777)
        db = np.sqrt(dt) * np.random.normal(size=(self.nb_days * T, nb_assets))
        B0 = np.zeros(shape=(1, nb_assets))
        b = np.concatenate((B0, db), axis=0)
        return {asset: b[:, i] for i, asset in enumerate(self.assets)}
