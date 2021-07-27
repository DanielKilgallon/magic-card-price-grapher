import plotly.graph_objects as go
import csv

header = []
data = []

card_name = 'Toralf'

with open('output.csv', mode ='r') as file:
    csvFile = csv.reader(file)
    first_line = True
    for line in csvFile:
        if first_line:
            first_line = False
            for header_spot in range(2, len(line)):
                header.append(line[header_spot])
        for spot in range(1, len(line)):
            if card_name in line[spot]:
                data = line[2:len(line)]
                found_card_name = line[spot]

fig = go.Figure()
fig.add_trace(go.Scatter(x=header, y=[float(i) for i in data], name=found_card_name, hovertemplate = '%{y:$.2f}<extra></extra>'))
fig.update_layout(
    title=found_card_name,
    xaxis_title="Date",
    yaxis_title="Price",
    hoverlabel=dict(
        bgcolor="blue",
        bordercolor="white",
        font_size=24,
        font_family="Arial"
    )
)
fig.update_yaxes(showspikes=True)
fig.show()