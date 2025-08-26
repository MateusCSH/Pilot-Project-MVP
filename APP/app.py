import pandas as pd
from datetime import datetime
import streamlit as st
from app_monitor import monitor
from babel.dates import format_datetime

#with open('style.css', encoding='utf8') as r:
    #st.markdown(f"<style>{r.read()}</style>", unsafe_allow_html=True)

# CD MONITORES -> ENTRAR NA PASTA

# st.sidebar.text('Selecione a opção:')
option = st.sidebar.selectbox('Selecione a opção:', options=['Ficha de Atendimento','Monitores'])

if option == 'Ficha de Atendimento':



    import pandas as pd
    import streamlit as st
    from datetime import datetime, timedelta
    import altair as alt

    file = st.sidebar.file_uploader('Baixar arquivo', type=['csv'])

    if file is not None:

        df = pd.read_csv(file, sep=',')
        df = df[["Nome", "Data", "Motivo", "Horário de entrada", "Horário de Saída"]]

        # Conversões
        df['Data'] = pd.to_datetime(df['Data'], dayfirst=True)
        df['Horário de entrada'] = pd.to_datetime(df['Horário de entrada'], format='%H:%M:%S').dt.time
        df['Horário de Saída'] = pd.to_datetime(df['Horário de Saída'], format='%H:%M:%S').dt.time

        # Função para unir intervalos sobrepostos
        def unir_intervalos(intervalos):
            intervalos = sorted(intervalos)
            unidos = [intervalos[0]]
            for inicio, fim in intervalos[1:]:
                ult_inicio, ult_fim = unidos[-1]
                if inicio <= ult_fim:
                    unidos[-1] = (ult_inicio, max(ult_fim, fim))
                else:
                    unidos.append((inicio, fim))
            return unidos

        # Calcular o total de horas por dia
        horas_por_dia = {}

        for data, grupo in df.groupby('Data'):
            intervalos = []
            for _, linha in grupo.iterrows():
                entrada = datetime.combine(data, linha['Horário de entrada'])
                saida = datetime.combine(data, linha['Horário de Saída'])
                intervalos.append((entrada, saida))
            
            unificados = unir_intervalos(intervalos)
            total = sum([(fim - ini) for ini, fim in unificados], timedelta())
            horas_por_dia[data] = total

        # Criar a nova coluna com horas de funcionamento por dia
        df['Horas de Funcionamento no Dia'] = df['Data'].map(horas_por_dia)




        # Criando dataframe apenas com dias únicos
        dias_df = df.drop_duplicates('Data')[['Data', 'Horas de Funcionamento no Dia', 'Motivo']].copy()
        dias_df['Horas (decimais)'] = dias_df['Horas de Funcionamento no Dia'].dt.total_seconds() / 3600
        dias_df['Dia da Semana'] = dias_df['Data'].apply(lambda x: format_datetime(x, "EEEE", locale='pt_BR'))  # para nomes em português



        
        total_horas = dias_df['Horas (decimais)'].sum()
        total_dias = dias_df['Data'].nunique()
        media_por_dia = total_horas / total_dias if total_dias else 0
        # media_por_dia = dias_df['Horas (decimais)'].mean()

        
        st.title("📊 Painel de Monitoramento do Espaço")

        # col1, col2, col3 = st.columns(3)
        # col1.metric("⏱️ Horas Totais", f"{total_horas:.2f} h")
        # col2.metric("📅 Dias Registrados", total_dias)
        # col3.metric("📈 Média por Dia", f"{media_por_dia:.2f} h")


        total_horas = dias_df['Horas (decimais)'].sum()

        total_dias = dias_df['Data'].nunique()

        media_horas = dias_df['Horas (decimais)'].mean()

        max_horas = dias_df['Horas (decimais)'].max()

        min_horas = dias_df['Horas (decimais)'].min()

        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric("⏱️ Horas Totais", f"{total_horas:.2f} h")
        col2.metric("📅 Dias Registrados", total_dias)
        col3.metric("📈 Média por Dia", f"{media_horas:.2f} h")
        col4.metric("⬆️ Máximo por Dia", f"{max_horas:.2f} h")
        col5.metric("⬇️ Mínimo por Dia", f"{min_horas:.2f} h")






        # ----- GRÁFICO POR DIA DA SEMANA -----
        st.subheader("Distribuição de Horas por Dia da Semana")

        # ordem dos dias 
        ordem_dias = ['segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 
                    'sexta-feira', 'sábado', 'domingo']

        # Agrupando
        soma_por_dia_semana = dias_df.groupby('Dia da Semana')['Horas (decimais)'].sum().reset_index()

        # Ordenar do maior para o menor
        soma_por_dia_semana = soma_por_dia_semana.sort_values(by='Horas (decimais)', ascending=False)


        # Gráfico de barras
        grafico_soma = (
            alt.Chart(soma_por_dia_semana)
            .mark_bar()
            .encode(
                x=alt.X('Dia da Semana:N', sort=ordem_dias, title='Dia da Semana', axis=alt.Axis(labelFontSize=14, titleFontSize=16)),
                y=alt.Y('Horas (decimais):Q', title='Horas', axis=alt.Axis(labelFontSize=14, titleFontSize=16)),
                color='Dia da Semana:N',
                tooltip=['Dia da Semana:N', alt.Tooltip('Horas (decimais):Q', title='Horas Totais', format='.2f')]
            )
            .properties(width=700, height=400)
        )

        # rótulos acima das barras
        rotulos = (
            alt.Chart(soma_por_dia_semana)
            .mark_text(dy=-10, color='white', fontSize=15)
            .encode(
                x=alt.X('Dia da Semana:N', sort=ordem_dias),
                y='Horas (decimais):Q',
                text=alt.Text('Horas (decimais):Q', format='.2f')
            )
        )

        # gráfico
        st.altair_chart(grafico_soma + rotulos, use_container_width=True)




        # MOSTRANDO POR MÊS
        import locale
        locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil.1252')
        dias_df['Mes_Ano'] = dias_df['Data'].dt.strftime('%Y-%B').str.capitalize()

        metrics_mes = dias_df.groupby('Mes_Ano').agg(
            Horas_Totais=('Horas (decimais)', 'sum'),
            Dias_Registrados=('Data', 'nunique'),
            Media_Horas_Por_Dia=('Horas (decimais)', 'mean'),
            Max_Horas_Por_Dia=('Horas (decimais)', 'max'),
            Min_Horas_Por_Dia=('Horas (decimais)', 'min')
        ).reset_index()


        metrics_mes = metrics_mes.sort_values(by='Mes_Ano')  # Ordenar cronologicamente

        st.subheader("##")
        st.subheader("📆 Informações por Mês")

        for _, row in metrics_mes.iterrows():
            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric(f"Mês: {row['Mes_Ano']}", "")
            col2.metric("⏱️ Horas Totais", f"{row['Horas_Totais']:.2f} h")
            col3.metric("📅 Dias Registrados", int(row['Dias_Registrados']))
            col4.metric("📈 Média por Dia", f"{row['Media_Horas_Por_Dia']:.2f} h")
            col5.metric("⬆️ Máximo", f"{row['Max_Horas_Por_Dia']:.2f} h")
            st.write("---")





        import altair as alt


        # Gráfico de barras principais
        grafico_barras = (
            alt.Chart(metrics_mes)
            .mark_bar()
            .encode(
                x=alt.X('Mes_Ano:N', title='Mês', axis=alt.Axis(labelFontSize=14, titleFontSize=16)),
                y=alt.Y('Horas_Totais:Q', title='Horas Totais', axis=alt.Axis(labelFontSize=14, titleFontSize=16)),
                color='Mes_Ano:N',
                tooltip=[
                    alt.Tooltip('Mes_Ano:N', title='Mês'),
                    alt.Tooltip('Horas_Totais:Q', title='Horas Totais', format='.2f')
                ]
            )
            .properties(width=700, height=400)
        )

        # Rótulos de texto sobre as barras
        rotulos = (
            alt.Chart(metrics_mes)
            .mark_text(
                dy=-10,  # deslocamento para cima
                fontSize=15,
                color='white'
            )
            .encode(
                x=alt.X('Mes_Ano:N'),
                y='Horas_Totais:Q',
                text=alt.Text('Horas_Totais:Q', format='.1f')
            )
        )

        # Combinar gráfico + rótulos
        st.altair_chart(grafico_barras + rotulos, use_container_width=True)
        



