
import streamlit as st


def info_por_motivo(df, motivo):
    df_filtrado = df[df['Motivo'] == motivo]

    total_horas = df_filtrado['Horas (decimais)'].sum()
    total_dias = df_filtrado['Data'].nunique()
    media_horas = df_filtrado['Horas (decimais)'].mean()
    max_horas = df_filtrado['Horas (decimais)'].max()
    min_horas = df_filtrado['Horas (decimais)'].min()

    st.subheader(f"📈 Informações por Motivo: {motivo}")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("⏱️ Horas Totais", f"{total_horas:.2f} h")
    col2.metric("📅 Dias Registrados", total_dias)
    col3.metric("📈 Média por Dia", f"{media_horas:.2f} h")
    col4.metric("⬆️ Máximo por Dia", f"{max_horas:.2f} h")
    col5.metric("⬇️ Mínimo por Dia", f"{min_horas:.2f} h")