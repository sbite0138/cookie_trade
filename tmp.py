import random
import joblib
import math
from tqdm import tqdm
# from matplotlib import pyplot as plt

from statistics import median

BANK_LEVEL = 10
DRAGON_BOOST = 1


def get_resting_val(id):
    return 10*(id+1)+BANK_LEVEL-1


class Item():
    def __init__(self, id):
        self.id = id
        self.stock = 0
        self.mode = random.choice([0, 1, 1, 2, 2, 3, 4, 5])
        self.dur = math.floor(10 + random.random() * 690)
        self.val = get_resting_val(id)
        self.d = random.random() * 0.2 - 0.1
        self.vals = [self.val, self.val - self.d]
        self.last = 0

    def tick(self):
        globD = 0
        globP = random.random()
        if (random.random() < 0.1 + 0.1 * DRAGON_BOOST):
            globD = (random.random() - 0.5) * 2
        self.last = 0
        self.d *= 0.97 + 0.01 * DRAGON_BOOST
        if (self.mode == 0):
            self.d *= 0.95
            self.d += 0.05 * (random.random() - 0.5)
        elif (self.mode == 1):
            self.d *= 0.99
            self.d += 0.05 * (random.random() - 0.1)
        elif (self.mode == 2):
            self.d *= 0.99
            self.d -= 0.05 * (random.random() - 0.1)
        elif (self.mode == 3):
            self.d += 0.15 * (random.random() - 0.1)
            self.val += random.random() * 5
        elif (self.mode == 4):
            self.d -= 0.15 * (random.random() - 0.1)
            self.val -= random.random() * 5
        elif (self.mode == 5):
            self.d += 0.3 * (random.random() - 0.5)
        self.val += (get_resting_val(self.id) - self.val) * 0.01

        if (globD != 0 and random.random() < globP):
            self.val -= (1 + self.d * math.pow(random.random(), 3) * 7) * globD
            self.val -= globD * (1 + math.pow(random.random(), 3) * 7)
            self.d += globD * (1 + random.random() * 4)
            self.dur = 0
        self.val += math.pow((random.random() - 0.5) * 2, 11) * 3
        self.d += 0.1 * (random.random() - 0.5)
        if (random.random() < 0.15):
            self.val += (random.random() - 0.5) * 3
        if (random.random() < 0.03):
            self.val += (random.random() - 0.5) * (10 + 10 * DRAGON_BOOST)
        if (random.random() < 0.1):
            self.d += (random.random() - 0.5) * (0.3 + 0.2 * DRAGON_BOOST)
        if (self.mode == 5):
            if (random.random() < 0.5):
                self.val += (random.random() - 0.5) * 10
            if (random.random() < 0.2):
                self.d = (random.random() - 0.5) * (2 + 6 * DRAGON_BOOST)
        if (self.mode == 3 and random.random() < 0.3):
            self.d += (random.random() - 0.5) * 0.1
            self.val += (random.random() - 0.7) * 10
        if (self.mode == 3 and random.random() < 0.03):
            self.mode = 4
        if (self.mode == 4 and random.random() < 0.3):
            self.d += (random.random() - 0.5) * 0.1
            self.val += (random.random() - 0.3) * 10
        if (self.val > (100 + (BANK_LEVEL - 1) * 3) and self.d > 0):
            self.d *= 0.9
        self.val += self.d

        if (self.val < 5):
            self.val += (5 - self.val) * 0.5
        if (self.val < 5 and self.d < 0):
            self.d *= 0.95
        self.val = max(self.val, 1)
        self.vals.append(self.val)
        self.dur -= 1
        if (self.dur <= 0):
            self.dur = math.floor(10 + random.random() *
                                  (690 - 200 * DRAGON_BOOST))
            if (random.random() < DRAGON_BOOST and random.random() < 0.5):
                self.mode = 5
            elif (random.random() < 0.7 and (self.mode == 3 or self.mode == 4)):
                self.mode = 5
            else:
                self.mode = random.choice([0, 1, 1, 2, 2, 3, 4, 5])


def simurate_trade(item_id, buy_price, sell_price):
    item = Item(item_id)
    max_tick = 1000
    have_stock = False
    profit = 0
    broker_num = 95
    for i in range(max_tick):
        item.tick()
        if item.val <= buy_price and have_stock == False:
            profit -= item.val + item.val * (0.2*(0.95**broker_num))
            have_stock = True
        elif item.val >= sell_price and have_stock == True:
            profit += item.val
            have_stock = False
        print(item.val, buy_price, sell_price, profit +
              item.val if have_stock else profit, have_stock)
    profit += item.val if have_stock else 0
    return profit


def evaluate_param(item_id, buy_price, sell_price):
    profits = []
    # for i in range(1000):
    #     profit = simurate_trade(item_id, buy_price, sell_price)
    #     profits.append(profit)
    profit = simurate_trade(item_id, buy_price, sell_price)
    print(profit)


evaluate_param(0, 100, 5)
