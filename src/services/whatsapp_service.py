from urllib.parse import quote

def create_whatsapp_ticket_link(phone_number, monto, tipo_pago, ticket_id):
    mensaje = (
        f"🧾 *COMPROBANTE DE PAGO - PUENTE DIGITAL*\n"
        f"----------------------------------------\n"
        f"Ticket #: {ticket_id}\n"
        f"Monto Total: ${monto:,.2f} MXN\n"
        f"Método de Pago: {tipo_pago}\n"
        f"¡Gracias por su compra!\n"
    )
    url_encoded = quote(mensaje)
    clean_phone = "".join(filter(str.isdigit, str(phone_number)))
    return f"https://wa.me/{clean_phone}?text={url_encoded}"