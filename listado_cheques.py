import csv
import sys
import datetime

fecha_rango = '2020-01-25:2022-05-25'
fecha_inicio, fecha_fin = fecha_rango.split(':')

fecha_inicio_obj = datetime.datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
fecha_fin_obj = datetime.datetime.strptime(fecha_fin, "%Y-%m-%d").date()

timestamp_inicio = int(datetime.datetime.strptime(fecha_inicio, "%Y-%m-%d").timestamp())
timestamp_fin = int(datetime.datetime.strptime(fecha_fin, "%Y-%m-%d").timestamp())

def validar_fecha_formato_y_rango(fecha_str):
    try:
        fecha_obj = datetime.datetime.strptime(fecha_str, '%Y-%m-%d')
        if fecha_obj.date() < fecha_inicio_obj or fecha_obj.date() > fecha_fin_obj:
            return False
    except ValueError: 
        return False
    return True

def timestamp_to_datetime(timestamp):
    return datetime.datetime.fromtimestamp(int(timestamp))

def format_datetime(dt_obj):
    return dt_obj.strftime('%Y-%m-%d %H:%M:%S')

# Validar que se proporcionen suficientes argumentos
if len(sys.argv) < 5:
    print("Uso: python script.py <filename> <dni_a_filtrar> <pantalla_o_csv> <tipo> [estado] [fecha_a_filtrar]")
    sys.exit(1)

# Obtener argumentos de la línea de comandos
filename = sys.argv[1]
dni_a_filtrar = sys.argv[2]
pantalla_o_csv = sys.argv[3]
tipo = sys.argv[4]
estado = None
fecha_a_filtrar = None

# Leer argumentos opcionales si están presentes
if len(sys.argv) > 5:
    estado = sys.argv[5]

if len(sys.argv) > 6:
    fecha_a_filtrar = sys.argv[6]

if fecha_a_filtrar is not None and not validar_fecha_formato_y_rango(fecha_a_filtrar):
    print(f"Error: La fecha {fecha_a_filtrar} no tiene el formato correcto o está fuera del rango permitido.")
    sys.exit(1)

# Abre el archivo y lee el contenido
with open(filename, "r") as file:
    reader = csv.DictReader(file)
    datos = [row for row in reader]

# Filtrar los datos según los criterios especificados
datos_filtrados = [dato for dato in datos if dato['DNI'] == dni_a_filtrar]
datos_filtrados = [dato for dato in datos_filtrados if dato['Tipo'] == tipo]

if estado is not None:
    datos_filtrados = [dato for dato in datos_filtrados if dato['Estado'] == estado]

if fecha_a_filtrar is not None:
    fecha_a_filtrar_obj = datetime.datetime.strptime(fecha_a_filtrar, '%Y-%m-%d')
    datos_filtrados = [dato for dato in datos_filtrados if datetime.datetime.fromtimestamp(int(dato['FechaOrigen'])).date() == fecha_a_filtrar_obj.date()]
    datos_filtrados = [dato for dato in datos_filtrados if timestamp_inicio <= int(dato['FechaOrigen']) <= timestamp_fin]



# Parte que valida si se desea la salida en CSV o en pantalla
if pantalla_o_csv == 'CSV':
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    output_filename_custom = f"{dni_a_filtrar}_{timestamp}.csv"
    output_filename_default = "salida.csv"

    with open(output_filename_custom, "w") as salida_custom:
        writer_custom = csv.DictWriter(salida_custom, fieldnames=reader.fieldnames)
        writer_custom.writeheader()
        writer_custom.writerows(datos_filtrados)
    print(f"Datos filtrados guardados en {output_filename_custom}")

    # Además, guardamos los datos en el archivo predeterminado "salida.csv"
    with open(output_filename_default, "a") as salida_default:
        writer_default = csv.DictWriter(salida_default, fieldnames=reader.fieldnames)
        writer_default.writerows(datos_filtrados)

elif pantalla_o_csv == 'PANTALLA':
    print(f"{'DNI':<15}{'Tipo':<10}{'Estado':<15}{'FechaOrigen':<20}{'FechaPago':<20}")

    for fila in datos_filtrados:
        dni = fila['DNI']
        tipo = fila['Tipo']
        estado = fila['Estado']
        fecha_origen = format_datetime(timestamp_to_datetime(fila['FechaOrigen']))
        fecha_pago = format_datetime(timestamp_to_datetime(fila['FechaPago']))

        print(f"{dni:<15}{tipo:<10}{estado:<15}{fecha_origen:<20}{fecha_pago:<20}")

else:
    print("Opción incorrecta. Elegir entre 'CSV' o 'PANTALLA'.")