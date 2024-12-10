import streamlit as st
import pandas as pd
import pickle

# Cargar los modelos
def load_model(model_path):
    try:
        with open(model_path, 'rb') as file:
            return pickle.load(file)
    except Exception as e:
        st.error(f"Error al cargar el modelo {model_path}: {e}")
        return None

# Cargar el archivo CSV y obtener valores únicos
@st.cache_data
def load_event_locations(csv_path):
    try:
        df = pd.read_csv(csv_path)
        return df['EventLocation'].dropna().unique()
    except Exception as e:
        st.error(f"Error al cargar el archivo {csv_path}: {e}")
        return []

# Predicción basada en modelos
def predict_time(model, age, event):
    if model is None:
        return "Modelo no disponible"
    try:
        # Crear un DataFrame con las entradas
        input_data = pd.DataFrame({"age": [age], "event": [event]})
        # Realizar predicción
        prediction = model.predict(input_data)
        return round(prediction[0], 2)
    except Exception as e:
        st.error(f"Error al realizar la predicción: {e}")
        return "Error en la predicción"

# Cargar los modelos
model_swim = load_model('model_xgb_swim.pkl')
model_bike = load_model('model_xgb_bike.pkl')
model_run = load_model('model_rf_run.pkl')

# Configurar la app de Streamlit
st.title("Predicción de tiempos para Ironman 70.3")

# Cargar valores únicos de la columna 'event location'
event_locations = load_event_locations('df_merged_small.csv')

# Interfaz de usuario
st.header("Introduce los detalles")
age = st.slider("Edad", 18, 70, 30)
event = st.selectbox("Carrera", event_locations)

if st.button("Predecir tiempos"):
    st.subheader("Resultados")
    swim_time = predict_time(model_swim, age, event)
    bike_time = predict_time(model_bike, age, event)
    run_time = predict_time(model_run, age, event)

    st.write(f"*Tiempo natación:* {swim_time} minutos")
    st.write(f"*Tiempo bicicleta:* {bike_time} minutos")
    st.write(f"*Tiempo carrera:* {run_time} minutos")
