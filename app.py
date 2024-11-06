
import datetime
import pandas as pd
import streamlit as st
from PIL import Image
#from haversine import haversine
import plotly.express as px
import folium
from streamlit_folium import folium_static

st.set_page_config (page_title='Visão empresa', page_icon='', layout='wide')


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

def pedidos_data (df):

    pedidos = [ 'ID' , 'Order_Date']
    pedidos1 = df.loc [: , pedidos].groupby(['Order_Date']). count().reset_index()
    fig = px.bar (pedidos1 , x = 'Order_Date' , y = 'ID' )

    return fig

def pedidos_traf (df):
    pedidos1 = [ 'ID' , 'Road_traffic_density']
    pedidos1 = df.loc [: , pedidos1].groupby(['Road_traffic_density']). count().reset_index()
    pedidos1 ['perc']=  pedidos1 ['ID'] / pedidos1 ['ID'].sum()
    fig = px.pie (pedidos1 , values = 'perc' , names = 'Road_traffic_density' )

    return fig

def pedidos_traf_cidade (df):
    pedidos1 = [ 'ID' , 'City', 'Road_traffic_density']
    pedidos1 = df.loc [: , pedidos1].groupby(['Road_traffic_density', 'City']). count().reset_index()
    fig = px.scatter (pedidos1 , x = 'City', y = 'Road_traffic_density' , size = 'ID', color = 'City')

    return fig

def pedidos_semana (df):
    df ['Week'] = df ['Order_Date'] .dt.strftime ('%U')
    pedidos = [ 'ID' , 'Week']
    pedidos1 = df.loc [: , pedidos].groupby(['Week']). count().reset_index()
    fig = px.line (pedidos1 , x = 'Week' , y = 'ID' )

    return fig

def pedidos_semana_entreg (df):
    ped_sem = [ 'ID' , 'Week']
    ped_entreg = ['Delivery_person_ID', 'Week']
    pedidos2 = df.loc [: , ped_sem].groupby('Week'). count().reset_index()
    pedidos3 = df.loc [: , ped_entreg].groupby(['Week']). nunique().reset_index()
    pedidos4 = pd.merge (pedidos2, pedidos3, how='inner')
    pedidos4 ['Pedidos por entregador na semana'] = pedidos4 ['ID'] / pedidos4 ['Delivery_person_ID']
    fig = px.line (pedidos4 , x = 'Week', y = 'Pedidos por entregador na semana')

    return fig

def mapa (df):
    local_traf = df.loc [: , ["Road_traffic_density", "City","Delivery_location_latitude", "Delivery_location_longitude"]].groupby(['Road_traffic_density', 'City']). median().reset_index()

    map = folium.Map()

    for index, location_info in local_traf.iterrows ():
        folium.Marker ([location_info ['Delivery_location_latitude'],
                        location_info ['Delivery_location_longitude']],
                        popup = location_info [['City', 'Road_traffic_density']]). add_to (map)

    folium_static (map, width=1024, height = 600)

    return


#-----------Iniciando a estrutura lógica------------------------------

# Importando o dataframe "train.csv"
df = pd.read_csv ('/Users/alexandremarquesdasilva/Trabalho-conclus-o-Analisando-dados-com-Python/train.csv')

# Limpando o dataframe

df = limpeza (df)


#============================
# Criando a barra lateral
#============================

# Importando o logotipo da empresa 'logo_delivery.png'
arquivo='/Users/alexandremarquesdasilva/Trabalho-conclus-o-Analisando-dados-com-Python/logo_delivery.png'
logo=Image.open (arquivo)
st.sidebar.image (logo, width =120)

st.sidebar.markdown ('# Cury Company')
st.sidebar.markdown ('## Fastest delivery in town')
st.sidebar.markdown ('--------')

# Criando os filtros (inputs do usuário)
date = st.sidebar.slider ('Selecione uma data limite', value=datetime.datetime (2022, 4, 13 ), min_value=datetime.datetime (2022, 2, 11 ), max_value=datetime.datetime (2022, 4, 6 ), format='DD-MM-YYYY' )

trafic = st.sidebar.multiselect ('Selecione uma condição de trânsito',['Low', 'Medium', 'High', 'Jam'], default = ['Low', 'Medium', 'High', 'Jam'] )

st.sidebar.markdown ('--------')

st.sidebar.markdown ('## Powered by Alexandre Silva')

# Linkando os filtros com os gráficos abaixo
linhas_selecionadas = df ['Order_Date'] <  date
df = df.loc [linhas_selecionadas, :]

linhas_selecionadas = df ['Road_traffic_density']. isin (trafic)
df = df.loc [linhas_selecionadas, :]



#============================
# Criando a página principal
#============================

st.header ('Marketplace - Visão empresa')

tab1, tab2, tab3 = st.tabs (['Visão estratégica', 'Visão tática', 'Visão geográfica'])
with tab1:
    with st.container():
        st.markdown ('Distribuição dos pedidos por data')
        fig = pedidos_data (df)
        st.plotly_chart (fig, use_container_width=True)

    with st.container():
        col1, col2 = st.columns (2)
        with col1:
            st.markdown ('Distribuição dos pedidos por tipo de tráfego')
            fig = pedidos_traf (df)
            st.plotly_chart (fig, use_container_width=True)

        with col2:
            st.markdown ('Distribuição dos pedidos por cidade e tipo de tráfego')
            fig = pedidos_traf_cidade(df)
            st.plotly_chart (fig, use_container_width=True)

with tab2:
    with st.container():
        st.markdown ('Quantidade de pedidos por semana')
        fig = pedidos_semana (df)
        st.plotly_chart (fig, use_container_width=True)

    with st.container():
        st.markdown ('Quantidade de pedidos por entregador por semana')
        fig = pedidos_semana_entreg (df)
        st.plotly_chart (fig, use_container_width=True)

with tab3:
    st.markdown ('Localização central de cada cidade por tipo de tráfego')
    mapa (df)

