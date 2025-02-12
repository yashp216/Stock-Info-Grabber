from backtesting import Backtest, Strategy
from backtesting.lib import crossover

from backtesting.test import GOOG


class SmaCross(Strategy):
    n1 = 10
    n2 = 20

    def init(self):
        close = self.data.Close
        self.sma1 = self.I(SMA, close, self.n1)
        self.sma2 = self.I(SMA, close, self.n2)

    def next(self):
    #Ai will return a 0 or 1 : 0 for buy : 1 for sell
    #Ai will also return a 
        if crossover(self.sma1, self.sma2):
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.sell()


bt = Backtest(GOOG, SmaCross,
              cash=100000, commission=.002,
              exclusive_orders=True)

output = bt.run()
bt.plot()