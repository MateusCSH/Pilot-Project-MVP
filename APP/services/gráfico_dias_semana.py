
import streamlit as st
import plotly.express as px
import pandas as pd

def dias_semana(df):


    dias_tradução = {
    "Monday": "Segunda-feira",
    "Tuesday": "Terça-feira",
    "Wednesday": "Quarta-feira",
    "Thursday": "Quinta-feira",
    "Friday": "Sexta-feira",
    "Saturday": "Sábado",
    "Sunday": "Domingo"
    }

    # Ordem correta dos dias em português
    ordem_dias = [
        "Segunda-feira", "Terça-feira", "Quarta-feira",
        "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"
    ]

    df["Data"] = pd.to_datetime(df["Data"], format="%d/%m/%Y", errors="coerce")
    # Criar coluna com dias em português
    df["Dia_Semana"] = df["Data"].dt.day_name().map(dias_tradução)

    # Contagem de registros por dia (já ordenada)
    contagem = df["Dia_Semana"].value_counts()\
                .reindex(ordem_dias, fill_value=0)\
                .reset_index()  # Resetar índice para virar coluna

    # Renomear colunas para Plotly
    contagem.columns = ["Dia da Semana", "Total de Registros"]

    # Criar gráfico
    fig = px.bar(
        contagem,
        x="Dia da Semana",
        y="Total de Registros",
        title="Registros por Dia da Semana",
        labels={"Dia da Semana": "Dia", "Total de Registros": "Número de Registros"},
        color="Dia da Semana",
        text="Total de Registros"
    )

    # Forçar ordem cronológica no eixo X
    fig.update_layout(
        xaxis={'categoryorder': 'array', 'categoryarray': ordem_dias}
    )

    st.plotly_chart(fig)