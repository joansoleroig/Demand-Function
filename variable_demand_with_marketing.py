def demand_function(qualities, deliveries, prices, marketing):
    import pandas as pd
    import matplotlib.pyplot as plt

    deliveriesm=[]
    for i in deliveries:
        if bool(deliveriesm): #The list is not empty
            deliverymean=(i+sum(deliveriesm))/(len(deliveriesm)+1)
        else:
            deliverymean=i
        deliveriesm.append(deliverymean)
    qualitiesm=[]
    for i in qualities:
        if bool(qualitiesm): #The list is not empty
            qualitymean=(i+sum(qualitiesm))/(len(qualitiesm)+1)
        else:
            qualitymean=i
        qualitiesm.append(qualitymean)

    total_marketing_expenditure=[]
    suma_marketing=0
    for expenses in marketing:
        suma_marketing += expenses
        total_marketing_expenditure.append(suma_marketing)
    print('total marketing expenditure',total_marketing_expenditure,'\n',len(total_marketing_expenditure))



    #Conversion to a dataframe:
    data = {'Price' : prices,
            'Quality' : qualities,
            'Quality mean' : qualitiesm,
            'Delivery' : deliveries,
            'Delivery mean' : deliveriesm,
            'Marketing' : marketing,
            'Total Marketing Expenditure' : total_marketing_expenditure,
    }

    df_data = pd.DataFrame(data)
    ############### WEIGHTED AVERAGES
    # weighted average of quality:
    df_data['Qualities Weigh Avg']=df_data['Quality'].rolling(window=8).mean()

    # Weighted average of delivery:
    df_data['Deliveries Weigh Avg']=df_data['Delivery'].rolling(window=8).mean()
    print(df_data.to_string())
    # print weighted averages
    plt.figure(figsize=(10, 5))
    plt.plot(df_data['Quality mean'], '#ffc37a', label='Quality mean')
    plt.plot(df_data['Qualities Weigh Avg'], '#ff8c00', label='Qualities weighted average')
    plt.plot(df_data['Delivery mean'], '#ff6ed1', label='Deliveries mean')
    plt.plot(df_data['Deliveries Weigh Avg'], '#d60093', label='Deliveries weighted average')
    plt.ylabel('Quality and deliveries in %')
    plt.xlabel('Sales order nº')
    plt.grid(linestyle=':')
    plt.title('Qualities, deliveries & weighted averages')
    plt.fill_between(df_data['Quality mean'].index, df_data['Qualities Weigh Avg'], df_data['Quality mean'], where=df_data['Qualities Weigh Avg'] > df_data['Quality mean'], color='#ff8c00', alpha=0.1)
    plt.fill_between(df_data['Delivery mean'].index, df_data['Deliveries Weigh Avg'], df_data['Delivery mean'], where=df_data['Deliveries Weigh Avg'] > df_data['Delivery mean'], color='#d60093', alpha=0.1)
    plt.legend(loc='upper left')
    plt.show()



    ####################
    #Demand function with variability
    def demand(preus, quality, on_time_deliveries,total_marketing_expenditure):
        # Define the coefficients for each input
        price_coeff = -2
        quality_coeff = 0.1
        on_time_coeff = 0.1
        price_change_coeff = 0.25
        marketing_coeff = 0.03
        initialdemand=20
        premium=0
        #Si estem a la 1a sale:
        if n==0:
            demand= 20
        #Si no estem a la 1a sale:
        else:
            #Si no hem canviat el preu de l'última sale respecte la penúltima sale:
            if df_data['Price'].iloc[n] == df_data['Price'].iloc[n-1]:
                #Si ja portem més de 8 sale orders, la demand tindrà en compte la ponderació de les últimes 8 qualities i deliverie sales respecte la mitjana:
                if n>8:
                    #Si hem fet les últimes 8 sales amb millor qualitat que la mitjana o millor delivery rate que la mitjana:
                    if df_data['Qualities Weigh Avg'].iloc[n] >= df_data['Quality mean'].iloc[n] or df_data['Deliveries Weigh Avg'].iloc[n] >= df_data['Delivery mean'].iloc[n]:
                        premium=premium+0.05
                        # Si hem fet les últimes 8 sales amb millor qualitat que la mitjana i millor delivery rate que la mitjana:
                        if df_data['Qualities Weigh Avg'].iloc[n] >= df_data['Quality mean'].iloc[n] and df_data['Deliveries Weigh Avg'].iloc[n] >= df_data['Delivery mean'].iloc[n]:
                            premium = premium + 0.05
                    #Si no hem fet ni les últimes 8 sales amb millor qualitat que la mitjana ni millor delivery rate que la mitjana i o les últimes 8 deliveries en % son <80% o les últimes 8 qualities son <80%:
                    elif (df_data['Qualities Weigh Avg'].iloc[n] >= df_data['Quality mean'].iloc[n] and df_data['Deliveries Weigh Avg'].iloc[n] >= df_data['Delivery mean'].iloc[n]) and (df_data['Qualities Weigh Avg'].iloc[n] < 80 or df_data['Deliveries Weigh Avg'].iloc[n] < 80):
                        premium = premium - 0.05
                    demand = initialdemand*(1+premium) + (price_coeff * (preus - 20) + quality_coeff * (df_data['Qualities Weigh Avg'].iloc[n] - 50) + on_time_coeff * (df_data['Deliveries Weigh Avg'].iloc[n]- 50))+total_marketing_expenditure*marketing_coeff
                #Si estem a les primeres 8, la demand function no tindrà en compte la ponderació de les últimes 8 sinó la última sale respecte la mitjana global.
                else:
                    demand = initialdemand*(1+premium) + (price_coeff * (preus - 20) + quality_coeff * (df_data['Quality mean'].iloc[n] - 50) + on_time_coeff * (df_data['Delivery mean'].iloc[n]- 50))+total_marketing_expenditure*marketing_coeff

            #Si hem canviat el preu:    Ara ens afecten 2 coses: canvi de preu (short-term) & preu més alt (long-term) a part de tot lo d'abans
            else:
                #Si ja portem + de 8 sales:
                if n>8:
                    #Si hem fet les últimes 8 sales amb millor qualitat que la mitjana o millor delivery rate que la mitjana:
                    if df_data['Qualities Weigh Avg'].iloc[n] >= df_data['Quality mean'].iloc[n] or df_data['Deliveries Weigh Avg'].iloc[n] >= df_data['Delivery mean'].iloc[n]:
                        premium = premium + 0.05
                        # Si hem fet les últimes 8 sales amb millor qualitat que la mitjana i millor delivery rate que la mitjana:
                        if df_data['Qualities Weigh Avg'].iloc[n] >= df_data['Quality mean'].iloc[n] and df_data['Deliveries Weigh Avg'].iloc[n] >= df_data['Delivery mean'].iloc[n]:
                            premium = premium + 0.05
                        # Si no hem fet ni les últimes 8 sales amb millor qualitat que la mitjana ni millor delivery rate que la mitjana i o les últimes 8 deliveries en % son <80% o les últimes 8 qualities son <80%:
                    elif (df_data['Qualities Weigh Avg'].iloc[n] >= df_data['Quality mean'].iloc[n] and df_data['Deliveries Weigh Avg'].iloc[n] >= df_data['Delivery mean'].iloc[n]) and (df_data['Qualities Weigh Avg'].iloc[n] < 80 or df_data['Deliveries Weigh Avg'].iloc[n] < 80):
                        premium = premium -0.05
                    demand = initialdemand*(1-price_change_coeff*(preus/df_data['Price'].iloc[n-1]))*(1+premium) + (price_coeff * (preus -20) + quality_coeff *(df_data['Qualities Weigh Avg'].iloc[n]-50) + on_time_coeff * (df_data['Deliveries Weigh Avg'].iloc[n]-50))+total_marketing_expenditure*marketing_coeff
                #Si estem a les primeres 8 sales:
                else:
                    demand = initialdemand*(1-price_change_coeff*(preus/df_data['Price'].iloc[n-1]))*(1+premium) + (price_coeff * (preus -20) + quality_coeff *(df_data['Quality mean'].iloc[n]-50) + on_time_coeff * (df_data['Delivery mean'].iloc[n]-50))+total_marketing_expenditure*marketing_coeff
        return round(demand)
        #print('demand',n,demand)


