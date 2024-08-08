import serial
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Función para leer la configuración desde un archivo
def leer_configuracion():
    config = {}
    with open('config.txt', 'r') as f:
        for line in f:
            key, value = line.strip().split('=')
            config[key] = value
    return config

# Función para reiniciar la medición y la conexión serial
def reiniciar_medicion():
    global ser
    ser.close()  # Cierra la conexión serial actual
    ser.open()   # Reabre la conexión serial
    ser.flushInput()  # Limpia el buffer de entrada del puerto serial
    ser.flushOutput() # Limpia el buffer de salida del puerto serial
    ser.write(b'R')  # Envía el comando 'R' al Arduino para reiniciar la medición
    
    # Limpia los datos de la gráfica
    xdata.clear()
    ydata.clear()
    
    # Muestra un mensaje emergente
    messagebox.showinfo("Reiniciar Medición", "Favor de descargar el capacitor")

# Leer configuración del archivo
config = leer_configuracion()
puerto_serie = config.get('port', 'COM3')
baudrate = int(config.get('baudrate', 9600))
sampling_rate = int(config.get('sampling_rate', 100))

# Configuración del puerto serial
ser = serial.Serial(puerto_serie, baudrate)

# Configuración de la interfaz Tkinter
root = tk.Tk()
root.title("Gráfica en tiempo real de voltaje en el capacitor")

# Configuración de la gráfica
fig, ax = plt.subplots()
ax.set_xlim(0, 125)  # Limite del tiempo en segundos
ax.set_ylim(0, 5)    # Limite del voltaje en voltios
ax.set_xlabel('Tiempo (s)')
ax.set_ylabel('Voltaje (V DC)')
ax.set_title('Respuesta del Circuito RC')

# Listas para mantener los datos de la gráfica
xdata = []
ydata = []

# Parámetros del circuito
R = 1.8e6  # Resistencia en ohmios
C = 10e-6  # Capacitancia en faradios
V_in = 5.0  # Voltaje de entrada

# Generar la curva teórica para la gráfica
t_theoretical = np.linspace(0, 125, 500)
v_theoretical = V_in * (1 - np.exp(-t_theoretical / (R * C)))

# Crear etiquetas en la interfaz
voltage_label = tk.Label(root, text="Valor Actual ADC en V DC = 0.00")
voltage_label.pack()

circuit_values_label = tk.Label(root, text=f"Resistencia = {R / 1e6} MΩ\nCapacitancia = {C * 1e6} µF")
circuit_values_label.pack()

equation_label = tk.Label(root, text=f"Ecuación: V(t) = {V_in} * (1 - exp(-t / ({R} * {C})))")
equation_label.pack()

# Añadir tramado a la gráfica
ax.grid(True)  # Habilitar la rejilla
ax.xaxis.set_major_locator(plt.AutoLocator())  # Ajuste automático de los marcadores del eje X
ax.yaxis.set_major_locator(plt.AutoLocator())  # Ajuste automático de los marcadores del eje Y

# Función de inicialización para la animación
def init():
    line.set_data([], [])
    theoretical_line.set_data(t_theoretical, v_theoretical)
    return line, theoretical_line

# Función para actualizar la gráfica en tiempo real
def update(frame):
    if ser.in_waiting:
        data = ser.readline().decode().strip()  # Lee y decodifica el dato del puerto serial
        if data:
            time_str, voltage_str = data.split(',')
            currentTime = int(time_str) / 1000  # Convierte el tiempo a segundos
            voltage = int(voltage_str) * (5.0 / 1023.0)  # Convierte el valor analógico a voltaje
            
            # Solo actualiza si el tiempo está dentro del rango visible
            if currentTime <= ax.get_xlim()[1]:
                if len(xdata) == 0 or currentTime > xdata[-1]:
                    xdata.append(currentTime)
                    ydata.append(voltage)
                elif currentTime == xdata[-1]:
                    ydata[-1] = voltage
                
                # Mantener los datos dentro del rango visible
                if len(xdata) > 0 and xdata[0] < ax.get_xlim()[0]:
                    xdata.pop(0)  # Elimina el dato más antiguo
                    ydata.pop(0)  # Elimina el dato más antiguo
            
            # Actualizar la etiqueta con el valor de voltaje actual
            voltage_label.config(text=f"Valor Actual ADC en V DC = {voltage:.2f}")
    
    line.set_data(xdata, ydata)
    return line, theoretical_line

# Función para iniciar la medición
def iniciar_medicion():
    ser.write(b'S')  # Envía el comando 'S' al Arduino para iniciar la medición

# Añadir los botones en la interfaz
btn_iniciar = tk.Button(root, text="Iniciar Medición", command=iniciar_medicion)
btn_iniciar.pack()

btn_reiniciar = tk.Button(root, text="Reiniciar Medición", command=reiniciar_medicion)
btn_reiniciar.pack()

# Crear el lienzo para la gráfica
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Inicializar la línea para la gráfica
line, = ax.plot([], [], lw=2, label='Datos Reales')
theoretical_line, = ax.plot(t_theoretical, v_theoretical, 'r--', label='Curva Teórica')

ax.legend()

# Configurar la animación
ani = animation.FuncAnimation(fig, update, init_func=init, blit=True, interval=sampling_rate)

# Ejecutar la interfaz Tkinter
tk.mainloop()
