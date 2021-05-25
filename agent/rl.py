import random
import math

from agent.agent import Agent


class ReinforcementLearning(Agent):
    type = "RL"

    '''
    q(state, action)
    The states are:
        Each combination of owning stocks: 2 exp 10 stocks 
    
    The actions are:
        3 for each stock: buy, sell
        10 stocks
        
    The matrix is going to be 100x30
    
            c1 v1 c2 v2 c3 v3 c4 v4
        s1  0  0  0  0  0  0  0  0 
        s2  0  0  0  0  0  0  0  0 
        s3  0  0  0  0  0  0  0  0 
    '''

    def __init__(self, central_bank, initial_cash=1000):
        super().__init__(central_bank, initial_cash)
        self.current_step = 0
        self.dec = (self.epsilon - 0.1) / self.total
        self.q = []
        self.discount = 0.9
        self.total = 1000000
        self.learningRate = 0.8
        self.epsilon = 0.9
        self.rand_factor = 0.05
        self.reward_modifier = 100
        self.init_q_values()
        self.original_state = 0
        self.original_action = 0

    def init_q_values(self):
        num_lines = 2 * len(self.central_bank.get_all_stock())
        num_col = 2 ** len(self.central_bank.get_all_stock())

        for i in range(num_lines):
            tmp = [0 for _ in range(num_col)]
            self.q.append(tmp)

    def get_state(self):
        l = len(self.central_bank.get_all_stock())
        owned_stocks = set(self.stocks_owned.keys())
        s = "".join(["0" if i in owned_stocks else "1" for i in range(l)])
        return int(s, 2)

    def learn(self):
        original_state = 0
        original_action = 0
        u = self.reward(original_state, original_action)
        prev_q = self.get_q(original_state, original_action)
        pred_error = 0

        self.epsilon = max(self.epsilon - self.dec, 0.05)
        # ahead = aheadPosition(); // percept

        pred_error = u + self.discount * self.get_max_q(self.get_state()) - prev_q

        new_q = (original_state, original_action, prev_q + (self.learningRate * pred_error))
        self.q[original_state][original_action] = new_q
        return

    def _decide(self):
        self.epsilon -= self.dec
        if random.uniform(0, 1) < self.rand_factor:
            self.do_random_action(self.get_available_actions())
        else:
            act = self.do_e_greedy()
            # act = random.randint(0, 2 * len(self.central_bank.get_all_stock()))

    def get_available_actions(self):
        owned_stocks = set(self.stocks_owned.keys())
        l = len(self.central_bank.get_all_stock())

        buy_actions = [2 ** i for i in range(l) if self.central_bank.stocks[i].price <= self.cash]
        sell_actions = [2 ** i + 1 for i in range(l) if i in owned_stocks]

        return [*buy_actions, *sell_actions]

    def do_e_greedy(self):
        valid_actions = self.get_available_actions()
        if random.uniform(0, 1) < self.rand_factor:
            return self.do_random_action(valid_actions)
        state = self.get_state()
        act = self.get_max_action_q(state, valid_actions)
        self.do_action(act)
        return act

    def get_random_available_action(self):
        valid_actions = self.get_available_actions()
        action = valid_actions[random.randint(0, len(valid_actions) - 1)]
        return action

    def do_random_action(self, valid_actions):
        action = valid_actions[random.randint(0, len(valid_actions) - 1)]
        self.do_action(action)

    def do_action(self, action):
        stock_id = int(math.log(action, 2))
        if action % 2:
            #  odd, means sell
            max_sell = self.how_many_can_i_sell(stock_id)
            to_sell = random.randint(0, max_sell)
            self.sell(stock_id, to_sell)
        else:
            # even, means buy
            max_buy = self.how_many_can_i_buy(stock_id) - 1
            to_buy = random.randint(0, max_buy)
            self.buy(stock_id, to_buy)

    def reward(self, original_state, original_action):
        # usar a diff de valor da stock - ver function do report
        l = len(self.stock_history)
        current_value = self.stock_history[l - 1] + self.cash_history[l - 1]
        pre_value = self.stock_history[l - 2] + self.cash_history[l - 2]

        r = abs(current_value) - abs(pre_value)
        r *= self.reward_modifier

        return r

    def get_q(self, original_state, original_action):
        return self.q[original_state][original_action]

    def get_max_q(self, state):
        return max(self.q[state])

    def get_max_action_q(self, state, valid_actions):
        max = - float("inf")
        max_i = -1
        line = self.q[state]
        for i in range(len(valid_actions)):
            q_action = line[i]
            if q_action > max:
                max = q_action
                max_i = i
        return max_i
