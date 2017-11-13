import matplotlib.pyplot as plt

#Receives a DataFrame of at least two keys and two columns
#In our case, our pie is determined with our column 'Quantity'
#Pie chart and bar chart
def charts(df):
    plt.style.use("dark_background")
    colors = ["cornflowerblue", "orangered", "gold","r","limegreen","m","b","coral","yellow"]
    fig, axes = plt.subplots(ncols = 3,figsize=(15,10))
    ax1,ax2,ax3 = axes.ravel()

    # Table
    meat = []
    for i in df['Quantity']:
        meat.append([i])
    columns = ['Quantity']
    rows = ['Asada', 'Adobada', 'Otros']
    ax3.axis('off')
    table = ax3.table(cellText=meat,
              cellColours=[['black'] * len(meat[0])] * len(meat),
              colLabels=columns,
              colColours=['black'] * len(columns),
              rowLabels=rows,
              rowColours=colors,
              loc='center')
    table.scale(.3,1.5)

    #Pie chart
    ax1.pie(
        df['Quantity'],
        labels=df['Queues'],
        shadow=False,
        colors=colors,
        startangle=90,
        autopct='%1.1f%%',
        )
    ax1.axis('equal')
    ax1.margins(1)

    #Bar chart
    length = list(range(len(df["Quantity"])))
    ax2.bar([p + .375 for p in length],
            df["Quantity"],
            0.25,
            color=colors,
            label=df["Queues"]
            )
    ax2.set_ylabel('Total')
    ax2.set_title('Tacos')
    ax2.set_xticks([p + 1.5 * 0.25 for p in length])
    ax2.set_xticklabels(df['Queues'])

    #Both charts will be printed in one space and not one for each.
    plt.xlim(min(length)-.25, max(length)+0.25*4)
    plt.ylim([0, max(df['Quantity']) + 1])
    plt.grid()
    fig.tight_layout()
    fig.subplots_adjust(hspace=100)
    plt.show()

charts(df)