if option == 'Monitores':

    monitor()


    # total_horas = dias_df['Horas (decimais)'].sum()
    # total_dias = dias_df['Data'].nunique()
    # media_horas = dias_df['Horas (decimais)'].mean()
    # max_horas = dias_df['Horas (decimais)'].max()
    # min_horas = dias_df['Horas (decimais)'].min()

    # st.subheader("📈 Informações Gerais do Espaço")
    # col1, col2, col3, col4, col5 = st.columns(5)
    # col1.metric("⏱️ Horas Totais", f"{total_horas:.2f} h")
    # col2.metric("📅 Dias Registrados", total_dias)
    # col3.metric("📈 Média por Dia", f"{media_horas:.2f} h")
    # col4.metric("⬆️ Máximo por Dia", f"{max_horas:.2f} h")
    # col5.metric("⬇️ Mínimo por Dia", f"{min_horas:.2f} h")

    # st.text(dias_df.head())


    #SEPARANDO POR CATEGORIA
    # PEQUENO ERRO

    # USANDO SERVIÇOS
    # st.subheader('##')
    # st.subheader('##')
    # st.subheader('##')

    # from services.motivos import info_por_motivo
    # motivos = dias_df['Motivo'].unique()
    # for motivo in motivos:
    #     print(motivo)
    #     info_por_motivo(dias_df, motivo)


    # df_moni = dias_df[dias_df['Motivo'] == 'Monitoria']

    # total_horas = df_moni['Horas (decimais)'].sum()
    # total_dias = df_moni['Data'].nunique()
    # media_horas = df_moni['Horas (decimais)'].mean()
    # max_horas = df_moni['Horas (decimais)'].max()
    # min_horas = df_moni['Horas (decimais)'].min()

    # st.subheader("📈 Informações por motivo: Monitoria ")
    # col1, col2, col3, col4, col5 = st.columns(5)
    # col1.metric("⏱️ Horas Totais", f"{total_horas:.2f} h")
    # col2.metric("📅 Dias Registrados", total_dias)
    # col3.metric("📈 Média por Dia", f"{media_horas:.2f} h")
    # col4.metric("⬆️ Máximo por Dia", f"{max_horas:.2f} h")
    # col5.metric("⬇️ Mínimo por Dia", f"{min_horas:.2f} h")

    # df['Entrada_dt'] = df.apply(lambda row: datetime.combine(row['Data'], row['Horário de entrada']), axis=1)
    # df['Saida_dt'] = df.apply(lambda row: datetime.combine(row['Data'], row['Horário de Saída']), axis=1)
    # df['Duracao_horas'] = (df['Saida_dt'] - df['Entrada_dt']).dt.total_seconds() / 3600




































    # # --- Parte 2: métricas por Motivo (df) ---
    # df['Entrada_dt'] = df.apply(lambda row: datetime.combine(row['Data'], row['Horário de entrada']), axis=1)
    # df['Saida_dt'] = df.apply(lambda row: datetime.combine(row['Data'], row['Horário de Saída']), axis=1)
    # df['Duracao_horas'] = (df['Saida_dt'] - df['Entrada_dt']).dt.total_seconds() / 3600

    # metrics_motivo = df.groupby('Motivo').agg(
    #     Horas_Totais=('Duracao_horas', 'sum'),
    #     Dias_Registrados=('Data', 'nunique'),
    #     Media_Horas_Por_Dia=('Duracao_horas', 'mean'),
    #     Max_Horas_Por_Dia=('Duracao_horas', 'max'),
    #     Min_Horas_Por_Dia=('Duracao_horas', 'min')
    # ).reset_index()

    # st.subheader("📊 Métricas por Motivo")
    # for _, row in metrics_motivo.iterrows():
    #     col1, col2, col3, col4, col5 = st.columns(5)
    #     col1.metric(f"Motivo: {row['Motivo']}", "")
    #     col2.metric("⏱️ Horas Totais", f"{row['Horas_Totais']:.2f} h")
    #     col3.metric("📅 Dias Registrados", int(row['Dias_Registrados']))
    #     col4.metric("📈 Média por Registro", f"{row['Media_Horas_Por_Dia']:.2f} h")
    #     col5.metric("⬆️ Máximo", f"{row['Max_Horas_Por_Dia']:.2f} h")
    #     st.write("---")

    # # --- Parte 3: métrica geral da base de dados (soma direta do df) ---
    # total_horas_base = df['Duracao_horas'].sum()

    # st.metric("⏱️ Horas Totais na Base de Dados", f"{total_horas_base:.2f} h")

