import streamlit as st
from src.services.whatsapp_service import create_whatsapp_ticket_link

def render_tickets():
    st.markdown("<h2 style='color: #ffffff;'>🧾 Generador Manual de Comprobantes</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #8b949e;'>Cree y envíe un ticket digital por WhatsApp de forma independiente.</p>", unsafe_allow_html=True)
    st.divider()

    col_form, col_preview = st.columns([1, 1], gap="large")

    with col_form:
        st.markdown("<h3 style='color: #2ecc71;'>1. Datos del Comprobante</h3>", unsafe_allow_html=True)
        telefono = st.text_input("Número de WhatsApp del Cliente:", value="52")
        monto = st.number_input("Monto Total ($ MXN):", min_value=1.0, value=100.0, step=10.0)
        metodo = st.selectbox("Método de Pago:", ["EFECTIVO", "DIGITAL (NFC)", "DIGITAL (Enlace WhatsApp)"])
        ticket_id = st.text_input("Folio de Ticket / ID:", value="TK-101")

    with col_preview:
        st.markdown("<h3 style='color: #2ecc71;'>2. Vista Previa del Ticket</h3>", unsafe_allow_html=True)
        
        # Tarjeta visual del ticket
        st.markdown(f"""
            <div style="background-color: #161b22; border: 1px dashed #2ecc71; border-radius: 14px; padding: 20px; margin-bottom: 20px;">
                <div style="text-align: center; border-bottom: 1px solid #30363d; padding-bottom: 10px; margin-bottom: 15px;">
                    <h3 style="color: #2ecc71; margin: 0;">🏪 PUENTE DIGITAL</h3>
                    <p style="color: #8b949e; margin: 0; font-size: 0.85rem;">Ticket Digital de Compra</p>
                </div>
                <p style="color: #c9d1d9; margin: 5px 0;"><b>Folio:</b> {ticket_id}</p>
                <p style="color: #c9d1d9; margin: 5px 0;"><b>Método:</b> {metodo}</p>
                <p style="color: #c9d1d9; margin: 5px 0;"><b>Total:</b> <span style="color: #2ecc71; font-size: 1.3rem; font-weight: bold;">${monto:,.2f} MXN</span></p>
            </div>
        """, unsafe_allow_html=True)

        wa_url = create_whatsapp_ticket_link(telefono, monto, metodo, ticket_id)
        st.markdown(f"""
            <a href="{wa_url}" target="_blank" style="text-decoration: none;">
                <div style="background-color: #25D366; color: white; text-align: center; padding: 14px; border-radius: 10px; font-weight: bold; font-size: 1.1rem; box-shadow: 0 4px 14px rgba(37, 211, 102, 0.3);">
                    📲 Abrir WhatsApp y Enviar Ticket
                </div>
            </a>
        """, unsafe_allow_html=True)