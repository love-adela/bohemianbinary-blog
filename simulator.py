import pandas as pd
import strategies

class Simulator:
    def __init__(self, strategy):
        self.data_frame = strategy.get_data_frame()
        benefits = []
        drawdowns = []
        bought = False
        max_benefit = -1

        index = self.data_frame['close'].keys()

        for date in index:
            close_price = self.data_frame['close'][date]

            order_type, benefit = strategy.has_order(date)

            if order_type == strategies.OrderType.buy:
                bought = True
                if len(benefits) == 0:
                    benefits.append(1)
                else:
                    benefits.append(benefits[-1])
            elif order_type == strategies.OrderType.sell:
                bought = False
                benefits.append(benefits[-1] * (close_price / strategy.get_previous_price(date)))
            elif order_type == strategies.OrderType.day_trade:
                if len(benefits) == 0:
                    benefits.append(benefit)                    
                else:
                    benefits.append(benefits[-1] * benefit)
            else:
                if len(benefits) == 0:
                    benefits.append(1)
                elif bought:
                    benefits.append(benefits[-1] * (close_price / strategy.get_previous_price(date)))
                else:
                    benefits.append(benefits[-1])

            if benefits[-1] > max_benefit:
                max_benefit = benefits[-1]

            drawdowns.append(1 - (benefits[-1] / max_benefit))

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
