import pika
import sys


def cancelar_pago(hostname, port, id_pago):
    try:
        # Paso 1
        credentials = pika.PlainCredentials('alumnomq', 'alumnomq')
        parameters = pika.ConnectionParameters(host=hostname, port=port, credentials=credentials)

        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
    except Exception as e:
        print("Error al conectar con el host remoto.")
        exit()

    # Paso 2
    channel.queue_declare(queue='pago_cancelacion')
    channel.basic_publish(exchange='', routing_key='pago_cancelacion', body=str(id_pago))
    print(f" [x] Mensaje enviado: {id_pago}")

    # Paso 3
    connection.close()


def main():
    if len(sys.argv) != 4:
        print(" Debe indicar el host, el numero de puerto, y el ID del pago a cancelar como un argumento.")
        exit()

    cancelar_pago(sys.argv[1], sys.argv[2], sys.argv[3])

if __name__ == "__main__":
    main()