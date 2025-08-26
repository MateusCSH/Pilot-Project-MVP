
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from services.conversao_hrs import conversor
from services.gráfico_bar_vert import grafico_barras
from services.gráfico_dias_semana import dias_semana

def monitor():

    file = st.sidebar.file_uploader('Baixar arquivo', type=['csv'])

    if file is not None:
        df = pd.read_csv(file, sep=',')
        df = df[["Nome", "Data", "Motivo", "Horário de entrada", "Horário de Saída"]]

        conversor(df)
        df = df[["Nome", "Data", "Motivo", "Horário de entrada", "Horário de Saída", "Duração (hh:mm)"]]

        # Converter "Duração (hh:mm)" para timedelta
        df['Duração'] = df['Duração (hh:mm)'].apply(lambda x: timedelta(hours=int(x.split(':')[0]), minutes=int(x.split(':')[1])))

        df_filt = df.groupby('Nome',)['Duração'].sum().reset_index()
        df_filt['Horas'] = df_filt['Duração'].apply(lambda td: td.total_seconds() / 3600)
        df_filt['Horas (hh:mm)'] = df_filt['Horas'].apply(lambda h: f"{int(h):02}:{int((h % 1) * 60):02}")


        st.markdown(f"""<div class = 'marcacao'>
                        <p>RELATÓRIO GRÁFICO TEMPO DE PERMANÊNCIA</p>
                        </div>""", unsafe_allow_html=True)
        grafico_barras(df_filt)

        # dias mais frequentes.
        st.markdown(f"""<div class = 'marcacao'>
                        <p>Dias mais frequentes</p>
                        </div>""", unsafe_allow_html=True)
        dias_semana(df)