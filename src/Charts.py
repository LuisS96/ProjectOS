import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import pandas as pd
from classes import *


def charts(answersList, StatsDict):
    asada_time = []
    adobada_time = []
    others_time = []
    asadaTacos = StatsDict['Total_Asada']
    adobadaTacos = StatsDict['Total_Adobada']
    othersTacos = StatsDict['Total_Others']
    asada_amount_average = asadaTacos/StatsDict['Total_AsOrders']
    adobada_amount_average = asadaTacos/StatsDict['Total_AdOrders']
    others_amount_average = asadaTacos/StatsDict['Total_OtOrders']
    asada_step_average = StatsDict['Steps_Asada']/StatsDict['Total_AsOrders']
    adobada_step_average = StatsDict['Steps_Adobada']/StatsDict['Total_AdOrders']
    others_step_average = StatsDict['Steps_Others']/StatsDict['Total_OtOrders']
    print(asada_step_average)
    print(adobada_step_average)
    print(others_step_average)
    #for answer in answersList:
     #   for suborder in answer.order.subordersList:
      #      if suborder.meat == 'Asada':
       #         asada_time.append((suborder.endTime - suborder.startTime).total_seconds())
        #    elif suborder.meat == 'Adobada':
         #       adobada_time.append((suborder.endTime - suborder.startTime).total_seconds())
          #  else:
           #     others_time.append((suborder.endTime - suborder.startTime).total_seconds())

    raw_data_pie = {"Order": ['Asada', 'Adobada', 'Others'], "Average amount of tacos per order":
        [asada_amount_average,adobada_amount_average,others_amount_average]}
    df_pie = pd.DataFrame(raw_data_pie, columns=['Order', 'Average amount of tacos per order'])

    raw_data_pie2 = {"Order": ['Asada', 'Adobada', 'Others'], "Number of suborders":
        [StatsDict['Total_AsOrders'],StatsDict['Total_AdOrders'],StatsDict['Total_OtOrders']]}
    df_pie2 = pd.DataFrame(raw_data_pie2, columns=['Order', 'Number of suborders'])

    raw_data_bar = {"Order": ['Asada', 'Adobada', 'Others'], "Amount of tacos": [asadaTacos, adobadaTacos, othersTacos]}
    df_bar = pd.DataFrame(raw_data_bar, columns=['Order', 'Amount of tacos'])


    raw_data_bar2 = {"Order": ['Asada', 'Adobada', 'Others'], "Steps": [asada_step_average,adobada_step_average,others_step_average]}
    df_bar2 = pd.DataFrame(raw_data_bar2, columns=['Order','Steps'])
    # raw_data_plot = {'Meat Type':['Asada','Adobada','Others'],
    #                  'Time Spent': [asada_time, adobada_time, others_time]}

    plt.style.use("dark_background")
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', 'grey', 'gold', '#17becf']
    # grid = GridSpec(1,3)

    fig, axes = plt.subplots(ncols=3, figsize=(15, 10))
    ax1, ax2, ax3 = axes.ravel()

    # Table
    orders = [asada_amount_average,adobada_amount_average,others_amount_average]
    #for answer in answersList:
       # orders.append([answer.order.Id, (answer.order.endTime - answer.order.startTime).total_seconds()])
    columns = ["Order", 'Average amount of tacos per order']
    rows = [range(len(orders))]
    ax1.axis('off')
    table = ax1.table(cellText=orders,
              cellColours=[['black'] * len(str(orders[0]))] * len(orders),
              colLabels=columns,
              colColours=['black'] * len(columns),
              rowLabels=rows,
              rowColours=colors,
              loc='center',)
    table.set_fontsize(25)
    table.scale(1,1.5)

    # Pie chart
    # Amount of time each order took to make
    ax2.pie(
        df_pie['Average amount of tacos per order'],
        labels=df_pie['Order'],
        shadow=False,
        colors=colors,
        startangle=90,
        autopct='%1.1f%%',
        )
    ax2.axis('equal')
    ax2.margins(1)


    # Bar chart
    # Amount of tacos each order has
    length = list(range(len(df_bar['Amount of tacos'])))
    ax3.bar([p + .375 for p in length],
            df_bar['Amount of tacos'],
            0.25,
            color=colors,
            label=df_bar["Order"]
            )
    plt.tight_layout()

    fig, axes = plt.subplots(ncols=2, figsize=(10, 10))
    ax4,ax5 = axes.ravel()

    # Plot chart
    # Amount of time each suborder took to make
    ax4.pie(
        df_pie2['Number of suborders'],
        labels=df_pie['Order'],
        shadow=False,
        colors=colors,
        startangle=90,
        autopct='%1.1f%%',
        )
    ax4.axis('equal')
    ax4.margins(1)

    # Bar chart 2
    # 
    length = list(range(len(df_bar2['Steps'])))
    ax5.bar([p + .375 for p in length],
            df_bar2['Steps'],
            0.25,
            color=colors,
            label=df_bar2["Order"]
            )
    plt.tight_layout()

    plt.show()


