import json
import urllib
import requests
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objs as go
from plotly.offline import init_notebook_mode,iplot,plot,download_plotlyjs
        
#from map_plotter_india import *

#df_timestamp=pd.read_pickle('df_timestamp.pkl')
df_timestamp=pd.read_csv('df_timestamp.csv')
timestamp=pd.to_datetime(df_timestamp.loc[0].values[0])
#timestamp=df_timestamp.loc[0,0]

class covid_india:
    def __init__(self):
        #import datetime
        import pandas as pd
        df_timestamp=pd.read_csv('df_timestamp.csv')
        timestamp=pd.to_datetime(df_timestamp.loc[0].values[0])
        from datetime import datetime
        from datetime import timedelta
        time_elapsed=(((datetime.today())-timestamp).seconds/3600 + ((datetime.today())-timestamp).days*24)
        if (time_elapsed >24):
            import json
            import urllib
            import time
            import requests
            import numpy as np
            import pandas as pd
            url = "https://api.rootnet.in/covid19-in/stats/history"
            data = json.loads(requests.get(url).text)
        
            df_india=pd.DataFrame(columns=['total','deaths','discharged'])
            df_temp=pd.DataFrame()
            for i in range(0,len(data['data'])):
                df_temp[['total','deaths','discharged']]=pd.DataFrame([data['data'][i]['summary'][x] for x in ['total','deaths','discharged']]).T
                df_temp['date']=data['data'][i]['day']
                df_india=df_india.append(df_temp,ignore_index=True)
            #Calculating percentage and also active cases
            df_india['active']=df_india.apply(lambda x: x.total-x.discharged-x.deaths,axis=1)
            df_india['perdeath']=df_india.apply(lambda x: '%.2f'%(x['deaths']*100/x.total),axis=1)
            df_india['perdis']=df_india.apply(lambda x: '%.2f'%(x['discharged']*100/x.total),axis=1)
            df_india['peractive']=df_india.apply(lambda x: '%.2f'%(x['active']*100/x.total),axis=1)
            #Converting to float
            df_india['perdeath']=df_india['perdeath'].astype(float)
            df_india['perdis']=df_india['perdis'].astype(float)
            df_india['peractive']=df_india['peractive'].astype(float)
            self.df_india=df_india

            #state
            df_statewise=pd.DataFrame()
            df_temp2=pd.DataFrame()
            for j in range(0,len(data['data'])):
                df_temp2=pd.DataFrame()
                for i in range(0,len(data['data'][j]['regional'])):
                    df_temp=pd.DataFrame(data['data'][j]['regional'][i],index=[i])
                    df_temp2=df_temp2.append([df_temp],sort=True)
                df_temp2['date']=data['data'][j]['day']
                df_statewise=df_statewise.append([df_temp2],sort=True)
            df_statewise=df_statewise[(df_statewise['loc']!='Nagaland#') & (df_statewise['loc']!='Jharkhand#') & (df_statewise['loc']!='Madhya Pradesh#')]
            df_statewise=df_statewise[[ 'loc','totalConfirmed','deaths','discharged','date']]
            df_statewise.reset_index(drop=True,inplace=True) 

            df_statewise.drop([1052,1085],inplace=True)
            df_statewise['active']=df_statewise.apply(lambda x: x.totalConfirmed-x.discharged-x.deaths,axis=1)
            df_statewise['perdeath']=df_statewise.apply(lambda x: '%.2f'%(x['deaths']*100/x.totalConfirmed),axis=1)
            df_statewise['perdis']=df_statewise.apply(lambda x: '%.2f'%(x['discharged']*100/x.totalConfirmed),axis=1)
            df_statewise['peractive']=df_statewise.apply(lambda x: '%.2f'%(x['active']*100/x.totalConfirmed),axis=1)
                #Converting to float
            df_statewise['perdeath']=df_statewise['perdeath'].astype(float)
            df_statewise['perdis']=df_statewise['perdis'].astype(float)
            df_statewise['peractive']=df_statewise['peractive'].astype(float)
            df_statewise=df_statewise.rename(columns={'totalConfirmed':'total'})
            self.df_statewise=df_statewise

            #india_daily(self):
            self.df_india_daily=self.df_india.drop('date',axis=1).diff().join(df_india['date']).drop(0)
            df_india_daily=self.df_india_daily

            #statewise daily count
            df_daily_statewise=pd.DataFrame()
            df_daily_temp=pd.DataFrame()
            for state in df_statewise['loc'].unique():
                df_daily_temp=df_statewise[df_statewise['loc']==state].drop(['date','loc'],axis=1).diff().reset_index(drop=True).join(df_statewise[df_statewise['loc']==state][['date','loc']].reset_index(drop=True)).drop(0)
                df_daily_statewise=df_daily_statewise.append([df_daily_temp],sort=True)
            self.df_daily_statewise=df_daily_statewise

            # df_india.to_pickle('df_india.pkl')
            # df_statewise.to_pickle('df_statewise.pkl')
            # df_india_daily.to_pickle('df_india_daily.pkl')
            # df_daily_statewise.to_pickle('df_daily_statewise.pkl')

            df_india.to_csv('df_india.csv',index=False)
            df_statewise.to_csv('df_statewise.csv',index=False)
            df_india_daily.to_csv('df_india_daily.csv',index=False)
            df_daily_statewise.to_csv('df_daily_statewise.csv',index=False)

            #map_plot()

            #refresh the timestamp
        timestamp=datetime.today() + timedelta(seconds=19800)
        df_timestamp=pd.DataFrame()
        df_timestamp.loc[0,0]=timestamp
        df_timestamp.to_pickle('df_timestamp.pkl')
        df_timestamp.to_csv('df_timestamp.csv',index=False)
            
            

