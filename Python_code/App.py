import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt

# Ruta del archivo CSV
csv_file = r'C:\Users\cesar\Desktop\platzi\SafeSight_AI\Histori_data\cumplimiento_registros.csv'

# Configuración de la interfaz de Streamlit
st.title("Monitoreo de EPP - SafeSight AI")
st.subheader("Estado en tiempo real de los implementos de seguridad")

# Placeholder para los datos
placeholder_data = st.empty()  # Para mostrar los datos en tiempo real

# Función para cargar y mostrar datos en tiempo real
def load_and_display_data():
    while True:
        data = pd.read_csv(csv_file, encoding='latin-1')
        data['Hora'] = pd.to_datetime(data['Hora'], errors='coerce')  # Convertir a datetime

        # Mostrar los datos en tabla
        with placeholder_data.container():
            st.write("Historial de cumplimiento:", data)

        # Generar y mostrar gráficas
        st.write("## Gráficas de análisis")

        # Gráfica 1: Histórico de uso por implemento
        plt.figure(figsize=(10, 6))
        for implemento in data['Implemento'].unique():
            subset = data[data['Implemento'] == implemento]
            plt.plot(subset['Hora'], subset['Duración'], label=implemento)
        plt.xlabel('Hora')
        plt.ylabel('Duración (s)')
        plt.title('Histórico de uso por implemento')
        plt.legend()
        plt.xticks(rotation=45)
        st.pyplot(plt)

        # Gráfica 2: Distribución de tiempo en cada estado por implemento
        plt.figure(figsize=(10, 6))
        estados_counts = data.groupby(['Implemento', 'Estado']).size().unstack(fill_value=0)
        estados_counts = estados_counts.apply(pd.to_numeric, errors='coerce').fillna(0)  # Asegurar datos numéricos
        estados_counts.plot(kind='bar', stacked=True)
        plt.xlabel('Implemento')
        plt.ylabel('Frecuencia')
        plt.title('Distribución de tiempo en cada estado por implemento')
        st.pyplot(plt)

        # Gráfica 3: Duración promedio de cada estado por implemento
        plt.figure(figsize=(10, 6))
        duracion_promedio = data.groupby(['Implemento', 'Estado'])['Duración'].mean().unstack(fill_value=0)
        duracion_promedio = duracion_promedio.apply(pd.to_numeric, errors='coerce').fillna(0)  # Asegurar datos numéricos
        duracion_promedio.plot(kind='bar')
        plt.xlabel('Implemento')
        plt.ylabel('Duración promedio (s)')
        plt.title('Duración promedio de cada estado por implemento')
        st.pyplot(plt)

        # Gráfica 4: Tendencia de cambios de estado
        plt.figure(figsize=(10, 6))
        data['Cambio'] = data['Estado'].ne(data['Estado'].shift()).astype(int)
        cambios_estado = data.groupby([data['Hora'].dt.date, 'Implemento'])['Cambio'].sum().unstack(fill_value=0)
        cambios_estado = cambios_estado.apply(pd.to_numeric, errors='coerce').fillna(0)  # Asegurar datos numéricos
        cambios_estado.plot()
        plt.xlabel('Fecha')
        plt.ylabel('Número de cambios')
        plt.title('Tendencia de cambios de estado por implemento')
        plt.xticks(rotation=45)
        st.pyplot(plt)

        time.sleep(5)  # Actualización cada 5 segundos

# Ejecutar la función para cargar datos y generar gráficos
load_and_display_data()
