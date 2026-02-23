# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# author: rmarabini
"Interface with the database"
from django.conf import settings
from xmlrpc.client import ServerProxy


def verificar_tarjeta(tarjeta_data):
    """
    Invokes the remote RPC procedure to validate a credit card.
    :param tarjeta_data: A dictionary containing card details:
                         (number, holder_name, expiration_date, CVV).
    :return: Returns True if the card is valid and exists in the remote
             database, False otherwise.
    """
    with ServerProxy(settings.RPCAPIBASEURL) as proxy:
        return proxy.verificar_tarjeta(tarjeta_data)


def registrar_pago(pago_dict):
    """
    Calls the remote RPC method to record a new payment transaction.
    :param pago_dict: A dictionary with payment details such as:
                      (idComercio, price, idTarjeta_id).
    :return: A dictionary representing the created Pago object (including the
             timestamp 'marcaTiempo') if successful, or None if an error
             occurred.
    """
    with ServerProxy(settings.RPCAPIBASEURL) as proxy:
        return proxy.registrar_pago(pago_dict)


def eliminar_pago(idPago):
    """
    Requests the remote RPC server to delete a specific payment record.
    :param idPago: The unique integer ID of the payment to be deleted.
    :return: Returns True if the deletion was successful,
             False if the record was not found or an error occurred.
    """
    with ServerProxy(settings.RPCAPIBASEURL) as proxy:
        return proxy.eliminar_pago(idPago)


def get_pagos_from_db(idComercio):
    """
    Retrieves a list of all payments associated with a specific merchant
    from the remote database.
    :param idComercio: The unique identifier of the merchant (string or int).
    :return: A list of dictionaries, where each dictionary contains the data
             of a payment record.
    """
    with ServerProxy(settings.RPCAPIBASEURL) as proxy:
        return proxy.get_pagos_from_db(idComercio)
