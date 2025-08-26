
import pandas as pd
from datetime import datetime, timedelta


def conversor(df):
    df['Data'] = df['Data'].apply(lambda x: datetime.strptime(x, "%d/%m/%Y"))
    df['Horário de entrada'] = df['Horário de entrada'].apply(lambda x: datetime.strptime(x, "%H:%M:%S").time())
    df['Horário de Saída'] = df['Horário de Saída'].apply(lambda x: datetime.strptime(x, "%H:%M:%S").time())

    # Combinar data e hora para criar a coluna 'Data_completa'
    df['Data_completa'] = df.apply(lambda row: datetime.combine(row['Data'], row['Horário de entrada']), axis=1)
    df['Data_saida'] = df.apply(lambda row: datetime.combine(row['Data'], row['Horário de Saída']), axis=1)

    df['Duração (hh:mm)'] = df['Data_saida'] - df['Data_completa']
    df['Duração (hh:mm)'] = df['Duração (hh:mm)'].apply(lambda td: f"{td.seconds // 3600:02}:{(td.seconds // 60) % 60:02}")

    # DEIXAR PARA MINUTOS (AO INVEZ DE 02:02 DEIXA APENAS COMO 122min)
    # df['Duração'] = df['Data_saida'] - df['Data_completa']
    # df['Duração (minutos)'] = df['Duração'].apply(lambda td: td.total_seconds() // 60)
    # print(df)
    