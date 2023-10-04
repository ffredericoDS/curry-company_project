#librariess
from datetime import datetime
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
from PIL import Image
import folium
from streamlit_folium import folium_static


st.set_page_config( page_title='Visão Empresa',page_icon='📈',layout='wide')

#====================================================
#funcões
#====================================================
#limpeza


def coutry_maps(df):
    
        columns = [
        'City',
        'Road_traffic_density',
        'Delivery_location_latitude',
        'Delivery_location_longitude'
        ]
        columns_grouped = ['City', 'Road_traffic_density']
        data_plot = df.loc[:, columns].groupby( columns_grouped ).median().reset_index()
        

        # Desenhar o mapa
        map_ = folium.Map( zoom_start=11 )
        for index, location_info in data_plot.iterrows():
            folium.Marker( [location_info['Delivery_location_latitude'],
            location_info['Delivery_location_longitude']],
            popup=location_info[['City', 'Road_traffic_density']] ).add_to( map_ )
        folium_static(map_)
        







def order_share_by_week(df):
                #st.markdown('# typede'
                df_aux1 = df.loc[:, ['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()
                df_aux2 = df.loc[:, ['Delivery_person_ID', 'week_of_year']].groupby('week_of_year').nunique().reset_index()

                # Renomeie a coluna 'Delivery_person_ID' para evitar conflito durante a mesclagem
                df_aux2 = df_aux2.rename(columns={'Delivery_person_ID': 'Unique_Delivery_Persons'})

                df_aux = pd.merge(df_aux1, df_aux2, on='week_of_year', how='inner')
                df_aux['order_by_delivery'] = df_aux['ID'] / df_aux['Unique_Delivery_Persons']
                fig=px.line(df_aux, x='week_of_year', y='order_by_delivery')

                return fig
       # gráfico

                        #df_aux2 = df.loc[:, ['Delivery_person_ID', 'week_of_year']].groupby( 'week_of_year').nunique().reset_index()
                #df_aux = pd.merge( df_aux1, df_aux2, how='inner' )
                #df_aux['order_by_delivery'] = df_aux['ID'] / df_aux['Delivery_person_ID']
                # gráfico
                #fig=px.line( df_aux, x='week_of_year', y='order_by_delivery' )
                #st.plotly_chart(fig,use_container_widht=True)












def order_by_week(df):
            df['week_of_year'] = df['Order_Date'].dt.strftime('%U')
            df_aux = df.loc[:,['week_of_year','ID']].groupby('week_of_year').count().reset_index()
            fig=px.line(df_aux,x='week_of_year',y='ID')
            return fig
            




def traffic_order_city(df):
                df_aux = df.loc[:,['ID','City','Road_traffic_density']].groupby(['City','Road_traffic_density']).count().reset_index()
                fig=px.scatter(df_aux,x='City',y='Road_traffic_density',size='ID',color='City')
                return fig








def traffic_order_share(df):
                df_aux = df.loc[:, ['ID', 'Road_traffic_density']].groupby( 'Road_traffic_density' ).count().reset_index()
                df_aux = df_aux.loc[df_aux['Road_traffic_density'] != 'NaN' ,:]
                df_aux['entregas_perc'] = 100 * ( df_aux['ID'] / df_aux['ID'].sum() )
                fig=px.pie(df_aux,values='entregas_perc',names='Road_traffic_density')
                return fig








def order_metric(df):
            df_aux = df.loc[:,['Order_Date','ID']].groupby('Order_Date').count().reset_index()
            fig = px.bar(df_aux,x='Order_Date',y='ID')
            return fig
            
            
            
            
            
            
            
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


#====================================================
#inicio estrutur logica do codigo 
#====================================================
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
tab1,tab2,tab3 = st.tabs(['Visão Gerencial','Visão Tatica','Visão Geografica'])

with tab1:
    #criar container
    with st.container():
        fig=order_metric(df)
        st.markdown('# Orders by day')
        st.plotly_chart(fig,use_coontainer_width=True)
        
        
    
            
            
            

    #criar coluna horizontal
    with st.container():
        col1,col2 = st.columns(2)
        with col1:
            fig = traffic_order_share(df)
            st.header('Traffic Order Share')
            st.plotly_chart(fig,use_container_width=True)

            
            
            
        with col2:
            st.header('Traffic Order City')
            fig = traffic_order_city(df)
            st.plotly_chart(fig,use_container_widht=True)
            
            
            
                
                
                
                
                
                
                

with tab2:
    with st.container():
        st.markdown('# Order by week')
        fig=order_by_week(df)
        st.plotly_chart(fig,use_container_widht=True)
        

        
    
            
            
            
            
        with st.container():
            st.markdown('# Order by delivery person')
            fig= order_share_by_week(df)
            st.plotly_chart(fig,use_container_widht=True)
            
            

         




    
    
    
    
    
    
            
with tab3:
    st.markdown('# Coutry map')
    coutry_maps(df)
    
    
    
    
    
