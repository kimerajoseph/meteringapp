import pandas as pd
import pymysql
import math
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input,Output
from datetime import datetime,date
#import datetime
import plotly.express as px

#now = datetime.today().date().__format__('%m,%d,%Y')
conn = pymysql.connect(host='localhost', port=3306, user='root', password='', database='meteringdatabase')
c = conn.cursor
df_2 = pd.read_sql(sql="select date,end_time, PW, P_var FROM uetcl0102_load_profile", con=conn)
df_2.reset_index(inplace=False)
#print(df_2)
data = []
date_list = df_2["end_time"].tolist()
date_list1 = []

#changing date format
date_listx = df_2['date'].tolist()
#print(date_listx)
dattt = []
for item in date_listx:
    itemm = item.replace('/','-')
    new_itemm = str(itemm).split('-')
    #print(new_itemm)
    #if len(new_itemm)== 3:
    if len(new_itemm[0])==1:
        itemmm = new_itemm[0].zfill(2)
        new_date_f = f"{new_itemm[2]}-{new_itemm[1]}-{itemmm}"
        #print(new_date_f)
        dattt.append(new_date_f)

    else:
        new_date_f = f"{new_itemm[2]}-{new_itemm[1]}-{new_itemm[0]}"
        dattt.append(new_date_f)
#print(dattt)

df_date = pd.DataFrame(dattt)
df_date.columns = ['date']

df_2 = df_2.drop(["end_time"],axis=1) #dropping end_time from dataframe
df_2 = df_2.drop(["date"],axis=1) #dropping date from dataframe

#cleaning the end_time
for item in date_list:
    itemx = item.split(':')
    new_date = f"{item.split(':')[0]}:{item.split(':')[1]}"
    new_date1 = new_date.strip()
    date_list1.append(new_date1)
#print(date_list1)
df_end_time = pd.DataFrame(date_list1)
df_end_time.columns = ['end_time']

df_length = len(df_2.index)
df_2['PW'] = df_2['PW'].replace(',', '').astype(float)
df_2['P_var'] = df_2['P_var'].replace(',', '').astype(float)
#df_2['date'] = pd.to_datetime(df_2['P_var'],format="%Y/%M/%d")


#Getting Apparent power
for i in range(0,df_length):
    val1 = pow(df_2["PW"].loc[i],2)
    val2 = pow(df_2["P_var"].loc[i], 2)
    val_t = val1 + val2
    valuesx = math.sqrt(val_t)
    values = round(valuesx,3)
    data.append(values)

df_ia = pd.DataFrame(data)
df_ia.columns = ['App_pow']

new_df = pd.concat([df_end_time,df_date,df_2,df_ia], axis=1)
print(new_df)
new_df_startdate = new_df['date'].iloc[0]
new_df_enddate = new_df['date'].iloc[-1]
print(new_df_enddate)
new_df.to_excel("C:\\Users\\KIMERA\\Desktop\\1.xlsx")
maxx = new_df.loc[new_df['PW'].idxmax()].tolist()


#dash app
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children="This is my Plot",style={'color':'red','text-align':'center'}),

    html.Br(),
    html.Label(children="Select Day:  ", style={'fontSize':30}),


    dcc.DatePickerRange(
        id='date_range',
        min_date_allowed=new_df_startdate,
        max_date_allowed=new_df_enddate,
        initial_visible_month=date(2020, 10, 2),
        start_date=date(2020, 10, 1),
        end_date=date(2020, 10, 3)
    ),

    dcc.Graph(
        id="graph",
        figure={}
    ),
html.Label(children="Max Demand (kW): ", style={'fontSize':20}),
dcc.Input(id='max_pw',type="text",value=1),
 html.Br(),
html.Br(),
html.Label(children="Max Demand Date: ", style={'fontSize':20}),
dcc.Input(id='date_max',type="text",value=1),
    html.Br(),
html.Br(),
html.Label(children="Max Demand Time (Hrs): ", style={'fontSize':20}),
dcc.Input(id='time_max',type="text",value=1),
#html.Label(children="Hours", style={'fontSize':20,'marginLeft':'10px'}),

dcc.Dropdown(id="month",
             options=[]
             ),
    # html.Div(id='output-single')


])

# #call back application
@app.callback(

     [Output(component_id="graph",component_property="figure"),
     Output(component_id="max_pw",component_property="value"),
      Output(component_id="time_max",component_property="value"),
      Output(component_id="date_max", component_property="value")
      ],
     [Input(component_id="date_range",component_property="start_date"),
      Input(component_id="date_range",component_property="end_date")]
 )
def update_graph(start_date1,end_date1):
    new_dff = new_df.copy()
    #print(new_dff)
    new_dff1= new_dff[new_dff['date'] == start_date1]
    new_dff2 = new_dff[new_dff['date'] == end_date1]
    print(start_date1)
    print(end_date1)
    #plot_df = new_df.loc[new_df['date'] == interest_day]
    print(f"graph dfI is \n{new_dff1}")
    print(f"THIS IS DATAFRAME II \n{new_dff2}")
    #final_df = pd.concat([new_dff1, new_dff2],axis=1)
    final_df = new_dff1.append(new_dff2).reset_index(drop=True)
    #final_df['datetime'] = final_df['date'] + final_df['end_time']
    final_df['datetime'] = final_df[['date', 'end_time']].agg('.'.join, axis=1)
    print(f"THIS IS THE FINAL DF \n {final_df}")
    maxx1 = final_df.loc[final_df['PW'].idxmax()].tolist()
    print(maxx1)
    max_val1 = maxx1[2]
    max_val = "{:,}".format(max_val1)
    time_maxxx = maxx1[5]
    date_maxx = str(time_maxxx).split('.')[0]
    time_maxx = str(time_maxxx).split('.')[1]

    print(max_val)
    fig = go.Figure(
        data=[go.Line(y=final_df['PW'], x=final_df['datetime'])],
        #data=[],
    )
    return fig, max_val,time_maxx,date_maxx
#
if __name__ == "__main__":
    app.run_server(debug=True,use_reloader=True)
