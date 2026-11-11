import os
import base64
import streamlit as st
from src.utils.data_manager import add_sale
from src.services.payments import process_nfc_payment, process_whatsapp_link_payment
from src.services.whatsapp_service import create_whatsapp_ticket_link

def play_audio():
    audio_path = "assets/success_sound.mp3"
    if os.path.exists(audio_path):
        with open(audio_path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f"""
                <audio autoplay style="display:none;">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
                """
            st.markdown(md, unsafe_allow_html=True)

def set_monto(nuevo_valor):
    """Callback para sustituir el valor en el session_state"""
    st.session_state["monto_venta"] = float(nuevo_valor)

def render_register_sale():
    if "monto_venta" not in st.session_state:
        st.session_state["monto_venta"] = 50.0

    st.markdown("<h2 style='color: #ffffff;'>⚡ Terminal de Cobro Rápido</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #8b949e; font-size: 1.05rem;'>Ingrese el importe de la venta o seleccione un billete rápido.</p>", unsafe_allow_html=True)
    st.divider()

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("<h3 style='color: #2ecc71;'>1. Importe de la Transacción</h3>", unsafe_allow_html=True)
        
        monto = st.number_input(
            "Monto de la Venta ($ MXN)", 
            min_value=1.0, 
            step=5.0,
            key="monto_venta"
        )
        
        st.caption("Billetes / Montos Rápidos (Sustituir):")
        c1, c2, c3, c4 = st.columns(4)
        c1.button("$20", on_click=set_monto, args=(20.0,), use_container_width=True)
        c2.button("$50", on_click=set_monto, args=(50.0,), use_container_width=True)
        c3.button("$100", on_click=set_monto, args=(100.0,), use_container_width=True)
        c4.button("$200", on_click=set_monto, args=(200.0,), use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)
        tipo_pago = st.radio("Método de Pago:", ["EFECTIVO", "DIGITAL"], horizontal=True)

        # Selección de modalid digital previa al resumen
        if tipo_pago == "DIGITAL":
            metodo = st.selectbox("Canal Digital:", ["Sin Contacto (NFC)", "Enlace WhatsApp"])
            telefono = st.text_input("WhatsApp del Cliente (para ticket):", value="52")
        else:
            metodo = "EFECTIVO"
            telefono = ""

    with col2:
        st.markdown("<h3 style='color: #2ecc71;'>2. Resumen & Cobro</h3>", unsafe_allow_html=True)
        
        # Calcular valores preliminares para el ticket
        comision_estimada = 0.0 if tipo_pago == "EFECTIVO" else (monto * 0.02 if "WhatsApp" in metodo else 0.0)
        neto_estimado = monto - comision_estimada

        # Tarjeta visual estilo recibo que ocupa espacio vertical
        st.markdown(f"""
            <div style="background-color: #161b22; border: 1px solid #30363d; border-radius: 14px; padding: 24px; margin-bottom: 20px;">
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #30363d; padding-bottom: 12px; margin-bottom: 16px;">
                    <span style="color: #8b949e; font-weight: 600;">Concepto</span>
                    <span style="color: #ffffff; font-weight: 700;">Cobro de Mostrador</span>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <span style="color: #8b949e;">Venta Bruta:</span>
                    <span style="color: #ffffff; font-size: 1.2rem; font-weight: 600;">${monto:,.2f} MXN</span>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <span style="color: #8b949e;">Vía de Pago:</span>
                    <span style="color: {'#2ecc71' if tipo_pago == 'EFECTIVO' else '#3498db'}; font-weight: bold;">{metodo}</span>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                    <span style="color: #8b949e;">Comisión Estimada:</span>
                    <span style="color: #e74c3c; font-weight: 600;">-${comision_estimada:,.2f} MXN</span>
                </div>
                <div style="border-top: 2px dashed #30363d; padding-top: 14px; display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: #ffffff; font-size: 1.1rem; font-weight: bold;">Ingreso Neto Caja:</span>
                    <span style="color: #2ecc71; font-size: 1.8rem; font-weight: 800;">${neto_estimado:,.2f} MXN</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Botón de cobro principal
        if tipo_pago == "EFECTIVO":
            if st.button("💵 CONFIRMAR PAGO EN EFECTIVO", type="primary", use_container_width=True):
                venta = add_sale(monto, "EFECTIVO", comision=0.0)
                st.balloons()
                st.success(f"✅ ¡Pago en efectivo registrado! (${monto:,.2f} MXN)")
                play_audio()
        else:
            if st.button("💳 PROCESAR COBRO DIGITAL", type="primary", use_container_width=True):
                if metodo == "Sin Contacto (NFC)":
                    exito, comision = process_nfc_payment(monto)
                else:
                    exito, comision = process_whatsapp_link_payment(monto)
                    
                if exito:
                    venta = add_sale(monto, f"DIGITAL ({metodo})", comision=comision)
                    st.balloons()
                    st.success(f"✅ ¡Pago Digital Aprobado! Netos: ${venta['ingreso_neto']:,.2f} MXN")
                    play_audio()
                    
                    if telefono:
                        wa_url = create_whatsapp_ticket_link(telefono, monto, metodo, venta["id"])
                        st.markdown(f"""
                            <a href="{wa_url}" target="_blank" style="text-decoration: none;">
                                <div style="background-color: #25D366; color: white; text-align: center; padding: 14px; border-radius: 10px; font-weight: bold; margin-top: 12px; font-size: 1.1rem;">
                                    📲 Enviar Comprobante por WhatsApp
                                </div>
                            </a>
                        """, unsafe_allow_html=True)