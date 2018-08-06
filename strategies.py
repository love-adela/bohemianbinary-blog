import datetime
import enum
import copy
import coin_repository


class OrderType(enum.Enum):
    buy = 1
    sell = 2
    day_trade = 3


class Strategy:
    def __init__(self, repository, end_date=None, duration=365):
        if end_date is None:
            self.end_date = datetime.datetime.now()
        self.data_frame = copy.deepcopy(repository.get_data_frame(end_date, duration))

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
    def __init__(self, repository, end_date=None, duration=365):
        if self.end_date is None:
            self.end_date = datetime.datetime.now()
        super(GcdcStrategy, self).__init__(repository, end_date, duration)
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
    def __init__(self, repository, end_date=None, duration=365, k_value=0.5, k_factor=1):
        if self.end_date is None:
            self.end_date = datetime.datetime.now()
        super(VolatilityBreakoutStrategy, self).__init__(repository, end_date, duration)
        self.k_value = k_value
        self.ks = []
        self.k_factor = k_factor

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
        if self.k_value == -1:
            body_length = abs(yesterday_close_price - yesterday_open_price)
            self.ks.append(1 - (body_length / gap))
            if len(self.ks) > self.k_factor:
                self.ks.pop(0)
            k_value = sum(self.ks) / float(len(self.ks))
        else:
            k_value = self.k_value

        target_gap = gap * k_value
        target_price = open_price + target_gap
        if target_price > high_price:
            return None, None
        
        return OrderType.day_trade, close_price / target_price


if __name__ == "__main__":
    # print("hello")
    a = VolatilityBreakoutStrategy(coin_repository.CoinRepository('ETH'), 0.5)
    a.get_prices(datetime.date(2018, 6, 6))
    print(a.get_prices(datetime.date(2018, 6, 6)))
    print(a.has_order(datetime.date(2018, 6, 6)))
