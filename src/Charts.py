import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import pandas as pd
from classes import *


def charts(answersList):
    asada_time = []
    adobada_time = []
    others_time = []
    asadaTacos = 0
    adobadaTacos = 0
    othersTacos = 0
    for answer in answersList:
        for suborder in answer.order.subordersList:
            if suborder.meat == 'Asada':
                asada_time.append((suborder.endTime - suborder.startTime).total_seconds())
                asadaTacos += suborder.qty
            elif suborder.meat == 'Adobada':
                adobada_time.append((suborder.endTime - suborder.startTime).total_seconds())
                adobadaTacos += suborder.qty
            else:
                others_time.append((suborder.endTime - suborder.startTime).total_seconds())
                othersTacos += suborder.qty

    raw_data_pie = {"Order": [answer.order.Id for answer in answersList], "Time of completion":
        [(answer.order.endTime-answer.order.startTime).total_seconds() for answer in answersList]}
    df_pie = pd.DataFrame(raw_data_pie, columns=['Order', 'Time of completion'])
    print(df_pie)

    raw_data_bar = {"Order": ['Asada', 'Adobada', 'Others'], "Amount of tacos": [asadaTacos, adobadaTacos, othersTacos]}
    df_bar = pd.DataFrame(raw_data_bar, columns=['Order', 'Amount of tacos'])
    print(df_bar)

    # raw_data_plot = {'Meat Type':['Asada','Adobada','Others'],
    #                  'Time Spent': [asada_time, adobada_time, others_time]}

    plt.style.use("dark_background")
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', 'grey', 'gold', '#17becf']
    # grid = GridSpec(1,3)

    fig, axes = plt.subplots(ncols=3, figsize=(15, 10))
    ax1, ax2, ax3 = axes.ravel()

    # Table
    orders = []
    for answer in answersList:
        orders.append([answer.order.Id, (answer.order.endTime - answer.order.startTime).total_seconds()])
    columns = ["Order", 'Time of completion']
    rows = [index for index in range(len(answersList))]
    ax1.axis('off')
    table = ax1.table(cellText=orders,
              cellColours=[['black'] * len(orders[0])] * len(orders),
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
        df_pie['Time of completion'],
        # labels=df_pie['Order'],
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
    ax4.plot(asada_time, 'bo-', label='Asada')
    ax4.plot(adobada_time, 'go-', label='Adobada')
    ax4.plot(others_time, 'ro-', label='Others')

    plt.tight_layout()

    plt.show()
