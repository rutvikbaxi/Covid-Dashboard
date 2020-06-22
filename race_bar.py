def bar_chart_race_plot(df_statewise,df_india):
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    import matplotlib.animation as animation
    #plt.rcParams['animation.ffmpeg_path'] = '/ffmpeg'
    df_statewise.reset_index(drop=True,inplace=True)
    colors = dict(zip(
        ['Delhi', 'Haryana', 'Karnataka', 'Kerala', 'Maharashtra','Punjab',
            'Tamil Nadu', 'Rajasthan','Telengana', 'Jammu and Kashmir','Ladakh', 'Uttar Pradesh',
        'Andhra Pradesh', 'Uttarakhand','Odisha', 'Puducherry', 'West Bengal', 'Chhattisgarh',
        'Chandigarh', 'Gujarat','Himachal Pradesh', 'Madhya Pradesh','Bihar', 'Manipur',
        'Mizoram', 'Andaman and Nicobar Islands','Goa', 'Assam', 'Jharkhand', 'Arunachal Pradesh',
        'Tripura','Nagaland', 'Meghalaya', 'Nagaland#', 'Jharkhand#','Madhya Pradesh#', 
        'Dadar Nagar Haveli', 'Sikkim'],
        #lavender,pink,green,red,orange,yellow
        ['#adb0ff', '#f25a92', '#90d595', '#e48381', '#aafbff', '#f7bb5f', '#eafb50',
        '#adb0ff', '#ffb3ff', '#90d595', '#e48381', '#aafbff', '#f7bb5f', '#eafb50',
        '#adb0ff', '#ffb3ff', '#90d595', '#e48381', '#aafbff', '#f7bb5f', '#eafb50',
        '#adb0ff', '#ffb3ff', '#90d595', '#e48381', '#aafbff', '#f7bb5f', '#eafb50',
        '#adb0ff', '#ffb3ff', '#90d595', '#e48381', '#aafbff', '#f7bb5f', '#eafb50',
        '#adb0ff', '#ffb3ff', '#90d595']
    ))
    group_lk = df_statewise['loc'].to_dict()

    fig, ax = plt.subplots(figsize=(15, 8))
    def draw_barchart(date):
        dff = df_statewise[df_statewise['date']==date].sort_values(by='total', ascending=True).tail(10)
        ax.clear()
        ax.barh(dff['loc'], dff['total'], color=[[colors[group_lk[x]] for x in dff.index]][0])
        dx = dff['total'].max() / 200
        #dx=200
        for i, (value, name) in enumerate(zip(dff['total'], dff['loc'])):
            ax.text(value-dx, i, name, size=14, weight=600, ha='right',color='#1a434a')
            ax.text(value+dx, i,f'{value:,.0f}',size=14, ha='left', va='center')
        ax.text(1, 0.4, date, transform=ax.transAxes, color='#a2a2a3', size=46, ha='right', weight=800)
        #
        ax.text(0, 1.06, 'Population', transform=ax.transAxes, size=12, color='#000000')
        
        
        ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))#used for inserting ',' 
        ax.xaxis.set_ticks_position('top')
        ax.tick_params(axis='x', colors='#000000', labelsize=14)
        ax.set_yticks([])
        ax.margins(0, 0.01)
        ax.grid(which='major', axis='x', linestyle='-.',color='#777777')
        ax.set_axisbelow(True)#shifts the grids below the graph
        
        ax.text(0, 1.1, 'Progress of Covid-19 in India: ',color='#1a434a',
                transform=ax.transAxes, size=24, weight=600, ha='left')
        ax.text(1, 0, 'by Rutvik Baxi; credit @pratapvardhan', transform=ax.transAxes, ha='right',
                color='#1a434a', bbox=dict(facecolor='white', alpha=0.8, edgecolor='white'))
        ax.text(1, 0.05, 'Since 10th march', transform=ax.transAxes, ha='right',
                color='#1a434a', bbox=dict(facecolor='white', alpha=0.8, edgecolor='white'))
        plt.box(False)
        
    date_list = list(df_india['date'].unique())

    #@st.cache
    #def animate(fig, draw_barchart,date_list):
    fig, ax = plt.subplots(figsize=(15, 9))
    animator = animation.FuncAnimation(fig, draw_barchart, frames=date_list)
        #st.write(animator.to_html5_video(),unsafe_allow_html=True)
    return animator
    #animate(fig, draw_barchart,date_list)

import streamlit as st
import pandas as pd
df_india=pd.read_csv('df_india.csv')
df_statewise=pd.read_csv('df_statewise.csv')
df_statewise.loc[df_statewise['loc']=='Telangana','loc']='Telengana'
df_statewise.loc[df_statewise['loc']=='Dadra and Nagar Haveli and Daman and Diu','loc']='Dadar Nagar Haveli'
animator=bar_chart_race_plot(df_statewise,df_india)
animator.save('Covid_india_animation3.gif',fps=4)#writer='ffmpeg',
import moviepy.editor as mp
clip = mp.VideoFileClip("Covid_india_animation3.gif")
clip.write_videofile("Covid_india_animation3.mp4")

#video_file = open('Covid_india_animation3.mp4', 'rb')
#video_bytes = video_file.read()
#st.video(video_bytes)

