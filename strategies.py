import datetime

class Strategy:
	def __init__(self, data_frame):
		self.data_frame = data_frame

	def get_bought_price(self, date):
		# TODO: 날짜를 알려줬을 떄 그 날짜 전에 구매한 가격을 리턴하게 수정해야함.
		self.bought_price

	def get_data_frame(self):
		return self.data_frame

	def has_to_buy(self, date):
		pass

	def has_to_sell(self, date):
		pass


class GcdcStrategy(Strategy):
	def __init__(self, data_frame):
		super(GcdcStrategy, self).__init__(data_frame)
		self.data_frame['ma5'] = data_frame['close'].rolling(window=5).mean()
		self.data_frame['ma20'] = data_frame['close'].rolling(window=20).mean()

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
		return (ma5_now, ma20_now, ma5_yesterday, ma20_yesterday)

	def has_to_buy(self, date):
		ma5_now, ma20_now, ma5_yesterday, ma20_yesterday = self.get_mas(date)
		if ma5_yesterday == None:
			return False
		if ma5_now > ma20_now and ma5_yesterday <= ma20_yesterday:
			self.bought_price = self.data_frame['close'][date]
			return True
		else:
			return False

	def has_to_sell(self, date):
		ma5_now, ma20_now, ma5_yesterday, ma20_yesterday = self.get_mas(date)
		if ma5_yesterday == None:
			return False
		return ma5_now < ma20_now and ma5_yesterday >= ma20_yesterday
