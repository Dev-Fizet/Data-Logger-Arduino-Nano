// Definiciones de pines
const int pinSalida = 4; // Pin digital para la función escalón
const int pinAnalogico = A5; // Pin analógico para leer el voltaje del capacitor

// Constantes de tiempo
const long tiempoMuestreo = 18000; // 18 segundos (constante de tiempo)
const long totalTiempo = 7 * tiempoMuestreo; // 126 segundos (7 constantes de tiempo)

void setup() {
  pinMode(pinSalida, OUTPUT);
  Serial.begin(9600);
  digitalWrite(pinSalida, LOW); // Inicializa el pin de salida en LOW
}

void loop() {
  if (Serial.available() > 0) {
    char comando = Serial.read();
    if (comando == 'S') { // Comienza la medición cuando se recibe 'S'
      digitalWrite(pinSalida, HIGH); // Aplica la función escalón
      long startTime = millis();

      while (millis() - startTime < totalTiempo) {
        int valorAnalogico = analogRead(pinAnalogico);
        long currentTime = millis() - startTime;
        Serial.print(currentTime);
        Serial.print(",");
        Serial.println(valorAnalogico);
        delay(100); // Tiempo de muestreo
      }

      digitalWrite(pinSalida, LOW); // Desactiva la función escalón
    }
  }
}
