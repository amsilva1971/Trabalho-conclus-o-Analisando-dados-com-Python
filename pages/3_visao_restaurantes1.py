#------Importando as bibliotecas-------#
import datetime
import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image
#from haversine import haversine
#import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static
from datetime import datetime


st.set_page_config (page_title='Visão restaurantes', page_icon='', layout='wide') 

#-------Criando as funções/modularização--------#

def limpeza (df):
    
    df.loc[:, 'ID'] = df.loc[:, 'ID'].str.strip()
    df.loc[:, 'Delivery_person_ID'] = df.loc[:, 'Delivery_person_ID'].str.strip()
    df.loc[:, 'Road_traffic_density'] = df.loc[:, 'Road_traffic_density'].str.strip()
    df.loc[:, 'Type_of_order'] = df.loc[:, 'Type_of_order'].str.strip()
    df.loc[:, 'Type_of_vehicle'] = df.loc[:, 'Type_of_vehicle'].str.strip()
    df.loc[:, 'Festival'] = df.loc[:, 'Festival'].str.strip()
    df.loc[:, 'City'] = df.loc[:, 'City'].str.strip()

    linhas_vazias = df['Time_taken(min)'] != 'NaN '
    df = df.loc[linhas_vazias, :]
    linhas_vazias = df['Time_taken(min)'] != 'NaN'
    df = df.loc[linhas_vazias, :]
    linhas_vazias = df['Vehicle_condition'] != 'NaN '
    df = df.loc[linhas_vazias, :]
    linhas_vazias = df['Vehicle_condition'] != 'NaN'
    df = df.loc[linhas_vazias, :]
    linhas_vazias = df['Delivery_person_Age'] != 'NaN '
    df = df.loc[linhas_vazias, :]
    linhas_vazias = df['Delivery_person_Ratings'] != 'NaN '
    df = df.loc[linhas_vazias, :]
    linhas_vazias = df['Road_traffic_density'] != 'NaN '
    df = df.loc[linhas_vazias, :]
    linhas_vazias = df['Road_traffic_density'] != 'NaN'
    df = df.loc[linhas_vazias, :]
    linhas_vazias = df['multiple_deliveries'] != 'NaN '
    df = df.loc[linhas_vazias, :]
    linhas_vazias = df['Festival'] != 'NaN '
    df = df.loc[linhas_vazias, :]
    linhas_vazias = df['City'] != 'NaN '
    df = df.loc[linhas_vazias, :]
    linhas_vazias = df['City'] != 'NaN'
    df = df.loc[linhas_vazias, :]
    linhas_vazias = df['Order_Date'] != 'NaN '
    df = df.loc[linhas_vazias, :]
    
    df['Delivery_person_Age'] = df['Delivery_person_Age'].astype( int )
    df['Delivery_person_Ratings'] = df['Delivery_person_Ratings'].astype( float )
    df['Order_Date'] = pd.to_datetime( df['Order_Date'], format = '%d-%m-%Y')
    df ['Time_taken(min)'] = df ['Time_taken(min)'].apply (lambda x: x.split ('(min) ')[1])
    df ['Time_taken(min)'] = df ['Time_taken(min)'].astype(int)
    
    return df

def dist (df, fig):
    if fig==False:
        cols = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude' ]
        df ['distancia'] = df.loc [ : , cols] .apply (lambda x: haversine((x ['Restaurant_latitude'], x ['Restaurant_longitude']),(x ['Delivery_location_latitude'],x ['Delivery_location_longitude'])), axis = 1)
        dist_media = np.round (df['distancia'] .mean (), 2)

        return dist_media
    
    else:
        cols = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude' ]
        df ['distancia'] = df.loc [ : , cols]. apply (lambda x: haversine((x ['Restaurant_latitude'], x ['Restaurant_longitude']),(x ['Delivery_location_latitude'],x ['Delivery_location_longitude'])), axis = 1)
        dist_media_cidade = df.loc [ : , ['City', 'distancia']] .groupby ('City') .mean () .reset_index()

        fig = go.Figure (data=[go.Pie(labels=dist_media_cidade ['City'], values=dist_media_cidade['distancia'], pull=[0,0,0])])
        
        return fig
                 
        
def tempo (df, festival, op):
    cols = ['Time_taken(min)', 'Festival']
    df_aux = df.loc [: , cols]. groupby ('Festival'). agg ({'Time_taken(min)' : ['mean', 'std']})
    df_aux.columns = ['tempo médio (min)', 'Desvio padrão']
    df_aux = df_aux.reset_index ()
    linhas_selec = df_aux ['Festival'] == festival
    df_aux = np.round(df_aux.loc [linhas_selec , op], 2)
    
    return df_aux

