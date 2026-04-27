import streamlit   as st              #Framework
import pandas as pd                   #Biblioteca para trabalhar o excel
import plotly.express as px           #Biblioteca para ajudar com os gráficos

def main():
    data = pd.read_excel('Base.xlsx', sheet_name='Base')
    titulo = 'Dashboard - Projeto Vendas'
    st.set_page_config(page_title=titulo, layout='wide')
    st.title(titulo)

    ano = data['Ano'].unique()
    paises = data['País'].unique()

    filtro_ano = st.sidebar.selectbox('Selecione o Ano:', options=['Todos'] + sorted(ano), index=0)
    filtro_pais = st.sidebar.selectbox('Selecione o País:', options=['Todos'] + sorted(paises), index=0)

    data_filtrada = data.copy()
    if filtro_ano != 'Todos':
        data_filtrada = data_filtrada[data_filtrada['Ano'] ==  filtro_ano]
    if filtro_pais !='Todos':
        data_filtrada = data_filtrada[data_filtrada['País'] == filtro_pais]

main()