#    print('Dataframe: ', '\n', df_data.head(10),'\n')
#    print('Maximum values in general', '\n', df_data.max(),'\n')

    demand_list=[]
    n=0
    for preus in df_data['Price']:
        current_demand = demand(preus, df_data['Quality'].iloc[n],df_data['Delivery'].iloc[n],df_data['Total Marketing Expenditure'].iloc[n])
        demand_list.append(current_demand)
        n = n + 1
    pd.set_option("display.max_columns", 0)
    df_data['Current Demand']=demand_list
    #print('df_data',df_data)





    ############### PLOT DEMAND AS FUNCTION OF EVERYTHING
    fig,ax=plt.subplots()
    ax.plot(df_data['Qualities Weigh Avg'], '#ff8c00', label='Qualities weighted average')
    ax.plot(df_data['Quality mean'], '#ffb04f', label='Quality mean')
    ax.plot(df_data['Deliveries Weigh Avg'], '#be06cf', label='Deliveries weighted average')
    ax.plot(df_data['Delivery mean'], '#f585ff', label='Delivery mean')

    ax.set_ylabel('Quality and deliveries in %')
    ax.set_xlabel('Sales order nº')
    ax.grid(linestyle=':')
    ax.set_title('Qualities, deliveries & weighted averages')
    ax.fill_between(df_data['Quality mean'].index, df_data['Qualities Weigh Avg'], df_data['Quality mean'],where=df_data['Qualities Weigh Avg']>df_data['Quality mean'], color='#ff8c00', alpha=0.1)
    ax.fill_between(df_data['Delivery mean'].index, df_data['Deliveries Weigh Avg'], df_data['Delivery mean'],where=df_data['Deliveries Weigh Avg']>df_data['Delivery mean'], color='#be06cf', alpha=0.1)
    ax.legend(loc='upper left')
    # twin object for two different y-axis on the sample plot
    ax2=ax.twinx()
    # make a plot with different y-axis using second axis object
    ax2.plot(df_data['Price'],color="blue",marker="o", label='Price')
    ax2.plot(df_data['Current Demand'], '#008000', label='Current demand')
    ax2.legend(loc='upper right')

    ax2.set_ylabel('Current Price and current demand')
    # ax2.set_ylabel('Current demand',color="#008000",fontsize=14)
    plt.show()


    ######### REVENUE
    df_data['Revenue'] = df_data['Current Demand'] * df_data['Price']
    df_data['Normalised Revenue'] = df_data['Current Demand'] * df_data['Price']/20
    df_data['Normalised Marketing Expenditure'] = df_data['Total Marketing Expenditure']/15
