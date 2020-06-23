import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
from plotly import graph_objs as go
from plotly.offline import iplot,plot,download_plotlyjs,init_notebook_mode
from covid_19_oop import covid_india,covid_plotter
from datetime import datetime 
from datetime import timedelta
from functions import *

#######
#for import

HTML_t = """<div style="ovrflow-x:auto;color:white;border: 1px solid #e6e9ef; border-radius: 0.4rem;
padding: 0.5rem; background-color:#377ed4 ;margin-bottom: 1rem; width: 250px;font-weight:500 ;float:left">Total: {}</div>"""
HTML_a = """<div style="ovrflow-x:auto;color:#a8192b;border: 1px solid #e6e9ef; border-radius: 0.4rem;
padding: 0.5rem; background-color:#ed939e ;margin-bottom: 1rem; width: 250px;font-weight:500 ; float:left">Active    {} <br> {}%</div>"""
HTML_de= """<div style="ovrflow-x:auto;color:white;border: 1px solid #e6e9ef; border-radius: 0.4rem;
padding: 0.5rem; background-color:#2c3632 ;margin-bottom: 1rem; width: 250px; font-weight:500 ;float:left">Deaths    {}  <br>   {}%</div>"""

def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)


local_css("style.css")
t = "<div><NOBR><span class='highlight blue'>Total: {} </span> <span>&nbsp</span> <span class='highlight red'>Active: {}  {}% </span> <span>&nbsp</span> <span class='highlight green'>Recovered: {} {}% </span> <span>&nbsp</span> <span class='highlight black'>Death: {} {}% </span> <span>&nbsp</span></NOBR></div>"
title = "<div><h1><span class='ho'>Covid19</span>&nbsp <span class='hb'>India</span>&nbsp <span class='hg'>Dashboard</span>&nbsp </h1></div>"
st.markdown(title,unsafe_allow_html=True)
#st.title('Covid19 Dashboard')
st.subheader('by Rutvik Baxi')
st.write('')

df_timestamp=pd.read_csv('df_timestamp.csv')
timestamp=pd.to_datetime(df_timestamp.loc[0].values[0])
#time_elapsed=(((datetime.today())-timestamp).seconds/3600 + ((datetime.today())-timestamp).days*24)
st.write('Ignore this line: ',timestamp+ timedelta(seconds=19800),' IST')

@st.cache
def load_data():
    data1=covid_india()
    return data1

data1=load_data()
#df_india=pd.read_pickle('df_india.pkl')
#df_statewise=pd.read_pickle('df_statewise.pkl')
#df_india_daily=pd.read_pickle('df_india_daily.pkl')
#df_daily_statewise=pd.read_pickle('df_daily_statewise.pkl')

df_india=pd.read_csv('df_india.csv')
df_statewise=pd.read_csv('df_statewise.csv')
df_india_daily=pd.read_csv('df_india_daily.csv')
df_daily_statewise=pd.read_csv('df_daily_statewise.csv')
df_india_daily=df_india_daily[df_india_daily['active']>=0]
df_statewise.loc[df_statewise['loc']=='Telangana','loc']='Telengana'
df_statewise.loc[df_statewise['loc']=='Dadra and Nagar Haveli and Daman and Diu','loc']='Dadar Nagar Haveli'
#df_india_daily.reset_index(drop=True,inplace=True)
#def main():


plt1=covid_plotter()
################################
#@st.cache
# import pandas as pd
df_timestamp=pd.read_csv('df_timestamp.csv')
timestamp=pd.to_datetime(df_timestamp.loc[0].values[0])

location_type=st.sidebar.radio('Menu',options=('Overall India','Individual States','About the page'))
##state data
if location_type=='Individual States':
    st.subheader('State data')
    st.write(plt1.top_4_states(df_statewise))
    #state=st.selectbox('States',df_statewise['loc'].unique())
    state=st.selectbox('States',np.delete(df_statewise['loc'].unique(),np.where(df_statewise['loc'].unique()=='Andaman and Nicobar Islands')))
    graph_type=st.radio('Type of Graph',options=('Bar','Line'))
    date_range=st.radio(' ',options=('Overall','Last 15 days'))
    #st.write(plt1.lineplot(df_statewise[df_statewise['loc']==state],'Local total cases'))
    if date_range=='Overall':
        if graph_type=='Bar':
            st.write(plt1.stack_bar(df_statewise[df_statewise['loc']==state],'{} cases: overall'.format(state)))
            #st.write(plt1.stack_bar(df_daily_statewise[df_daily_statewise['loc']==state],'{} cases: daily'.format(state)))
        else:
            st.write(plt1.lineplot(df_statewise[df_statewise['loc']==state],'{} total cases'.format(state)))
            #st.write(plt1.lineplot(df_daily_statewise[df_daily_statewise['loc']==state],'{} cases: daily'.format(state)))
    else:
        if graph_type=='Bar':
            st.write(plt1.stack_bar(df_statewise[df_statewise['loc']==state][-15:],'{} cases: Last 15 days'.format(state)))
            #st.write(plt1.stack_bar(df_daily_statewise[df_daily_statewise['loc']==state][-15:],'{} cases: Daily count in last 15 days'.format(state)))

        else:
            st.write(plt1.lineplot(df_statewise[df_statewise['loc']==state][-15:],'{} cases: Last 15 days'.format(state)))
            #st.write(plt1.lineplot(df_daily_statewise[df_daily_statewise['loc']==state][-15:],'{} cases:  Daily count in last 15 days'.format(state)))

    #ttotal=str(df_statewise[-35:][df_statewise['loc']==state]['total'].values[0])
    ttotal=df_statewise[-35:][df_statewise['loc']==state]['total'].values[0]
    tactive=df_statewise[-35:][df_statewise['loc']==state]['active'].values[0]
    tperactive=str(df_statewise[-35:][df_statewise['loc']==state]['peractive'].values[0])
    tdis=int(df_statewise[-35:][df_statewise['loc']==state]['total'].values[0]*df_statewise[-35:][df_statewise['loc']==state]['perdis'].values[0]/100)
    tperdis=str(df_statewise[-35:][df_statewise['loc']==state]['perdis'].values[0])
    tdeaths=df_statewise[-35:][df_statewise['loc']==state]['deaths'].values[0]
    tperdeath=str(df_statewise[-35:][df_statewise['loc']==state]['perdeath'].values[0])
    st.markdown(t.format(f'{ttotal:,.0f}',f'{tactive:,.0f}',tperactive,f'{tdis:,.0f}',tperdis,f'{tdeaths:,.0f}',tperdeath), unsafe_allow_html=True)
    st.write('')
    #st.write('as of  ',str(datetime.now()).split()[0])
    st.write('last updated on ',timestamp+ timedelta(seconds=19800),' IST'  )  
    st.write('')
    st.write(plt1.top_10_states(df_statewise))
    
