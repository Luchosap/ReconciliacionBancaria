import streamlit as st
import pandas as pd

def cargar_archivo_excel(label):
    archivo = st.file_uploader(label, type=['xlsx'])
    if archivo:
        # Forzar engine openpyxl para evitar errores
        df = pd.read_excel(archivo, engine='openpyxl')
        return df
    return None

def conciliacion(sap_df, bank_df):
    # Merge por Referencia con indicador de existencia en cada archivo
    df_merge = pd.merge(sap_df, bank_df, on='Referencia', how='outer', suffixes=('_SAP', '_Banco'), indicator=True)
    
    # Calcular diferencia de importes
    df_merge['Diferencia Importe'] = df_merge['Importe Cobranzas'].fillna(0) - df_merge['Importe Depósitos'].fillna(0)
    
    # Filtrar diferencias: referencias que no están en ambos o con importes diferentes
    diferencias = df_merge[(df_merge['_merge'] != 'both') | (df_merge['Diferencia Importe'] != 0)]
    
    return diferencias

st.title('Conciliación de Cobranzas SAP vs Estado de Cuenta Bancario')

sap_df = cargar_archivo_excel('Subir archivo FBL5N SAP con cobranzas')
bank_df = cargar_archivo_excel('Subir archivo Estado de Cuenta Bancario con depósitos')

if sap_df is not None and bank_df is not None:
    st.subheader('Datos SAP')
    st.dataframe(sap_df)
    st.subheader('Datos Banco')
    st.dataframe(bank_df)
    
    diferencias = conciliacion(sap_df, bank_df)
    st.subheader('Diferencias encontradas')
    st.dataframe(diferencias)
else:
    st.info('Por favor, sube ambos archivos para realizar la conciliación.')
