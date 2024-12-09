import streamlit as st

# Título de la app
st.title("Calculadora de tiempos para Ironman")

# Mensaje inicial
st.write("Introduce tus datos para estimar el tiempo de cada segmento y el total.")

# Inputs del usuario
st.header("Datos de rendimiento")
swim_pace = st.text_input("Ritmo natación (min:seg / 100m):", value="2:00")  # Ritmo natación
bike_pace = st.text_input("Ritmo ciclismo (min/km):", value="4:00")  # Ritmo ciclismo
run_pace = st.text_input("Ritmo carrera (min/km):", value="5:00")  # Ritmo carrera

t1_time = st.number_input("Tiempo de transición T1 (min):", min_value=0.0, max_value=30.0, step=0.1)
t2_time = st.number_input("Tiempo de transición T2 (min):", min_value=0.0, max_value=30.0, step=0.1)

# Distancias estándar de un Ironman
swim_distance = 3.8  # en km
bike_distance = 180  # en km
run_distance = 42.2  # en km

# Función para convertir ritmo (min:seg) a tiempo en horas
def convert_pace_to_hours(pace, distance_m):
    try:
        minutes, seconds = map(int, pace.split(":"))
        total_seconds_per_100m = minutes * 60 + seconds
        total_time_seconds = (distance_m / 100) * total_seconds_per_100m
        return total_time_seconds / 3600  # Convertir segundos a horas
    except:
        st.error("Por favor, introduce el ritmo en formato correcto (min:seg).")
        return None

# Función para convertir el ritmo ciclismo/carrera (min/km) a tiempo en horas
def convert_pace_to_hours_for_bike_run(pace, distance_km):
    try:
        minutes, seconds = map(int, pace.split(":"))
        total_seconds_per_km = minutes * 60 + seconds
        total_time_seconds = distance_km * total_seconds_per_km
        return total_time_seconds / 3600  # Convertir segundos a horas
    except:
        st.error("Por favor, introduce el ritmo en formato correcto (min:seg).")
        return None

# Cálculos de tiempo
if st.button("Calcular tiempo total"):
    swim_time = convert_pace_to_hours(swim_pace, swim_distance * 1000)  # Convertir distancia a metros
    if swim_time is not None:
        bike_time = convert_pace_to_hours_for_bike_run(bike_pace, bike_distance)  # Cálculo de tiempo ciclismo
        run_time = convert_pace_to_hours_for_bike_run(run_pace, run_distance)  # Cálculo de tiempo carrera

        total_time = swim_time + bike_time + run_time + t1_time / 60 + t2_time / 60  # Convertir transiciones a horas

        # Mostrar resultados
        st.header("Resultados")
        st.write(f"Tiempo natación: {swim_time:.2f} horas")
        st.write(f"Tiempo ciclismo: {bike_time:.2f} horas")
        st.write(f"Tiempo carrera: {run_time:.2f} horas")
        st.write(f"*Tiempo total estimado: {total_time:.2f} horas*")
