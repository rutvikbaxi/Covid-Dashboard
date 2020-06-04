import pandas as pd
import streamlit as st
def map_plot2(df_statewise):
        import pydeck as pdk
        df_coords_state=pd.read_csv('state wise centroids_2011.csv')
        df_statewise=df_statewise[-35:]
        df_statewise=df_statewise[['loc','total']]
        df_statewise.reset_index(inplace=True, drop=True)
        for state in df_statewise['loc'].unique():
            df_statewise.loc[df_statewise['loc']==state,'Latitude']=df_coords_state[df_coords_state['State']==state]['Latitude'].values[0]
            df_statewise.loc[df_statewise['loc']==state,'Longitude']=df_coords_state[df_coords_state['State']==state]['Longitude'].values[0]
        #df_coords_state=pd.concat([df_statewise,df_coords_state],axis=1)
        df_statewise.drop('loc',inplace=True, axis=1)
        df=df_statewise

        center_long = df_coords_state.mean().Longitude
        center_lat = df_coords_state.mean().Latitude

        COLOR_BREWER_BLUE_SCALE = [
            [105, 192, 245],
            [153,213,148],
            [245, 242, 152],
             [230, 146, 87],
             [255,141,89],
            [213,62,79],
        ]
        total = pdk.Layer(
            "HeatmapLayer",
            data=df,
            opacity=0.9,
            get_position='[Longitude,Latitude]',
            aggregation='"MEAN"',
            color_range=COLOR_BREWER_BLUE_SCALE,
            threshold=0.05,
            intensity=1,
            get_weight="total",
            radiusPixels=50,
            pickable=True,
        )
        initial_view_state=pdk.ViewState(
            latitude=center_lat,
            longitude=center_long,
            zoom=3.5,
            pitch=20,
        )
        r = pdk.Deck(
        layers=[total],
        initial_view_state=initial_view_state,
        map_style="mapbox://styles/mapbox/dark-v9",
        tooltip={"text": "Concentration of Covid cases"},
        )
        st.pydeck_chart(r)