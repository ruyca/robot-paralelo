import openpyxl
import RPi.GPIO as GPIO
import time

pin_paso_motor1 = 21
pin_paso_motor2 = 20
pin_paso_motor3 = 16
pin_paso_motor4 = 12
pin_direccion_motor1 = 26
pin_direccion_motor2 = 19
pin_direccion_motor3 = 13
pin_direccion_motor4 = 6

GPIO.setwarnings(False)  # Desactivar las advertencias de GPIO
# Configurar pines GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_paso_motor1, GPIO.OUT)
GPIO.setup(pin_direccion_motor1, GPIO.OUT)
GPIO.setup(pin_paso_motor2, GPIO.OUT)
GPIO.setup(pin_direccion_motor2, GPIO.OUT)
GPIO.setup(pin_paso_motor3, GPIO.OUT)
GPIO.setup(pin_direccion_motor3, GPIO.OUT)
GPIO.setup(pin_paso_motor4, GPIO.OUT)
GPIO.setup(pin_direccion_motor4, GPIO.OUT)


# Función para girar el motor a una posición absoluta
def girar_a_posicion(pin_direccion, pin_paso, posicion_deseada, posicion_actual=0, detener_despues=True):
    # Calcular la cantidad de pasos necesarios para llegar a la posición deseada
    pasos_necesarios = abs(posicion_deseada - posicion_actual)

    # Determinar el sentido de giro
    sentido_horario = (posicion_deseada - posicion_actual) <= 0

    # Configurar dirección
    GPIO.output(pin_direccion, sentido_horario )

    # Girar a la posición deseada
    for _ in range(pasos_necesarios):
        GPIO.output(pin_paso, GPIO.HIGH)
        time.sleep(0.001)  # Ajustar según la velocidad deseada
        GPIO.output(pin_paso, GPIO.LOW)
        time.sleep(0.001)
          # Actualizar la posición actual
    posicion_actual = posicion_deseada

    if detener_despues:
        GPIO.output(pin_paso, GPIO.LOW)  # Asegurar que el pin de paso esté en bajo para detener el motor

    return posicion_actual

# Ruta del archivo XLSX
ruta_archivo = "/home/los3dh/Descargas/PASOS.xlsx"

# Lista para almacenar los datos de la columna 1
datos_columna_1 = []

# Leer datos desde el archivo XLSX
workbook = openpyxl.load_workbook(ruta_archivo)
sheet = workbook.active

# Obtener todos los datos de la columna 1
for row in sheet.iter_rows(min_row=1, max_col=1, values_only=True):
    # Se asume que la columna 1 contiene datos numéricos
    datos_columna_1.extend(row)
for dato in datos_columna_1:
    print(dato)
   
# Inicializar la posición actual
posicion_actual1 = 0
posicion_actual2 = 0
posicion_actual3 = 0
posicion_actual4 = 0

# Llamar a la función girar_a_posicion para cada valor en la lista
for posicion_deseada in datos_columna_1:
    posicion_actual1 = girar_a_posicion(pin_direccion_motor1, pin_paso_motor1, posicion_deseada, posicion_actual = 11,detener_despues=False)
    posicion_actual2 = girar_a_posicion(pin_direccion_motor2, pin_paso_motor2, posicion_deseada, posicion_actual = 11,detener_despues=False)
    posicion_actual3 = girar_a_posicion(pin_direccion_motor3, pin_paso_motor3, posicion_deseada, posicion_actual = 11,detener_despues=False)
    posicion_actual4 = girar_a_posicion(pin_direccion_motor4, pin_paso_motor4, posicion_deseada, posicion_actual = 11,detener_despues=False)
# Limpiar configuración de GPIO
girar_a_posicion(pin_direccion_motor1, pin_paso_motor1, 0, 0,detener_despues=True)
girar_a_posicion(pin_direccion_motor2, pin_paso_motor2, 0, 0,detener_despues=False)
girar_a_posicion(pin_direccion_motor3, pin_paso_motor3, 0, 0,detener_despues=False)
girar_a_posicion(pin_direccion_motor4, pin_paso_motor4, 0, 0,detener_despues=False)
GPIO.cleanup()

