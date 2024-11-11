#------Importando as bibliotecas-------#
import datetime
import pandas as pd
import streamlit as st
from PIL import Image
#from haversine import haversine
import plotly.express as px
import folium
from streamlit_folium import folium_static
from datetime import datetime



st.set_page_config (page_title='Visão entregadores', page_icon='', layout='wide') 

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

def top_entreg_cid (df, top_asc):
    
    df1 = (df.loc [: , ['Delivery_person_ID', 'City', 'Time_taken(min)']]
                   .groupby (['City', 'Delivery_person_ID'])
                   .mean()
                   .sort_values(['City', 'Time_taken(min)'], ascending=top_asc).reset_index())
    df2 = df1.loc [df1 ['City'] == 'Metropolitian', :]. head (10)
    df3 = df1.loc [df1 ['City'] == 'Urban', :]. head (10)
    df4 = df1.loc [df1 ['City'] == 'Semi-urban', :]. head (10)
    df5 = pd.concat ([df2,df3,df4]).reset_index(drop=True)
    
    return df5

#-----------Iniciando a estrutura lógica------------------------------#

# Importando o dataframe "train.csv"
df = pd.read_csv ('train.csv')

# Limpando o dataframe

df = limpeza (df)
    

#============================
# Criando a barra lateral
#============================

# Importando o logotipo da empresa 'logo_delivery.png' 
#arquivo='logo_delivery.png'
#logo=Image.open (arquivo)
image = Image.open ('logo_delivery.png')
st.sidebar.image (image, width =120)

st.sidebar.markdown ('# Cury Company')
st.sidebar.markdown ('## Fastest delivery in town')
st.sidebar.markdown ('--------')

# Criando os filtros (inputs do usuário)
date = st.sidebar.slider ('Selecione uma data limite', value=datetime (2022, 4, 13 ), min_value=datetime (2022, 2, 11 ), max_value=datetime (2022, 4, 6 ), format='DD-MM-YYYY' )

trafic = st.sidebar.multiselect ('Selecione uma condição de trânsito',['Low', 'Medium', 'High', 'Jam'], default = ['Low', 'Medium', 'High', 'Jam'] )

st.sidebar.markdown ('--------')

st.sidebar.markdown ('## Powered by Alexandre Silva')

# Linkando os filtros com os gráficos abaixo
linhas_selecionadas = df ['Order_Date'] <  date 
df = df.loc [linhas_selecionadas, :]

linhas_selecionadas = df ['Road_traffic_density']. isin (trafic)
df = df.loc [linhas_selecionadas, :]



#=============================
# Criação da página principal
#=============================

st.header ('Marketplace - Visão entregadores')

tab1, tab2, tab3 = st.tabs (['Visão gerencial', '', ''])

with tab1:
    with st.container():
        st.subheader  ('Métricas gerais')
              
        col1, col2, col3, col4 = st.columns (4)
        
        with col1:
            maior_idade = df.loc [: , 'Delivery_person_Age'].max()
            col1.metric ('A maior idade é', maior_idade)
            
        with col2:
            menor_idade = df.loc [: , 'Delivery_person_Age'].min()
            col2.metric ('A menor idade é', menor_idade)
            
        with col3:
            melhor_cond = df.loc [: , 'Vehicle_condition'].max()
            col3.metric ('A melhor condição de veículo é', melhor_cond)
            
        with col4:
            pior_cond = df.loc [: , 'Vehicle_condition'].min()
            col4.metric ('A pior condição de veículo é', pior_cond)
            
    with st.container():
        st.markdown ('---')
        st.subheader  ('Avaliações')
        
        col1, col2 = st.columns (2)
        
        with col1:
            st.markdown  ('Avaliação média por entregador')
            aval_med_entreg = df.loc [: , ['Delivery_person_Ratings', 'Delivery_person_ID']].groupby ('Delivery_person_ID').mean().reset_index()
            st.dataframe (aval_med_entreg)
            
        with col2:
            st.markdown  ('Avaliação média e o desvio padrão por tipo de trânsito')
            med_desv_traf = (df.loc [: , ['Delivery_person_Ratings', 'Road_traffic_density']].groupby ('Road_traffic_density').agg ({'Delivery_person_Ratings': ['mean','std']}))
            med_desv_traf.columns = ['Média', 'Desvio padrão']
            med_desv_traf = med_desv_traf.reset_index()
            st.dataframe (med_desv_traf)
                
            st.markdown  ('Avaliação média e o desvio padrão por tipo de clima')
            med_desv_clim = (df.loc [: , ['Delivery_person_Ratings', 'Weatherconditions']].groupby ('Weatherconditions')
            .agg ({'Delivery_person_Ratings': ['mean','std']}))
            med_desv_clim.columns = ['Média', 'Desvio padrão']
            med_desv_clim = med_desv_clim.reset_index()
            st.dataframe (med_desv_clim)
            
    with st.container():
        st.markdown ('---')
        st.subheader  ('Velocidade de entrega')
        
        col1, col2 = st.columns (2)
        
        with col1:
            st.markdown  ('Entregadores mais rápidos')
            df5 = top_entreg_cid (df, top_asc=True)
            st.dataframe (df5)
            
        with col2:
            st.markdown  ('Entregadores mais lentos')
            df5 = top_entreg_cid (df, top_asc=False)
            st.dataframe (df5)
            
            
            
