import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import webbrowser
import pymysql
import pandas as pd
import mpld3

conn = pymysql.connect(host='localhost', port=3306, user='root', password='', database='meteringdatabase')
c = conn.cursor()
sql = "SELECT end_time, PW FROM uetcl0102 WHERE month = 'September' AND date = '22/09/2020'"
time = []
power = []
c.execute(sql)
data = c.fetchall()
for row in data:
    time.append(row[0])
    power.append(float(row[1]))
max_DD = max(power)
min_DD = min(power)
#print(max_DD)
max_DD_time = power.index(max_DD)
min_DD_time = power.index(min_DD)
#print(max_DD_time)
#print(time[max_DD_time])
max_DD1 = "{:,}".format(max_DD)
min_DD1 = "{:,}".format(min_DD)

#df1 = pd.DataFrame(time)
#df1.columns = ['time']
#df2 = pd.DataFrame(power)
#df2.columns = ['power']
#df = pd.concat([df1,df2], axis=1)
#df.head()
#print(df)
conn.commit()
c.close()
conn.close()

fig = go.Figure(
    data=[go.Line(y=power, x=time)],
    #layout_title_text="Load Profile for Meter"

)
fig.update_layout(
    #title="Plot Title",
    xaxis_title="Time/Hrs",
    yaxis_title="Power/kW",
font=dict(
        family="Tahoma, sans-serif",
        size=15,
        color="#7f7f7f"
        #bold = True
    )

)

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Meter Load Profile',style={'color':'green','textAlign': 'center'}),

    html.Div(children='''
        Powered by UETCL-EMIS
    ''',style={'textAlign': 'center'}),


    dcc.Graph(
        id='graph',
        figure=fig
    ),
html.H2(children=f'The Maximum Demand is: {max_DD1} kW at {time[max_DD_time]} Hours',style={'textAlign': 'center'}),
html.H2(children=f'The Minimum Demand is: {min_DD1} kW at {time[min_DD_time]} Hours',style={'textAlign': 'center'}),
])
#fig.show()

if __name__ == "__main__":
    app.run_server(debug=True,use_reloader=True)

#webbrowser.open('http://127.0.0.1:8050/')



#fig.show()



