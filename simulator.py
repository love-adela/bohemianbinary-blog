import pandas as pd


class Simulator:
    def __init__(self, strategy):
        self.data_frame = strategy.get_data_frame()
        benefits = []
        drawdowns = []
        bought = False
        max_close = -1

        index = self.data_frame['close'].keys()

        for date in index:
            close_price = self.data_frame['close'][date]

            if strategy.has_to_buy(date):
                bought = True
                if len(benefits) == 0:
                    benefits.append(1)
                else:
                    benefits.append(benefits[-1])
            elif strategy.has_to_sell(date):
                bought = False
                benefits.append(benefits[-1] * (close_price / strategy.get_previous_price(date)))
            else:
                if len(benefits) == 0:
                    benefits.append(1)
                elif bought:
                    benefits.append(benefits[-1] * (close_price / strategy.get_previous_price(date)))
                else:
                    benefits.append(benefits[-1])

            if close_price > max_close:
                max_close = close_price

            drawdowns.append(1 - (close_price / max_close))

        self.mdd = max(drawdowns)
        self.cagr = benefits[-1] - 1
        self.data_frame['benefit'] = pd.Series(benefits, index)
        self.data_frame['drawdown'] = pd.Series(drawdowns, index)

    def get_data_frame(self):
        return self.data_frame

    def get_mdd(self):
        return self.mdd

    def get_cagr(self):
        return self.cagr