elif location_type=='Overall India':
    ttotal=df_india[-1:]['total'].values[0]
    tactive=df_india[-1:]['active'].values[0]
    tperactive=str(df_india[-1:]['peractive'].values[0])
    tdis=int(df_india[-1:]['total'].values[0]*df_india[-1:]['perdis'].values[0]/100)
    tperdis=str(df_india[-1:]['perdis'].values[0])
    tdeaths=df_india[-1:]['deaths'].values[0]
    tperdeath=str(df_india[-1:]['perdeath'].values[0])
    st.markdown(t.format(f'{ttotal:,.0f}',f'{tactive:,.0f}',tperactive,f'{tdis:,.0f}',tperdis,f'{tdeaths:,.0f}',tperdeath), unsafe_allow_html=True)
    st.write('')
    #st.write('as of  ',str(datetime.now()).split()[0])
    st.write('last updated on ',timestamp+ timedelta(seconds=19800),' IST' )  
    st.write('')
    graph_type=st.selectbox('Type of Graph',options=('Bar','Line'))
    date_range=st.radio(' ',options=('Overall','Last 15 days'))
    if date_range=='Overall':
        if graph_type=='Bar':
            st.write(plt1.stack_bar(df_india,'India cases: overall'))
            st.write(plt1.stack_bar(df_india_daily,'India cases: daily'))
            
        else:
            st.write(plt1.lineplot(df_india,'India total cases'))
            st.write(plt1.lineplot(df_india_daily,'India cases: daily'))
    else:
        if graph_type=='Bar':
            st.write(plt1.stack_bar(df_india[-15:],'India cases: Last 15 days'))
            st.write(plt1.stack_bar(df_india_daily[-15:],'India cases: Daily count in last 15 days'))

        else:
            st.write(plt1.lineplot(df_india[-15:],'India cases: Last 15 days'))
            st.write(plt1.lineplot(df_india_daily[-15:],'India cases:  Daily count in last 15 days'))
    
    st.write(plt1.lockdown(df_india))
    video_file = open('Covid_india_animation3.mp4', 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)
    st.write('')
    st.subheader('Relative density distribution of Covid patients: ')
    st.write('This gives the relative density of the cases density w.r.t other states')
    df_statewise['days']=df_statewise['date'].apply(lambda x: (pd.to_datetime(x)-pd.to_datetime('2020-03-10')).days)
    days=st.slider('Number of days since starting',min_value=0,max_value=int(df_statewise[-1:]['days'].values[0]),value=int(df_statewise[-1:]['days'].values[0]),step=20)
    df_statewise2=df_statewise[df_statewise['days']<=days]
    #map_plot2(df_statewise2)
    #st.image('india_map.png',format='PNG')
    plt1.map_plot(df_statewise2)
    st.write('')
    st.subheader('Statewise-count as of {}'.format(datetime.today().date()))
    x=df_statewise[-35:].sort_values('total',ascending=False)[['loc','total','active','discharged','deaths']]
    x.reset_index(drop=True,inplace=True)
    cm = sns.light_palette("green", as_cmap=True)
    s = x.style.background_gradient(cmap=cm)
    st.dataframe(s,width=600)
    st.write('current time: ',(datetime.today() + timedelta(seconds=19800)), 'IST')

elif location_type=='About the page':
    st.header('About the developer')
    st.image('rutvik.jpg', width=150)
    st.markdown(' “You can have data without information, but you cannot have information without data.” – Daniel Keys Moran')
    st.markdown('Hello there! My name is Rutvik Baxi and I am currently an undergraduate student enrolled at the Department of Engineering Design at IIT Madras.  I enjoy learning new stuff which helps me expand my boundaries of knowledge and experience.I am highly enthusisatic about the field of Data Analytics and Machine Learning, and enjoy how new oppurtunities unroll every day in this field. So in an attempt to implement all my learning, I have built this real-time dashboard to present the most severe issue of India and the world in 2020: Covid19. This is an interactive dashboard with real time data and customized plots. This dashboard has been built using Streamlit and is mainly Python script. The data is updated every 24 hours. I will be glad to hear your thoughts or suggestions, you can reach out to me via [my LinkedIn](https://www.linkedin.com/in/rutvik-baxi) or [Facebook](https://www.facebook.com/rutvik.baxi.3/).',unsafe_allow_html=True)
    st.subheader('Acknowledgements')
    st.write('The data used here is collected from an online API from api.rootnet.in. ')
