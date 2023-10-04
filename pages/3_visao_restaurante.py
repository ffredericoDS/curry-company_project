#libraries
from datetime import datetime
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image
import folium
from streamlit_folium import folium_static

st.set_page_config( page_title='Visão Empresa',page_icon='🍽️',layout='wide')




#====================================================
#funções
#====================================================

def avg_std_time_graph(df):
            linhas_selecionadas = df['City'] != 'NaN'
            df = df.loc[linhas_selecionadas,:].copy()
            cols = ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']
            df['distance'] = df.loc[:, cols].apply(lambda x: haversine((x['Restaurant_latitude'], x['Restaurant_longitude']), (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1)
            avg_distance = df.loc[:, ['City', 'distance']].groupby('City').mean().reset_index()
            fig = go.Figure(data=[go.Pie(labels=avg_distance['City'], values=avg_distance['distance'], pull=[0, 0.1, 0])])
            return fig







def avg_std_time_delivery(df, festival, operation):
    df_grouped = df.loc[df['Festival'] == festival, ['Time_taken(min)']]
    if operation == 'mean':
        result = np.round(df_grouped.mean(), 2)
    elif operation == 'std':
        result = np.round(df_grouped.std(), 2)
    return result








def distance(df):
                cols =['Delivery_location_latitude','Delivery_location_longitude','Restaurant_latitude','Restaurant_longitude']
                df['Distance'] = df.loc[:,cols].apply(lambda x:haversine ((x['Restaurant_latitude'],x['Restaurant_longitude']) , (x['Delivery_location_latitude'],x['Delivery_location_longitude'])),axis=1)
                avg_distance = np.round(df['Distance'].mean(),2)
                return avg_distance












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
#image_path = '/home/f/repors/FTC/imagemf.png'
image= Image.open('imagemf.png')
st.sidebar.image(image,width=120)

st.sidebar.markdown(' # Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""----""")

st.sidebar.markdown('selecione uma data limite')
data_slider =st.sidebar.slider(
    'até qual valor?',
    value=datetime(2022,4,13),
    min_value=datetime(2022,2,11),
    max_value=datetime(2022,4,6),
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
st.title('Visão restaurante')

tab1,tab2,tab3 = st.tabs( ['Visão Restaurante','-','-'] )
with tab1:
    with st.container():
        col1,col2,col3,col4,col5,col6 = st.columns(6)
        with col1:
            df_grouped = df['Delivery_person_ID'].nunique()
            col1.metric('Entregadores ',df_grouped)
            
            
            
        with col2:
            avg_distance = distance(df)
            col2.metric('Distancia média',avg_distance)



        
        with col3:
            df1 = avg_std_time_delivery(df, 'Yes ', 'mean')
            col3.metric('time mean c/ ftv', df1)
    
        with col4:
            df1 = avg_std_time_delivery(df, 'Yes ', 'std')
            col4.metric('std c/ festial', df1)
    
        with col5:
            df1 = avg_std_time_delivery(df, 'No ', 'mean')
            col5.metric('Time mean s/ ftv', df1)
    
        with col6:
            df1 = avg_std_time_delivery(df, 'No ', 'std')
            col6.metric('std s/ festial', df1)
            
            
            
            
            
                
with st.container():
    
    #faz direto
    col1,col2 = st.columns(2)
    with col1:
        st.markdown('# distance mean from delivery.')
        fig = avg_std_time_graph(df)
        st.plotly_chart(fig)
        
    with col2:
        st.title('mean by city and traffic')
        df_grouped = df.loc[:, ['City', 'Road_traffic_density', 'Time_taken(min)']].groupby(['City', 'Road_traffic_density']).agg({'Time_taken(min)': ['mean', 'std']})
        df_grouped.columns = ['mean', 'std']
        df_grouped = df_grouped.reset_index()

        fig = px.sunburst(df_grouped, path=['City', 'Road_traffic_density'], values='mean',
                          color=df_grouped['std'],  # Usando a coluna 'std' para definir as cores
                          color_continuous_scale='RdBu',  # Escolha uma escala de cores
                          )

        st.plotly_chart(fig)
        
    
    
with st.container():
    col1,col2 = st.columns(2)
    with col1:
        st.title('mean/std time for city')
        cols = ['City', 'Time_taken(min)']
        df_aux = df.loc[:, cols].groupby('City').agg({'Time_taken(min)': ['mean', 'std']})
        df_aux.columns = ['mean', 'std']
        df_aux = df_aux.reset_index()  # Adicione esta linha para redefinir o índice
        fig = go.Figure(data=[go.Bar(
            name='Control',
            x=df_aux['City'],
            y=df_aux['mean'],  # Use 'mean' em vez de 'avg_time'
            error_y=dict(type='data', array=df_aux['std'])
        )])
        fig.update_layout(barmode='group')
        st.plotly_chart(fig)
        
    with col2:
        st.title('graph time mean/std for city')
        df_grouped = df.loc[:,['City','Type_of_order','Time_taken(min)']].groupby(['City','Type_of_order']).agg({'Time_taken(min)':['mean','std']})
        df_grouped.columns = ['mean','std']
        df_grouped.reset_index(drop=False)
        st.dataframe(df_grouped)

