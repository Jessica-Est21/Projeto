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

    gf_lucro_segmento = px.bar(
        data_filtrada.groupby('Segmento')['Lucro'].sum().reset_index(),
        x='Sgmento', y='Lucro',
        title='Lucro Por Segmento',
        color='Segmento',
        text_auto=True
)
    gf_lucro_segmento.update_layout(showlegend=False)

    gf_vendas_tempo = px.line(
        data_filtrada.groupby('Data')['Vendas Brutas'].sum().reset_index(),
        x='Data', y='Vendas Brutas',
        title='Vendas Brutas ao Longo do Tempo',
        markers=True
    )

    gf_produtos_vencidos = px.pie(
        data_filtrada.groupby('Produto')['Unidade Vendidas'].sum.reset_index(),
        values='Unidade Vendidas', names='Produto',
        title='Distribuição d Produtos Vendidos',
    )

    custo_lucro_data = data_filtrada(['Segmento'])[['COGS','Lucro']].sum().reset_index().melt(
        id_vars = 'Segmento', value_vars = ['COGS', 'Lucro'])
    custo_lucro_data['value_formatado'] = custo_lucro_data['value'].apply(lambda x:f'R$ {x:.2}')

    gf_custo_lucro = px.bar(
        custo_lucro_data,
        x='Segmento', y='value',
        title='Relação Entre Custo e Lucro',
        color='variable',
        barmode='group',
        text_auto=True
    )

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    col1.plotly_chart(gf_lucro_segmento, use_container_width=True)
    col2.plotly_chart(gf_vendas_tempo, use_container_width=True)
    col3.plotly_chart(gf_produtos_vencidos,use_container_width=True)
    col4.plotly_chart(gf_custo_lucro, use_container_width=True)

main()
