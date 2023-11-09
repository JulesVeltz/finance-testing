import sys
import os

sys.path.append(os.path.join(os.path.realpath(os.path.dirname(__file__)), "../"))

from finance_testing.simulation import Simulation
from finance_testing.models.parametric.geometric_brownien_motion import GeometricBrownienMotionStatic
from finance_testing.models.parametric.monte_carlo import MonteCarlo
from finance_testing.input.portfolio import Portfolio

ptf = Portfolio(asset=['^DJI', 'TSLA', 'TSCO.UK'], quantity=[100, 25 , 25])


# def test_monte_carlo():
test_sto = MonteCarlo(ptf=ptf,time_horizon=[2,5],
                        nb_sims=2)

# result_simu = Simulation(ptf=ptf,list_model=[test_sto]).simulate(display=False,
                                                    # display_type="return")

test_gbm = GeometricBrownienMotionStatic(ptf=ptf,
                                         time_horizon=[2,5],
                                         nb_sims=3)
result_simu = Simulation(ptf=ptf,list_model=[test_sto]).simulate(display=True,
                                                                 display_type="AUM")
