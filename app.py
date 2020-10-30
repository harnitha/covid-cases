# libraries needed
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

# color pallette
cnf = '#393e46'  # confirmed - grey
dth = '#ff2e63'  # death - red
rec = '#21bf73'  # recovered - cyan
act = '#fe9801'  # active case - yellow
blk = '#000000'  # black
plp = '#663399'  # purple


#find india stats
india_totals = pd.read_csv('https://api.covid19india.org/csv/latest/case_time_series.csv')
today_totals = india_totals.iloc[len(india_totals) - 1]
print(today_totals)
date = today_totals['Date']
india_totals.head()


#Line chart for Total India-confirmed,recovered and deceased
df = pd.DataFrame(india_totals, columns=['Date', 'Total Deceased', 'Total Recovered', 'Total Confirmed'])
df1 = df.melt(id_vars=['Date'] + list(df.keys()[4:]), var_name='Cases')
fig1 = px.line(df1, x="Date", y='value', color='Cases', title=f'Line Chart for Total India on {date}')
fig1.update_layout(margin=dict(t=180, l=0, r=0, b=0), yaxis_title="Number of Cases")



#pie chart for india-total confirmed recovered deceased
df = dict(today_totals)
labels = list(df.keys())
labels = ['Total Confirmed', 'Total Recovered', 'Total Deceased']
values = []
for i in labels:
    values.append(df[i])

fig2 = go.Figure(data=[go.Pie(labels=labels, values=values,
                              title=f'For India on: {date}', )])



#pie chart for india-daily confirmed recovered deceased
df = dict(today_totals)
labels = list(df.keys())
labels = ['Daily Confirmed', 'Daily Recovered', 'Daily Deceased']
values = []
for i in labels:
    values.append(df[i])

fig3 = go.Figure(data=[go.Pie(labels=labels, values=values,
                              title=f'For India on: {date}', )])



#statewise
state = pd.read_csv("https://api.covid19india.org/csv/latest/state_wise.csv")

statewise = state[state['State'] != 'Total']
statewise.head(20)

statedaily = pd.read_csv('https://api.covid19india.org/csv/latest/state_wise_daily.csv')
statedaily.tail()

today_totals = statedaily.iloc[len(statedaily) - 1]
date = today_totals['Date']

#line chart
fig4 = px.line(statedaily, x="Date", y='TN', color='Status',
               title=f'Line Chart for Daily Cases for TamilNadu on {date}')
fig4.update_layout(margin=dict(t=180, l=0, r=0, b=0), yaxis_title="Number of Cases")




#barchart confirmed cases sorted
fig5 = px.bar(statewise.sort_values('Confirmed', ascending=True),
              x="Confirmed", y="State", title=f'Total Confirmed Cases [Statewise-Comparision]-{date}2020',
              text='Confirmed', orientation='h',
              width=700, height=700, range_x=[0, max(statewise['Confirmed']) + 1000000])
fig5.update_traces(marker_color=plp, opacity=1, textposition='inside')
fig5.update_layout(margin=dict(t=80, l=0, r=0, b=0))


# stacked bar chart statewise
temp = statewise.groupby('State')['Confirmed', 'Recovered', 'Deaths', 'Active'].sum().reset_index()
temp = temp.melt(id_vars="State", value_vars=['Confirmed', 'Recovered', 'Deaths', 'Active'], var_name='Case',
                 value_name='Count')
temp.head()

fig6 = px.bar(temp, x="State", y="Count", color='Case',
              title=f'Comparision of Cases-{date}2020', color_discrete_sequence=[rec, dth, act, cnf])



#statewise testing
data1 = pd.read_csv('https://api.covid19india.org/csv/latest/statewise_tested_numbers_data.csv')

task = data1[['Updated On', 'State', 'Total Tested']].copy()
task.tail()

