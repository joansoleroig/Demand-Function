import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


def demand(price, quality, on_time_deliveries):
    # Define the coefficients for each input
    price_coeff = -0.5
    quality_coeff = 0.1        #bona=0.05
    on_time_coeff = 0.1       #bona=0.05
    initial_price = 50
    initial_demand = 20
    # Calculate the demand using the coefficients and input values
    demand = initial_demand + (price_coeff * (price - initial_price) + quality_coeff *(quality-50) + on_time_coeff * (on_time_deliveries-50))
    #demand=round(demand)        #venem robots sencers no mitjos robots
    return demand

possible_prices=list(range(30,71))
possible_deliveries=list(range(0,101))
possible_qualities=list(range(0,101))

demanda=[]
revenue=[]
n=0
e=0
j=0
llista_preus=[]
llista_qualitats=[]
llista_deliveries=[]
llista_revenue=[]
for i in possible_prices:           #Simulating all possible values
    for e in possible_qualities:
        for j in possible_deliveries:
            demandanova=demand(possible_prices[n],possible_qualities[e],possible_deliveries[j])
            demandanova=round(demandanova)
            demanda.append(demandanova)
            revenue.append(demandanova*possible_prices[n])
            llista_preus.append(i)
            llista_qualitats.append(e)
            llista_deliveries.append(j)
            j=j+1
        e=e+1
    n=n+1

data_changing_all = {'Demand': demanda,
        'Price': llista_preus,
        'Revenue': revenue,
        'Quality': llista_qualitats,
        'Delivery': llista_deliveries
}

df_data_changing_all = pd.DataFrame(data_changing_all)
print('Dataframe: ', df_data_changing_all.head(10),'\n')
print('Maximum values in general', '\n', df_data_changing_all.max(),'\n')
print('Maximum demand when: ','\n',df_data_changing_all[df_data_changing_all.Demand == df_data_changing_all.Demand.max()],'\n')
print('Maximum revenue when: ','\n',df_data_changing_all[df_data_changing_all.Revenue == df_data_changing_all.Revenue.max()],'\n')
print(df_data_changing_all.tail())



################### PLOTS

#3D Demand as function of the 3 vars.
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(df_data_changing_all['Price'], df_data_changing_all['Quality'], df_data_changing_all['Delivery'], c=df_data_changing_all['Demand'], cmap='viridis')


# Setting up the axis
ax.set_xlabel('Price ($)')
ax.set_ylabel('Quality (%)')
ax.set_zlabel('Delivery (%)')
plt.title('Demand as function of 3 variables')
# Add a colorbar legend for the demand values
cbar = plt.colorbar(ax.collections[0])
cbar.ax.set_ylabel('Demand')
plt.show()

# Revenue as a function of demand
df_data_changing_all.plot(x='Demand',y='Revenue')
plt.title('Revenue by demand level')

#Max revenue as a function of demand
dictionary_demands=df_data_changing_all.groupby(['Demand'])['Revenue'].max().to_dict()
x = list(dictionary_demands.keys())
print(x)
y = list(dictionary_demands.values())
print(y)
ymax=max(y)
print('ymax: ',ymax)
xpos=y.index(ymax)
print('xpos:', xpos)
xmax = x[xpos]
print('xmax: ', xmax)
line, = ax.plot(x, y)

print(ymax, xpos, xmax)
a=plt.plot(x,y)
# plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True
plt.legend(['Revenue', 'Max Revenue'])
plt.xlabel('Demand')
plt.ylabel('Revenue ($)')
plt.title('Maximum Revenue by Demand Level')
plt.annotate((xmax, ymax), xy=(xmax, ymax), xytext=(xmax + 10, ymax ), arrowprops=dict(facecolor='green'),)


plt.show()