import streamlit as st
from PIL import Image
from datetime import datetime


st.set_page_config(
    page_title='Home',
    page_icon='🎲'
)

#image_path = '/home/f/repors/FTC/' @##
image = Image.open('imagemf.png')
st.sidebar.image(image,width=120)

st.sidebar.markdown(' # Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""----""")

st.write('# Curry Company Growth Dashboard')
st.markdown(
    """
    # Growth Dashboard
    O Growth Dashboard foi construído para acompanhar as métricas de crescimento dos entregadores e restaurantes.

    ## Como utilizar este Growth Dashboard?
    - **Visão Empresa**:
        - Visão Gerencial: Métricas gerais de comportamento
        - Visão Tática: Indicadores semanais de crescimento
        - Visão Geográfica: Insights de geolocalização

    - **Visão Entregador**:
        - Acompanhamento dos indicadores semanais de crescimento

    - **Visão Restaurante**:
        - Indicadores semanais de crescimento dos restaurantes

    ## ASK FOR HELP
    Você pode entrar em contato com o nosso time de Data Science no Discord:
    - @meigarom
    """
)


import os

current_directory = os.getcwd()
st.write(f"Current Directory: {current_directory}")