month = {"January": '01', "February": '02', 'March': '03', 'April': '04', 'May': '05', 'June': '06', 'July': '07',
         'August': '08', 'September': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
DAY = {1: '01', 2: '02', 3: '03', 4: '04', 5: '05', 6: '06', 7: '07', 8: '08', 9: '09'}
d = date.split("-")

day = int(d[0])
mon = month[d[1]]
if day < 10:
    day = day
    date_struc = f'{DAY[day]}/{mon}/2020'
else:
    date_struc = f'{day}/{mon}/2020'

tested = task.loc[task['Updated On'] == date_struc]

fig7 = px.bar(tested.sort_values('Total Tested', ascending=False).sort_values('Total Tested', ascending=True),
              x="Total Tested", y="State", title=f'Tested Cases [Statewise Comparision] -{date_struc} ',
              text='Total Tested', orientation='h',
              width=700, height=700)
fig7.update_traces(marker_color=plp, opacity=1, )
fig7.update_layout(margin=dict(t=80, l=0, r=0, b=0))


top5 = tested.sort_values(by=['Total Tested'], ascending=False)
top5[:5]

least = tested.sort_values(by=['Total Tested'])
least[:5]


#world wide data
world_confirmed = pd.read_csv(
    'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
world_death = pd.read_csv(
    'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
world_recovered = pd.read_csv(
    'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')

date_world = world_confirmed.columns[-1]
world_confirmed

#world confirmed sorted
fig8 = px.bar(
    world_confirmed.sort_values(f'{date_world}', ascending=False).head(25).sort_values(f'{date_world}', ascending=True),
    x=date_world, y="Country/Region", title=f'Confirmed cases [Country wise-first 25 highest cases] -{date_world} ',
    orientation='h',
    width=700, height=700, text=date_world)
fig8.update_traces(marker_color=plp, opacity=1)
fig8.update_layout(margin=dict(t=80, l=0, r=0, b=0), xaxis_title="Confirmed Cases", )


#world deceased sorted
date_death = world_death.columns[-1]
fig9 = px.bar(
    world_death.sort_values(f'{date_death}', ascending=False).head(25).sort_values(f'{date_death}', ascending=True),
    x=date_death, y="Country/Region", title=f'Death cases [Country wise-first 25 highest cases] -{date_death} ',
    orientation='h',
    width=700, height=700, text=date_death)
fig9.update_traces(marker_color=plp, opacity=1)
fig9.update_layout(margin=dict(t=80, l=0, r=0, b=0), xaxis_title="Death Cases", )


#world recovered sorted
date_rec = world_recovered.columns[-1]
fig10 = px.bar(
    world_recovered.sort_values(f'{date_rec}', ascending=False).head(25).sort_values(f'{date_rec}', ascending=True),
    x=date_rec, y="Country/Region", title=f'Recovered cases [Country wise-first 25 highest cases] -{date_rec}'
    , orientation='h', text=date_rec,
    width=700, height=700)
fig10.update_traces(marker_color=plp, opacity=1)
fig10.update_layout(margin=dict(t=80, l=0, r=0, b=0), xaxis_title="Recovered Cases", )

#world map

url = 'https://raw.githubusercontent.com/imdevskp/covid_19_jhu_data_web_scrap_and_cleaning/master/covid_19_clean_complete.csv'
full_table = pd.read_csv(url,
                         parse_dates=['Date'])



full_latest = full_table[full_table['Date'] == max(full_table['Date'])].reset_index()
china_latest = full_latest[full_latest['Country/Region'] == 'China']
row_latest = full_latest[full_latest['Country/Region'] != 'China']



full_latest_grouped = full_latest.groupby('Country/Region')[
    'Confirmed', 'Deaths', 'Recovered', 'Active'].sum().reset_index()

fig11 = px.choropleth(full_latest_grouped, locations="Country/Region",
                      locationmode='country names', color="Confirmed",
                      hover_name="Country/Region", range_color=[1, max(full_latest_grouped['Confirmed'])],
                      color_continuous_scale="aggrnyl",
                      title=f'Countries with Confirmed Cases on {date}')
fig11.update(layout_coloraxis_showscale=True)
fig11.update_layout(margin=dict(t=80, l=0, r=0, b=0))
# fig11.show() #.write_image('covid-eda-1-1.png')



# Create the app
app = dash.Dash()
app.layout = html.Div(children=[
    # All elements from the top of the page

    html.Div([
        html.H1(children=""" """),
        dcc.Graph(id='graph1',figure=fig1)
    ]),
    # New Div for all elements in the new 'row' of the page
    html.Div([
        html.H4(children='''Comparison between Total Confirmed,Recovered and Deceased Cases for India'''),

        dcc.Graph(id='graph2',figure=fig2)
    ]),
    html.Div([
        html.H4(children='''Comparison between Daily Confirmed,Recovered and Deceased Cases for India '''),
        dcc.Graph(id='graph3',figure=fig3)
    ]),
    html.Div([
        html.H1(children=''' '''),
        dcc.Graph(id='graph4',figure=fig4)
    ]),
    html.Div([
        html.H1(children=''' '''),
        dcc.Graph(id='graph5',figure=fig5)
    ]),
    html.Div([
        html.H1(children=''' '''),
        dcc.Graph(id='graph6',figure=fig6)
    ]),html.Div([
        html.H1(children=''' '''),
        dcc.Graph(id='graph7',figure=fig7)
    ]),html.Div([
        html.H1(children=''' '''),
        dcc.Graph(id='graph8',figure=fig8)
    ]),html.Div([
        html.H1(children=''' '''),
        dcc.Graph(id='graph9',figure=fig9)
    ]),html.Div([
        html.H1(children=''' '''),
        dcc.Graph(id='graph10',figure=fig10)
    ]),html.Div([
        html.H1(children=''' '''),
        dcc.Graph(id='graph11',figure=fig11)
    ]),

])

app.run_server(debug=True)