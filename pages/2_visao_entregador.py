#libraries
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
from PIL import Image
import folium
from streamlit_folium import folium_static

st.set_page_config( page_title='Visão Empresa',page_icon='🚚',layout='wide')


#====================================================
#funções
#====================================================










def top_delivers(df,top_asc):
            df_grouped = df.loc[:,['Delivery_person_ID','City','Time_taken(min)']].groupby(['City','Delivery_person_ID']).max().sort_values(['City','Time_taken(min)'],ascending=top_asc).reset_index()
            df_aux1 = df_grouped.loc[df_grouped['City'] == 'Metropolitian',].head(10)
            df_aux2 = df_grouped.loc[df_grouped['City'] == 'Urban',].head(10)
            df_aux3 = df_grouped.loc[df_grouped['City'] == 'Semi-Urban',].head(10)
            df1 = pd.concat([df_aux1,df_aux2,df_aux3])
            df1.reset_index(drop=True)
            return df1













#limpeza
def clean_code(df):
    linhas_selecionadas = df['Delivery_person_Age'] != 'NaN '
    df = df.loc[linhas_selecionadas,:].copy()
    df['Delivery_person_Age'] = df['Delivery_person_Age'].astype(int)

    #Rating
    df['Delivery_person_Ratings'] = df['Delivery_person_Ratings'].astype(float)

    #date
    df['Order_Date'] = pd.to_datetime(df['Order_Date'], format = '%d-%m-%Y')

    #Road_traffic_density
    linhas_selecionadas = df['Road_traffic_density'] != 'NaN'
    df = df.loc[linhas_selecionadas,:].copy()

    #festival
    linhas_selecionadas = df['Festival'] != 'NaN'
    df = df.loc[linhas_selecionadas,:].copy()

    #Multiple Devileries
    linhas_selecionadas = df['multiple_deliveries'] != 'NaN'
    df = df.loc[linhas_selecionadas,:].copy()

    #city
    linhas_selecionadas = df['City'] != 'NaN'
    df = df.loc[linhas_selecionadas,:].copy()
    
    ######df_aux = df_aux.loc[df_aux['City'] != 'NaN',:]               
    #####df_aux = df_aux.loc[df_aux['Road_traffic_density'] != 'NaN',:]  
    
    #####data_plot = data_plot[data_plot['City'] != 'NaN']
    #####data_plot = data_plot[data_plot['Road_traffic_density'] != 'NaN']

    # Remover espaço da string:
    df.loc[:,'ID'] = df.loc[:,'ID'].str.strip()
    df.loc[:,'Road_traffic_density'] = df.loc[:,'Road_traffic_density'].str.strip()
    df.loc[:,'Type_of_order'] = df.loc[:,'Type_of_order'].str.strip()
    df.loc[:,'Type_of_vehicle'] = df.loc[:,'Type_of_vehicle'].str.strip()
    df.loc[:,'City'] = df.loc[:,'City'].str.strip()

    #esse codigo esta fucionando apenas uma vez
    df['Time_taken(min)'] = df['Time_taken(min)'].str.extract('(\d+)').fillna('0').astype(int) 
    return df








#------------------------------------------------------
#import dataset
df = pd.read_csv('dataset/train.csv') 
df = clean_code(df)

#====================================================
#Layoult no streamilit Barra Lateral
#====================================================
st.header('Marketplace - visão Cliente')

#image_path = '/home/f/repors/FTC/imagemf.png'
image= Image.open('imagemf.png')
st.sidebar.image(image,width=120)

st.sidebar.markdown(' # Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""----""")

st.sidebar.markdown('selecione uma data limite')
data_slider =st.sidebar.slider(
    'até qual valor?',
    value=pd.datetime(2022,4,13),
    min_value=pd.datetime(2022,2,11),
    max_value=pd.datetime(2022,4,6),
    format='DD--MM--YYYY')

    
st.sidebar.markdown("""----""")

traffic_option = st.sidebar.multiselect(
    'Quais as condições do transito?',
    ['Low','Medium','High','Jam'],
    default = ['Low','Medium','High','Jam'] )
  
st.sidebar.markdown("""---""")
st.sidebar.markdown('### Powered by Comunidade DS')

#st.dataframe(df)

#fitro de data
linhas_selecionadas = df['Order_Date']< data_slider
df = df.loc[linhas_selecionadas,:]

#filtrode transito
linhas_selecionadas = df['Road_traffic_density'].isin(traffic_option)
df = df.loc[linhas_selecionadas,:]

#====================================================
#Layoult no streamilit - Centro
#====================================================    


tab1,tab2,tab3 = st.tabs( ['Visão Gerencial','-','-'] )
#tab é o quadrado grande
#e container vai ser só a parte de cima do quadrado
with tab1:
    with st.container():
        st.title('Overall Metrics')
        col1,col2,col3,col4 = st.columns(4,gap='large')
        with col1:
            maior_idade = df.loc[:,['Delivery_person_Age']].max()
            col1.metric('Maior idade',maior_idade)
            
        with col2:
            menor_idade = df.loc[:,['Delivery_person_Age']].min()
            col2.metric('menor idade',menor_idade)
            
            
            with col3:
                df_aux1 = df.loc[:,['Vehicle_condition']].max()
                col3.metric('Melhor condição ',df_aux1)
                
            with col4:
                df_aux2 = df.loc[:,['Vehicle_condition']].min()
                col4.metric('Pior condição ',df_aux2)

            
            
    with st.container():
        st.markdown("""---""")
        st.title('Avaliações')
        
        col1,col2 = st.columns(2)
        with col1:
            st.subheader('Avaliação média por entregador')
            df_grouped = df.loc[:,['Delivery_person_ID','Delivery_person_Ratings']].groupby('Delivery_person_ID').mean().reset_index()
            st.dataframe(df_grouped)
            
            
            
            
            
        with col2:
            st.subheader('Avaliação média por transito')
            df_grouped = df.loc[:,['Road_traffic_density','Delivery_person_Ratings']].groupby('Road_traffic_density').agg({'Delivery_person_Ratings':['mean','std']})
            df_grouped.columns = ['mean','std']
            df_grouped.reset_index()
            st.dataframe(df_grouped)
            
            
            st.subheader('Avaliação média por clima')
            df_grouped = df.loc[:,['Weatherconditions','Delivery_person_Ratings']].groupby('Weatherconditions').agg({'Delivery_person_Ratings':['mean','std']})
            df_grouped.columns = ['mean','std']
            df_grouped.reset_index()
            st.dataframe(df_grouped)

            
            
    with st.container():
        st.markdown("""---""")
        st.title('Velocidade de entrega')
        col1,col2 = st.columns(2)
        with col1:
            st.subheader('Top entregadores mais rapidos')
            df1 = top_delivers(df,top_asc=True)
            st.dataframe(df1)
            
            
            
        
        with col2:
            st.subheader('Top entregadores mais lentos')
            df1 = top_delivers(df,top_asc=False)
            st.dataframe(df1)

            
            