#    print(df_data)
    fig, ax = plt.subplots()
    ax.plot(df_data['Qualities Weigh Avg'], '#ff8c00', label='Qualities weighted average')
    ax.plot(df_data['Quality mean'], '#ffb04f', label='Quality mean')
    ax.plot(df_data['Deliveries Weigh Avg'], '#be06cf', label='Deliveries weighted average')
    ax.plot(df_data['Delivery mean'], '#f585ff', label='Delivery mean')

    ax.set_ylabel('Quality and deliveries in %')
    ax.set_xlabel('Sales order nº')
    ax.grid(linestyle=':')
    ax.set_title('Qualities, deliveries & weighted averages')
    ax.fill_between(df_data['Quality mean'].index, df_data['Qualities Weigh Avg'], df_data['Quality mean'],
                    where=df_data['Qualities Weigh Avg'] > df_data['Quality mean'], color='#ff8c00', alpha=0.1)
    ax.fill_between(df_data['Delivery mean'].index, df_data['Deliveries Weigh Avg'], df_data['Delivery mean'],
                    where=df_data['Deliveries Weigh Avg'] > df_data['Delivery mean'], color='#be06cf', alpha=0.1)
    ax.legend(loc='upper left')
    # twin object for two different y-axis on the sample plot
    ax2 = ax.twinx()
    # make a plot with different y-axis using second axis object
    ax2.plot(df_data['Price'], color="blue", marker="o", label='Price')
    ax2.plot(df_data['Current Demand'], '#008000', label='Current demand')
    ax2.plot(df_data['Normalised Revenue'], '#70faa1', label='Normalised Renevue = Revenue/20')
    ax2.plot(df_data['Normalised Marketing Expenditure'], '#98F5FF', label='Normalised Marketing Expenditure = Marketing Expenditure/15')
    ax2.legend(loc='upper right')

    ax2.set_ylabel('Current Price, Current Demand & Current Revenue/20 & Marketing Expeniture/15')
    plt.show()
    print(df_data)

