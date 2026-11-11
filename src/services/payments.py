import time

def process_nfc_payment(monto):
    # Simula la conexión con tarjeta/celular NFC
    time.sleep(1)
    return True, 0.0  # (éxito, comisión)

def process_whatsapp_link_payment(monto):
    # Simula cobro por enlace digital con ligera comisión
    comision = monto * 0.02  # Ej: 2% comisión
    return True, comision