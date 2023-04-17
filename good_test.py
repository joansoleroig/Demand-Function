import random
from variable_demand_with_marketing import demand_function

#lists we must provide:
deliveries=[random.randint(50, 100) for _ in range(50)]
qualities=[random.randint(50, 100) for _ in range(50)]
prices=[]
marketing=[]
#generate marketing with 90% of sales without marketing but 10% with marketing:
for i in range(50):
    if random.random() < 0.85:
        marketing.append(0)
    else:
        marketing.append(100)
#generate price increase after 10 sales of +1$ on the price:
num = 20
for i in range(50):
    prices.append(num)
    if (i+1) % 10 == 0:
        num += 1
demand_function(qualities, deliveries, prices, marketing)

