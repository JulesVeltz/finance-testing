from typing import List
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm

from finance_testing.input.portfolio import Portfolio
from finance_testing.models import Model


class Simulation:
    def __init__(self, ptf: Portfolio, list_model: List[Model]) -> None:
        self.list_model = list_model
        self.ptf = ptf
        self.quantile = {"défavorable": 0.2,
                         "meduim": 0.5,
                         "favorable": 0.9}
        self.display = False

    def process(self):
        """process some calculation needed for the simulation
        """
        maxi = 0
        for model in self.list_model:
            max_local = model.time_horizon
            if maxi < max_local:
                self.ptf.set_max_horizon(max_horizon=max_local)
        self.ptf.process()

    def life_ptf(self, model: Model, returns, store=False):
        """Function that simulate the life of one ptf

        Args:
            returns (_type_): returns simulated by the framework
            store (bool, optional): if the aum calated need to be stored (for display). Defaults to False.

        Returns:
            liste_returns: return only the return of the ptf for the time horizon requested
            liste_aum : all the state (only if store == True)
        """
        liste_rdt, liste_aum = [], []
        nb_points = len(model.date_range)
        for step in range(nb_points):
            if step != 0:
                price_t = (1 + np.sum(returns[:, :step], axis=1)) * self.ptf.price_0
            else:
                price_t = self.ptf.price_0
            aum = np.sum(price_t * self.ptf.quantity)
            if store:
                liste_aum.append(aum)
            if step + 1 in np.array(model.liste_time_horizon) * 365:
                liste_rdt.append((aum - self.ptf.aum) / self.ptf.aum)
        return liste_rdt, liste_aum

    def loop_all_simu(self, model: Model):
        """If the framework use more than one simulation, loop on all the simulations done

        Returns:
            liste_returns: return only the return of the ptf for the time horizon requested
            liste_aum : all the state (only if store == True)
        """
        all_returns = model.calculate_return()
        all_liste_return, all_liste_aum = [], []
        for i in tqdm(range(model.nb_sims)):
            liste_return, liste_aum = self.life_ptf(
                returns=all_returns[i], model=model, store=self.display
            )
            all_liste_return.append(liste_return)
            all_liste_aum.append(liste_aum)
        return all_liste_return, all_liste_aum

    def prompt(self, liste_aum, model: Model, display_type: str) -> None:
        """to prompt with plt.plot the simulation of the ptf

        Args:
            liste_aum (List[liste_aum]): list of the list of the aum
        """
        # TODO: check comment faire si qu'une seule
        for aum_simu in liste_aum:
            if display_type == "AUM":
                plt.plot(model.date_range, aum_simu)
            elif display_type == "return":
                returns = (np.array(aum_simu) - np.array(aum_simu[0])) / np.array(
                    aum_simu[0]
                )
                plt.plot(model.date_range, returns)
        plt.xlabel("time")
        plt.ylabel(display_type)
        plt.title("Simulations for the portfolio")
        plt.show()

    def simulate(self, display=False, display_type="AUM"):
        """main function to make a simulation

        Args:
            display (bool, optional): to draw each simulation on a plt.plot. Defaults to False.
            display_type (str, optional): "returns" or "AUM". Defaults to "AUM".

        """
        df_final = pd.DataFrame()
        self.process()
        self.display = display
        for model in self.list_model:
            all_returns, all_aum = self.loop_all_simu(model=model)
            if display:
                self.prompt(liste_aum=all_aum, model=model, display_type=display_type)
            df_returns = pd.DataFrame(all_returns, columns=model.liste_time_horizon)
            for quant in self.quantile.values():
                df_q = df_returns.quantile(q=quant, interpolation="nearest")
                df_final = pd.concat([df_final, df_q], axis=1)
            df_final.columns = self.quantile.keys()
            df_final["model"] = model.name
        return df_final
