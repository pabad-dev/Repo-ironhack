import streamlit as st
import pickle
import pandas as pd

# Función para cargar modelos
def load_model(file_name):
    try:
        with open(file_name, 'rb') as file:
            return pickle.load(file)
    except Exception as e:
        st.error(f"Error al cargar el modelo {file_name}: {e}")
        raise

# Cargar los modelos
model_swim = load_model('model_xgb_swim.pkl')
model_bike = load_model('model_xgb_bike.pkl')
model_run = load_model('model_rf_run.pkl')

# Configuración de la app
st.title("Predicción de Tiempos para Ironman 70.3")
st.write("Introduce los detalles de la carrera para obtener una estimación de tus tiempos en cada segmento.")

# Entrada de datos por el usuario
age = st.slider("Edad del atleta", min_value=18, max_value=70, value=30)
race = st.selectbox(
    "Selecciona la carrera",
    ["Ironman 70.3 Barcelona", "Ironman 70.3 Lanzarote", "Ironman 70.3 Dubai"]
)

# Mapeo de las carreras (ajustar según cómo fueron entrenados los modelos)
race_mapping = {
    "Ironman 70.3 Barcelona": 0,
    "Ironman 70.3 Lanzarote": 1,
    "Ironman 70.3 Dubai": 2,
}
race_encoded = race_mapping[race]

# Crear DataFrame de entrada para los modelos
input_data = pd.DataFrame({"race": [race_encoded], "age": [age]})

# Botón para predecir
if st.button("Predecir Tiempos"):
    try:
        # Realizar predicciones
        swim_time = model_swim.predict(input_data)[0]
        bike_time = model_bike.predict(input_data)[0]
        run_time = model_run.predict(input_data)[0]

        # Calcular el tiempo total
        total_time = swim_time + bike_time + run_time

        # Mostrar resultados
        st.subheader("Resultados de la Predicción:")
        st.write(f"*Tiempo de Natación:* {swim_time:.2f} minutos")
        st.write(f"*Tiempo de Ciclismo:* {bike_time:.2f} minutos")
        st.write(f"*Tiempo de Carrera:* {run_time:.2f} minutos")
        st.write(f"*Tiempo Total Estimado:* {total_time:.2f} minutos")

    except Exception as e:
        st.error(f"Error al realizar las predicciones: {e}")
