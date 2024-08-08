# Monitor de Voltaje en Tiempo Real

Este proyecto utiliza un Arduino Nano y una interfaz gráfica en Python para visualizar en tiempo real el voltaje de un capacitor en un circuito RC. El programa permite iniciar y reiniciar la medición y mostrar la respuesta del circuito en una gráfica actualizada en tiempo real.

## Requisitos

### Hardware

- **Arduino Nano**
- **Resistencia de 1.8 MΩ**
- **Capacitor de 10 μF**
- **Cable USB** para la conexión del Arduino
- **Protoboard y cables de conexión**

### Software

- **Python 3.x**
- **Librerías Python**: `pyserial`, `tkinter`, `matplotlib`, `numpy`

## Instalación

1. **Instalar Python:**
   - Descarga e instala Python 3.x desde [python.org](https://www.python.org/downloads/).

2. **Instalar las librerías necesarias:**
   - Abre una terminal o consola de comandos.
   - Ejecuta el siguiente comando para instalar las librerías requeridas:

     ```bash
     pip install pyserial matplotlib numpy
     ```

3. **Configurar el Arduino:**
   - Conecta el Arduino Nano al computador.
   - Carga el siguiente código en tu Arduino Nano para enviar datos de tiempo y voltaje a través del puerto serial:

     ```cpp
     int analogPin = A5;  // Pin analógico para lectura del voltaje
     unsigned long startTime;

     void setup() {
       Serial.begin(9600);
       startTime = millis();
     }

     void loop() {
       unsigned long currentTime = millis() - startTime;
       int sensorValue = analogRead(analogPin);
       Serial.print(currentTime);
       Serial.print(",");
       Serial.println(sensorValue);
       delay(100);  // Espera 100 ms entre lecturas
     }
     ```

4. **Configurar el archivo `config.txt`:**
   - Crea un archivo llamado `config.txt` en el mismo directorio que el script de Python.
   - El archivo debe contener los siguientes parámetros de configuración:

     ```plaintext
     port=COM3
     baudrate=9600
     sampling_rate=100
     ```

   - **port:** El puerto serie al que está conectado el Arduino (por ejemplo, `COM3` en Windows o `/dev/ttyUSB0` en Linux).
   - **baudrate:** La velocidad de comunicación serial (9600 por defecto).
   - **sampling_rate:** La tasa de muestreo en milisegundos (100 ms por defecto).

## Uso

1. **Ejecuta el script de Python:**
   - Abre una terminal o consola de comandos.
   - Navega al directorio donde se encuentra el script de Python.
   - Ejecuta el siguiente comando:

     ```bash
     python nombre_del_script.py
     ```

2. **Interfaz de usuario:**
   - **Iniciar Medición:** Haz clic en el botón "Iniciar Medición" para comenzar la medición y mostrar los datos en la gráfica.
   - **Reiniciar Medición:** Haz clic en el botón "Reiniciar Medición" para reiniciar la conexión serial y limpiar los datos de la gráfica. Se mostrará un mensaje emergente que te pedirá descargar el capacitor.

3. **Gráfica:**
   - La gráfica muestra el voltaje en función del tiempo.
   - La curva teórica del circuito RC también se muestra en la gráfica para comparación.

4. **Configuración de la gráfica:**
   - La gráfica se ajusta automáticamente para mostrar los datos en el rango de 0 a 125 segundos y de 0 a 5 voltios.
   - La escala de la gráfica está configurada para ser proporcional a los valores del voltaje y el tiempo.

## Cálculos Detallados

### Respuesta del Circuito RC

El circuito RC tiene una resistencia \( R \) y un capacitor \( C \). La constante de tiempo \( \tau \) del circuito se define como:

![Ecuación de la constante de tiempo](https://quicklatex.com/latex3.f/ql_1e32c803c4d56058c1e7d4d8b5a394c7.png)

Para los valores dados:

- **R** = 1.8 MΩ = \( 1.8 \times 10^6 \) Ω
- **C** = 10 μF = \( 10 \times 10^{-6} \) F

Entonces,

![Cálculo de la constante de tiempo](https://quicklatex.com/latex3.f/ql_b58b89d14dbe9a0f3bb6c4b4b3e08782.png)

### Ecuación del Voltaje en el Capacitor

La ecuación diferencial para el voltaje \( V_C(t) \) en el capacitor en respuesta a un escalón de voltaje \( V_{\text{in}} \) es:

![Ecuación del voltaje en el capacitor](https://quicklatex.com/latex3.f/ql_6e08064e3a12a1a07c387d9266c4307d.png)

Para un escalón de voltaje de 5V, la ecuación se convierte en:

![Ecuación del voltaje para un escalón de 5V](https://quicklatex.com/latex3.f/ql_a9b75c2a62a6b46bb52e2cb76eb074b1.png)

### Ejemplo de Cálculo

Para calcular el voltaje en el capacitor en diferentes tiempos, sustituyamos los valores en la ecuación:

- **En \( t = 0 \) segundos:**

  ![Voltaje en t=0](https://quicklatex.com/latex3.f/ql_d8a6e373d3d3283df07c6cb86a3dd94a.png)

- **En \( t = 18 \) segundos (1 constante de tiempo):**

  ![Voltaje en t=18](https://quicklatex.com/latex3.f/ql_2b06c44b9a4317f6a6891c83d6b281b3.png)

- **En \( t = 36 \) segundos (2 constantes de tiempo):**

  ![Voltaje en t=36](https://quicklatex.com/latex3.f/ql_12cf3f982a98d7c5a490c8d308d12a4a.png)

- **En \( t = 54 \) segundos (3 constantes de tiempo):**

  ![Voltaje en t=54](https://quicklatex.com/latex3.f/ql_9dfc1718a20d75c0a77cf62f6a70e10b.png)

- **En \( t \to \infty \) segundos:**

  ![Voltaje en t=infinito](https://quicklatex.com/latex3.f/ql_bebd72d2b7d132d3f9d104db7d3d2180.png)

### Interpretación en la Gráfica

La gráfica en tiempo real mostrará cómo el voltaje en el capacitor se aproxima asintóticamente al voltaje de entrada. La curva debe seguir una forma exponencial que se aproxima a 5V, siguiendo la ecuación proporcionada. 

Para una visualización precisa, asegúrate de que los tiempos de muestreo y los intervalos de tiempo en la interfaz gráfica estén configurados para capturar y mostrar adecuadamente esta respuesta.

## Nota

- Asegúrate de tener el capacitor descargado antes de reiniciar la medición para obtener resultados precisos.
- Si el voltaje mostrado en la gráfica no coincide con la escala, verifica la conexión del capacitor y la configuración del Arduino.

## Contribuciones

Si encuentras algún problema o deseas contribuir al proyecto, no dudes en abrir un issue o enviar una pull request en el repositorio de GitHub.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.
