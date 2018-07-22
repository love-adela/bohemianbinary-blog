import datetime
import enum
import copy

class OrderType(enum.Enum):
    buy = 1
    sell = 2
    day_trade = 3

class Strategy:
    def __init__(self, repository):
        self.data_frame = copy.deepcopy(repository.get_data_frame())

    def get_previous_price(self, date):
        yesterday = date + datetime.timedelta(days=-1)
        if yesterday < self.data_frame['close'].keys()[0]:
            return False
        return self.data_frame['close'][yesterday]

    def get_data_frame(self):
        return self.data_frame

    def has_order(self, data):
        pass

    def has_to_buy(self, date):
        pass

    def has_to_sell(self, date):
        pass


class GcdcStrategy(Strategy):
    def __init__(self, repository):
        super(GcdcStrategy, self).__init__(repository)
        self.data_frame['ma5'] = self.data_frame['close'].rolling(window=5).mean()
        self.data_frame['ma20'] = self.data_frame['close'].rolling(window=20).mean()

    def get_mas(self, date):
        ma5_now = self.data_frame['ma5'][date]
        ma20_now = self.data_frame['ma20'][date]
        yesterday = date + datetime.timedelta(days=-1)
        if yesterday < self.data_frame['close'].keys()[0]:
            ma5_yesterday = None
            ma20_yesterday = None
        else:
            ma5_yesterday = self.data_frame['ma5'][yesterday]
            ma20_yesterday = self.data_frame['ma20'][yesterday]
        return ma5_now, ma20_now, ma5_yesterday, ma20_yesterday
    
    def has_order(self, date):
        ma5_now, ma20_now, ma5_yesterday, ma20_yesterday = self.get_mas(date)

        if ma5_yesterday is None:
            return None, None
        elif ma5_now > ma20_now and ma5_yesterday <= ma20_yesterday:
            return OrderType.buy, None
        elif ma5_now < ma20_now and ma5_yesterday >= ma20_yesterday:
            return OrderType.buy, None
        else:
            return None, None

class VolatilityBreakoutStrategy(Strategy):
    def __init__(self, repository, k_value=0.5):
        super(VolatilityBreakoutStrategy, self).__init__(repository)
        self.k_value = k_value
    
    def get_prices(self, date):
        yesterday = date + datetime.timedelta(days=-1)
        if yesterday < self.data_frame['close'].keys()[0]:
            return None, None, None, None, None, None, None

        yesterday_open_price = self.data_frame['open'][yesterday]
        yesterday_close_price = self.data_frame['close'][yesterday]
        yesterday_high_price = self.data_frame['high'][yesterday]               
        yesterday_low_price = self.data_frame['low'][yesterday]

        open_price = self.data_frame['open'][date]
        close_price = self.data_frame['close'][date]
        high_price = self.data_frame['high'][date]

        return yesterday_open_price, yesterday_close_price, \
            yesterday_high_price, yesterday_low_price, open_price, \
            close_price, high_price                 

    def has_order(self, date):
        yesterday_open_price, yesterday_close_price, \
            yesterday_high_price, yesterday_low_price, open_price, \
            close_price, high_price = self.get_prices(date)

        if yesterday_open_price is None:
            return None, None
        
        gap = yesterday_high_price - yesterday_low_price
        target_gap = gap * self.k_value
        target_price = open_price + target_gap

        if target_price > high_price:
            return None, None
        
        return OrderType.day_trade, close_price / target_price

    def noise_proportion(self):
        if k_value < -1:
            k_value = 1 - abs(open-close)/(high-low)
            return k_value
        else:     

