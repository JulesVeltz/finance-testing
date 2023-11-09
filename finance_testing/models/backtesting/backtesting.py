from typing import Dict
from finance_testing.models import Model


class Backtest(Model):
    def __init__(self, ptf: Dict[str, float], look_back_period: int):
        self.look_back_period = look_back_period
        self.ptf = ptf

    def calculate_return(self):
        pass
        # TODO
