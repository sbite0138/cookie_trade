from matplotlib import pyplot as plt
import csv

with open('out', 'r') as file:
    reader = csv.reader(file)
    csv_data = list(reader)

best_buy_price = {}
best_sell_price = {}
best_profit = {}
for d in csv_data:
    print(d)
    id, buy_price, sell_price, profit = d[0].split(' ')
    id = int(id)
    buy_price = int(buy_price)
    sell_price = int(sell_price)
    profit = float(profit)
    if id not in best_profit:
        best_profit[id] = profit
        best_buy_price[id] = buy_price
        best_sell_price[id] = sell_price
    elif profit > best_profit[id]:
        best_profit[id] = profit
        best_buy_price[id] = buy_price
        best_sell_price[id] = sell_price
best_profit_sum = 0
for id in best_profit:
    print(id, best_buy_price[id], best_sell_price[id], best_profit[id])
    best_profit_sum += best_profit[id]
print(best_profit_sum)
data = {}
for d in csv_data[1:]:
    # print(d)
    id, buy_price, sell_price, profit = d[0].split(' ')
    id = int(id)
    buy_price = int(buy_price)
    sell_price = int(sell_price)
    profit = float(profit)
    if id not in data:
        data[id] = [[0 for _ in range(40)] for __ in range(40)]
    data[id][buy_price//5][sell_price//5] = profit

# # put the data into single plot

for id in data:
    plt.imshow(data[id], cmap='hot', interpolation='nearest')
    # bigger image size
    # plt.figure(figsize=(10, 10))
    plt.savefig(f'item_{id}.png')
