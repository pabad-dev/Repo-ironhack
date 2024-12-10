import streamlit as st
import pickle
import pandas as pd

# Cargar los modelos previamente entrenados
def load_model(file_name):
    with open(file_name, 'rb') as file:
        return pickle.load(file)

# Cargar los modelos
model_swim = load_model('model_xgb_swim.pkl')
model_bike = load_model('model_xgb_bike.pkl')
model_run = load_model('model_rf_run.pkl')

# Configuración de la app
st.title("Predicción de tiempos para Ironman 70.3")
st.subheader("Introduce los detalles de la carrera")

# Entrada de datos
age = st.slider("Edad del atleta", min_value=18, max_value=70, value=30)
race = st.selectbox(
    "Selecciona la carrera",
    ["Ironman 70.3 Barcelona", "Ironman 70.3 Lanzarote", "Ironman 70.3 Dubai"]
)

# Procesar entrada
# Codificar las carreras en valores numéricos (ajustar según tu modelo)
race_mapping = {
    "Ironman 70.3 Barcelona": 0,
    "Ironman 70.3 Lanzarote": 1,
    "Ironman 70.3 Dubai": 2,
}
race_encoded = race_mapping[race]

# Crear el DataFrame de entrada
input_data = pd.DataFrame({"race": [race_encoded], "age": [age]})

# Botón de predicción
if st.button("Predecir tiempos"):
    # Generar predicciones
    swim_time = model_swim.predict(input_data)[0]
    bike_time = model_bike.predict(input_data)[0]
    run_time = model_run.predict(input_data)[0]

    # Mostrar resultados
    st.subheader("Resultados de la predicción:")
    st.write(f"*Tiempo de natación:* {swim_time:.2f} minutos")
    st.write(f"*Tiempo de ciclismo:* {bike_time:.2f} minutos")
    st.write(f"*Tiempo de carrera:* {run_time:.2f} minutos")

    total_time = swim_time + bike_time + run_time
    st.write(f"*Tiempo total estimado:* {total_time:.2f} minutos")