def tempo_graf (df):
    cols = ['City', 'Time_taken(min)']
    df1 = df.loc [: , cols]. groupby ('City'). agg ({'Time_taken(min)' : ['mean', 'std']})
    df1.columns = ['tempo médio entrega (min)', 'desvio padrão (min)']
    df1 = df1.reset_index ()
 
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Control', x=df1['City'], y=df1['tempo médio entrega (min)'], error_y=dict(type='data', array=df1['desvio padrão (min)'])))
    fig.update_layout (barmode='group')
    
    return fig

def tempo_traf_graf (df):
    cols = ['City', 'Road_traffic_density', 'Time_taken(min)']
    df_aux = df.loc [: , cols]. groupby (['City', 'Road_traffic_density']). agg ({'Time_taken(min)' : ['mean', 'std']})
    df_aux.columns = ['tempo médio entrega (min)', 'desvio padrão (min)']
    df_aux = df_aux.reset_index ()
                
    fig=px.sunburst(df_aux, path=['City','Road_traffic_density'], values = 'tempo médio entrega (min)', color= 'tempo médio entrega (min)', color_continuous_scale='RdBu', color_continuous_midpoint=np.average(df_aux['desvio padrão (min)']))
    
    return fig

#-----------Iniciando a estrutura lógica------------------------------#

# Importando o dataframe "train.csv"
df = pd.read_csv ('train.csv')

# Limpando o dataframe

df = limpeza (df)
    

#======================
# Criação da barra lateral
#======================

# Criação do logotipo e nome da empresa
#arquivo_logo = 'logo_delivery.png'
#logo = Image.open (arquivo_logo)
image = Image.open ('logo_delivery.png')
st.sidebar.image (image, width =120)

st.sidebar.markdown ('# Cury Company')
st.sidebar.markdown ('## Fastest delivery in town')
st.sidebar.markdown ('--------')

# Criação dos filtros (inputs do usuário)

date = st.sidebar.slider ('Selecione uma data limite', value=datetime (2022, 4, 13 ), min_value=datetime (2022, 2, 11 ), max_value=datetime (2022, 4, 6 ), format='DD-MM-YYYY' )

trafic = st.sidebar.multiselect ('Selecione uma condição de trânsito',['Low', 'Medium', 'High', 'Jam'], default = ['Low', 'Medium', 'High', 'Jam'] )

st.sidebar.markdown ('--------')

st.sidebar.markdown ('## Powered by Alexandre Silva')

# Linkando os filtros com os gráficos abaixo
linhas_selecionadas = df ['Order_Date']  < date
df = df.loc [linhas_selecionadas, :]

linhas_selecionadas = df ['Road_traffic_density']. isin (trafic)
df = df.loc [linhas_selecionadas, :]

#======================
# Criação da página principal
#======================

st.header ('Marketplace - Visão restaurantes')

tab1, tab2, tab3 = st.tabs (['Visão gerencial', '', ''])

with tab1:
    with st.container():
        st.subheader  ('Métricas gerais')
              
        col1, col2, col3, col4, col5, col6 = st.columns (6)
        
        with col1:
            num_entreg_unicos = len (df.loc[: ,'Delivery_person_ID'] .unique())
            col1.metric ('Quantidade de entregadores', num_entreg_unicos)
                
        with col2:
            dist_media = dist (df, fig=False)
            col2.metric ('Distância média das entregas (km)' , dist_media)
 
        with col3:
            df_aux = tempo (df, 'Yes','tempo médio (min)')             
            col3.metric ('Tempo médio entrega c/ festival (min)' , df_aux)
                
        with col4:
            df_aux = tempo (df, 'Yes','Desvio padrão')
            col4.metric ('Desvio padrão do tempo medio entrega c/ festival (min)' , df_aux)
                
        with col5:
            df_aux = tempo (df, 'No', 'tempo médio (min)') 
            col5.metric ('Tempo médio entrega s/ festival (min)' , df_aux)
            
        with col6:
            df_aux = tempo (df, 'No', 'Desvio padrão') 
            col6.metric ('Desvio padrão do tempo medio entrega s/ festival (min)' , df_aux)
                           
    with st.container():
        st.markdown ('---')
                        
        col1, col2 = st.columns (2)
        
        with col1:
            fig = tempo_graf (df)
            st.plotly_chart(fig)
                
            
        with col2:
            cols = ['City', 'Type_of_order', 'Time_taken(min)']
            df_aux = df.loc [: , cols]. groupby (['City', 'Type_of_order']). agg ({'Time_taken(min)' : ['mean', 'std']})
            df_aux.columns = ['tempo médio (min)', 'desvio padrão (min)']
            df_aux = df_aux.reset_index ()
        
            st.dataframe (df_aux)
        
                        
    with st.container():
        st.markdown ('---')
        st.subheader  ('Distribuição do tempo')
                
        col1, col2 = st.columns (2)
        
        with col1:
                fig = dist (df, fig=True)
                st.plotly_chart(fig)
                
        with col2:
                fig = tempo_traf_graf (df)
                st.plotly_chart (fig)
                
                
        
   
        
            
                                             
