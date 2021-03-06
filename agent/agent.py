import sys
import random
from collections import defaultdict


class Agent:
    def __init__(self, central_bank, initial_cash=1000):
        self.cash = initial_cash
        self.cash_history = [initial_cash]
        self.stock_history = [0]
        self.central_bank = central_bank
        self.value_history = [initial_cash]

        self.stocks_owned = defaultdict(lambda: 0)  # id stock : qtd owned, when accessing a key not present adds that key with value 0

    def __repr__(self):
        return "Agent"

    # value is cash value + each stock owned value
    def get_value(self):
        value = self.cash
        value += self.get_stock_value()
        return value

    def get_stock_value(self):
        stock_value = 0
        for stock_id in self.stocks_owned.keys():
            stock_value += self.central_bank.get_stock(stock_id).price * self.stocks_owned[stock_id]
        return stock_value

    def get_cash_value(self):
        return self.cash

    def get_stocks_owned(self):
        return self.stocks_owned

    def get_stocks_owned_by_id(self, id):
        return self.stocks_owned[id]

    def get_stocks_owned_by_id_price(self, id):
        return self.central_bank.stock_price(id, self.get_stocks_owned_by_id(id))

    # agents will be able to use the following to make decisions
    # TO BUY
    # 1 - global news events
    # 2 - if share price is up or down
    # 3 - share price evolution throughout n rounds
    # 4 - dividends if we see it fit
    # Evaluate current portfolio
    #  - evaluate each share owned
    def decide(self):
        self._decide()
        self.__update_history()

    def buy(self, stock_id, qtd):
        cost = self.central_bank.stock_price(stock_id, qtd)
        if not self.__can_buy(cost):
            return
        if not self.central_bank.buy_stock(stock_id, qtd):
            return
        self.stocks_owned[stock_id] += qtd
        self.cash -= cost

    def sell(self, stock_id, qtd):
        if not self.__can_sell(stock_id, qtd):
            return
        value = self.central_bank.sell_stock(stock_id, qtd)
        self.stocks_owned[stock_id] -= qtd
        self.cash += value

    def how_many_can_i_buy(self, stock_id):
        cost = self.central_bank.stock_price(stock_id, 1)
        if cost <= 0:
            return 0
        return min(100, self.cash // cost)

    def how_many_can_i_sell(self, stock_id):
        return self.stocks_owned[stock_id]

    def buy_random_stock(self):
        all_stock = self.central_bank.get_all_stock()

        # get random stock
        s = random.choice(all_stock)

        # compute random amount to buy
        amount_to_buy = self.how_many_can_i_buy(s.id) - 1
        if amount_to_buy <= 0:
            return
        amount_to_buy = random.randrange(amount_to_buy)
        self.buy(s.id, amount_to_buy)
        return 0

    def sell_random_stock(self):
        if len(self.stocks_owned) == 0:
            return
        # get random stock
        s_id = random.choice(list(self.stocks_owned.keys()))

        # compute random amount to buy
        amount_to_sell = self.stocks_owned[s_id]
        if amount_to_sell <= 0:
            return
        amount_to_sell = random.randrange(amount_to_sell)
        self.sell(s_id, amount_to_sell)
        return 0

    def __can_buy(self, c):
        return self.cash >= c

    def __can_sell(self, id, qtd):
        return self.stocks_owned[id] >= qtd  # if not present will be 0 >= qtd, and false, what we want

    def __update_history(self):
        self.stock_history.append(self.get_stock_value())
        self.cash_history.append(self.cash)
        self.value_history.append(self.cash + self.get_stock_value())


class RandomAgent(Agent):
    type = "Random"

    def _decide(self):
        if random.random() < 0.08:
            self.buy_random_stock()
            self.sell_random_stock()

    def _update_history(self):
        return
