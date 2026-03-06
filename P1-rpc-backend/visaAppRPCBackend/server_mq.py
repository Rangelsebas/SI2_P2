import os
import sys
import django
import pika

# Configuración del entorno de Django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'visaSite.settings')
django.setup()


# Importación de modelos después de django.setup()
from visaAppRPCBackend.models import Pago


# Paso 3
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())
    id_pago = body.decode()

    try:
        # Buscamos el pago en la base de datos
        pago = Pago.objects.get(id=id_pago)
        pago.codigoRespuesta = '111'
        pago.save()
        print(f" Éxito: Pago {id_pago} marcado como cancelado (111).")
    except Pago.DoesNotExist:
        print(f" Error: El pago {id_pago} no existe.")
    except Exception as e:
        print(f" Error inesperado: {e}")


def main():

    if len(sys.argv) != 3:
        print("Debe indicar el host y el puerto")
        exit()

    hostname = sys.argv[1]
    port = int(sys.argv[2])

    # Paso 1
    credentials = pika.PlainCredentials('alumnomq', 'alumnomq')
    parameters = pika.ConnectionParameters(host=hostname, port=port, credentials=credentials)

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # Paso 2
    channel.queue_declare(queue='pago_cancelacion')

    # Paso 4
    channel.basic_consume(queue='pago_cancelacion', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == "__main__":
    main()