class covid_plotter:
    def lineplot(self,df,title_graph):
        roll=df['active'].rolling(7).mean()
        roll=roll.fillna(0) 
        df['rollingactive']=pd.DataFrame(roll)
        tracet=go.Scatter(x=df.date, y=df.total, mode='lines+markers',name='total cases',marker_symbol=0,
                   marker = dict(color = '#4cd0f5'),)
        tracede=go.Scatter(x=df.date, y=df.deaths, mode='lines+markers',name='deaths',marker_symbol=4,
                           marker = dict(color = '#6e6b63'),text=(df.perdeath.apply(lambda x:str(x)) + '%'))
        tracedi=go.Scatter(x=df.date, y=df.discharged, mode='lines+markers',name='discharged', marker_symbol=6,
                           marker = dict(color = '#4dfa90'),text=(df.perdis.apply(lambda x:str(x)) + '%'))
        tracea=go.Scatter(x=df.date, y=df.active, mode='lines+markers',name='active', marker_symbol=2,
                           marker = dict(color = '#fa574b'),text=(df.peractive.apply(lambda x:str(x)) + '%'))
        tracer=go.Scatter(x=df.date, y=df.rollingactive, mode='lines',name='Last 7 days average', marker_symbol=5,
                           marker = dict(color = '#000000'))
        data = [tracet, tracede,tracedi,tracea,tracer]

        layout = dict(title = title_graph,xaxis= dict(title= 'Date',zeroline= True),height=400)

        fig = dict(data = data, layout = layout)
        return fig
    
    def stack_bar(self,df,title_graph):
        roll=df['active'].rolling(7).mean()
        roll=roll.fillna(0) 
        df['rollingactive']=pd.DataFrame(roll)
        fig1 = go.Figure(data=[
        go.Bar(name='Active',    x=df.date, y=df.active,marker=dict(color='#fa574b'),hovertext=(df.peractive.apply(lambda x:str(x)) + '%')),
        go.Bar(name='Discharged',x=df.date, y=df.discharged,marker=dict(color='#4dfa90'),hovertext=(df.perdis.apply(lambda x:str(x)) + '%')),
        go.Bar(name='Deaths',    x=df.date, y=df.deaths,marker=dict(color='#4cd0f5'),hovertext=(df.perdeath.apply(lambda x:str(x)) + '%')),
        go.Scatter(name='Last 7 days average', x=df.date, y=df.rollingactive ,marker=dict(color='#000000')),
        ])
        fig1.update_layout(barmode='stack',title=title_graph,height=400)

        return fig1

        min_4=df_statewise[-35:].sort_values('active',ascending=False)[:4]['loc'].values
        fig = make_subplots(rows=2, cols=2,
                            subplot_titles=min_4)
                            
        fig.add_trace(go.Scatter(x=df_statewise[df_statewise['loc']==min_4[0]]['date'],y=df_statewise[df_statewise['loc']==min_4[0]]['total']),row=1, col=1)
        fig.add_trace(go.Scatter(x=df_statewise[df_statewise['loc']==min_4[1]]['date'],y=df_statewise[df_statewise['loc']==min_4[1]]['total']),row=1, col=2)
        fig.add_trace(go.Scatter(x=df_statewise[df_statewise['loc']==min_4[2]]['date'],y=df_statewise[df_statewise['loc']==min_4[2]]['total']),row=2, col=1)
        fig.add_trace(go.Scatter(x=df_statewise[df_statewise['loc']==min_4[3]]['date'],y=df_statewise[df_statewise['loc']==min_4[3]]['total']),row=2, col=2)
        fig.update_layout(height=500, width=700,
                        title_text="States with highest active cases")
        return fig

    def lockdown(self,df):
        date_list=['2020-03-24', '2020-04-14', '2020-05-01', '2020-05-17','2020-05-30','2020-06-30',df[-1:].date.values[0]]
        df2=df[df['date'].isin(date_list)]
        for i in range(0,4):
            x=date_list[i]
            df2.loc[df2['date']==x,'lockdown']='Lockdown {}'.format(i)
        df2.loc[df2['date']=='2020-05-30','lockdown']='Unlock {}'.format(1)
        df2.loc[df2['date']=='2020-06-30','lockdown']='Unlock {}'.format(2)
        df2.loc[df2['date']==df[-1:].date.values[0],'lockdown']='Present'
        tracet=go.Scatter(x=df2.lockdown, y=df2.total, mode='lines+markers',name='total cases',marker_symbol=0,
                   marker = dict(color = '#4cd0f5'),)
        tracede=go.Scatter(x=df2.lockdown, y=df2.deaths, mode='lines+markers',name='deaths',marker_symbol=4,
                           marker = dict(color = '#6e6b63'),text=(df2.perdeath.apply(lambda x:str(x)) + '%'))
        tracedi=go.Scatter(x=df2.lockdown, y=df2.discharged, mode='lines+markers',name='discharged', marker_symbol=6,
                           marker = dict(color = '#4dfa90'),text=(df2.perdis.apply(lambda x:str(x)) + '%'))
        tracea=go.Scatter(x=df2.lockdown, y=df2.active, mode='lines+markers',name='active', marker_symbol=2,
                           marker = dict(color = '#fa574b'),text=(df2.peractive.apply(lambda x:str(x)) + '%'))
        data = [tracet, tracede,tracedi,tracea]
        layout = dict(title = 'Lockdown-wise changes in cases',xaxis= dict(title= 'Lockdown',zeroline= True),height=400)
        fig2 = dict(data = data, layout = layout)
        return fig2

    def top_4_states(self,df_statewise):
            from plotly.subplots import make_subplots
            import plotly.graph_objects as go

            df2=df_statewise[-35:].sort_values('active',ascending=False)[['active','total','loc']].reset_index(drop=True)
            df2.loc[4:,'loc']='Other states'
            labels=df2['loc']
            valuesa=df2['active']
            valuest=df2['total']
            fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
            fig.add_trace(go.Pie(labels=labels, values=valuesa, name="Active"),
                        1, 1)
            fig.add_trace(go.Pie(labels=labels, values=valuest, name="Total"),
                        1, 2)
            fig.update_traces(hole=.4, hoverinfo="label+percent+name")
            fig.update_layout(
                title_text="Contribution of top 4 states(by number of active cases) in India",
                # Add annotations in the center of the donut pies.
                annotations=[dict(text='Active', x=0.18, y=0.5, font_size=16, showarrow=False),
                            dict(text='Total', x=0.82, y=0.5, font_size=16, showarrow=False)])
            st.write(fig)

            min_4=df_statewise[-35:].sort_values('active',ascending=False)[:4]['loc'].values
            fig = make_subplots(rows=2, cols=2,
                                subplot_titles=min_4)
                                
            fig.add_trace(go.Scatter(x=df_statewise[df_statewise['loc']==min_4[0]]['date'],y=df_statewise[df_statewise['loc']==min_4[0]]['active']),row=1, col=1)
            fig.add_trace(go.Scatter(x=df_statewise[df_statewise['loc']==min_4[1]]['date'],y=df_statewise[df_statewise['loc']==min_4[1]]['active']),row=1, col=2)
            fig.add_trace(go.Scatter(x=df_statewise[df_statewise['loc']==min_4[2]]['date'],y=df_statewise[df_statewise['loc']==min_4[2]]['active']),row=2, col=1)
            fig.add_trace(go.Scatter(x=df_statewise[df_statewise['loc']==min_4[3]]['date'],y=df_statewise[df_statewise['loc']==min_4[3]]['active']),row=2, col=2)


            fig.update_layout(height=500, width=700,
                            title_text="States with highest active cases")
            return fig
    
    def top_10_states(self,df_statewise):
        import plotly.graph_objects as go
        df_statewise=pd.read_csv('df_statewise.csv')
        df_statewise=df_statewise[-35:]
        df=df_statewise.sort_values('total',ascending=False)[:10][['loc','total','active','deaths']]
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df['loc'],
            y=df.total,
            name='Total cases',
            marker_color='#4788de'
        ))
        fig.add_trace(go.Bar(
            x=df['loc'],
            y=df.active,
            name='Active cases',
            marker_color='#e35b5b'
        ))
        fig.add_trace(go.Bar(
            x=df['loc'],
            y=df.deaths,
            name='Deaths',
            marker_color='#87898c'
        ))
        fig.update_layout(barmode='group', xaxis_tickangle=-45,title_text='Top 10 states by total cases')
        return fig

    def map_plot(self,df_statewise):
        df_coords_state=pd.read_csv('state wise centroids_2011.csv')
        df_statewise=df_statewise[df_statewise['loc']!='Daman & Diu']
        df_statewise=df_statewise[-35:]
        df_statewise=df_statewise[['loc','total','active','deaths','discharged']]
        df_statewise.reset_index(inplace=True, drop=True)
        for state in df_statewise['loc'].unique():
            df_statewise.loc[df_statewise['loc']==state,'Latitude']=df_coords_state[df_coords_state['State']==state]['Latitude'].values[0]
            df_statewise.loc[df_statewise['loc']==state,'Longitude']=df_coords_state[df_coords_state['State']==state]['Longitude'].values[0]
        df=df_statewise
        import plotly.express as px
        fig = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", hover_name="loc",zoom=3, hover_data=["total", "active","deaths",'discharged'],size="total",color='total',color_continuous_scale='OrRd', height=300)
        fig.update_layout(mapbox_style="dark", mapbox_accesstoken='pk.eyJ1IjoicnV0dmlrYmF4aSIsImEiOiJja2F6bGpzYXAwZXZuMnluczFzcjJicWRlIn0.WBKhU7BPKNKuZlgQrto6kQ')
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.write(fig)
