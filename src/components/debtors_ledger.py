import streamlit as st
from src.utils.data_manager import get_debtors, add_or_update_debtor, pay_debt

def render_debtors_ledger():
    st.markdown("<h2 style='color: #ffffff;'>📖 Libreta Digital de Fiados</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #8b949e;'>Gestiona cuentas pendientes, créditos a clientes y cobros de saldo.</p>", unsafe_allow_html=True)
    st.divider()

    # Layout de 2 columnas principales
    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown("<h3 style='color: #2ecc71;'>✍️ Operaciones de Cuenta</h3>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["➕ Registrar / Incrementar Deuda", "💵 Registrar Pago de Cliente"])
        
        with tab1:
            st.markdown("<br>", unsafe_allow_html=True)
            nombre = st.text_input("Nombre del Cliente:", placeholder="Ej: Don Pedro - Tiendita")
            monto_deuda = st.number_input("Monto a Fiar ($ MXN):", min_value=1.0, value=20.0, step=5.0)
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("📌 REGISTRAR EN DEUDA", type="primary", use_container_width=True):
                if nombre.strip():
                    add_or_update_debtor(nombre, monto_deuda)
                    st.success(f"✅ Se añadieron ${monto_deuda:,.2f} a la cuenta de {nombre}.")
                else:
                    st.warning("⚠️ Escribe el nombre del cliente.")

        with tab2:
            st.markdown("<br>", unsafe_allow_html=True)
            df_debtors = get_debtors()
            debtors_list = df_debtors[df_debtors["deuda_total"] > 0]["cliente"].tolist() if not df_debtors.empty else []
            
            if debtors_list:
                cliente_sel = st.selectbox("Seleccionar Cliente deudor:", debtors_list)
                monto_pago = st.number_input("Monto que Abona ($ MXN):", min_value=1.0, value=10.0, step=5.0)
                st.markdown("<br>", unsafe_allow_html=True)
                
                if st.button("💰 REGISTRAR ABONO Y SALDAR", type="primary", use_container_width=True):
                    pay_debt(cliente_sel, monto_pago)
                    st.success(f"✅ Pago abonado a {cliente_sel}. Registrado en las ganancias en efectivo del día.")
            else:
                st.info("ℹ️ No hay clientes con saldos pendientes por cobrar.")

    with col_right:
        st.markdown("<h3 style='color: #2ecc71;'>📋 Resumen de Cuentas por Cobrar</h3>", unsafe_allow_html=True)
        
        df_debtors = get_debtors()
        total_por_cobrar = df_debtors['deuda_total'].sum() if not df_debtors.empty else 0.0

        # Tarjeta KPI de Deuda Total
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #161b22 0%, #21262d 100%); border: 1px solid #e74c3c; border-radius: 14px; padding: 20px; text-align: center; margin-bottom: 20px;">
                <h4 style="color: #8b949e; margin: 0; font-size: 0.95rem; text-transform: uppercase;">Saldo Total Pendiente por Cobrar</h4>
                <h2 style="color: #e74c3c; font-size: 2.5rem; margin: 8px 0 0 0;">${total_por_cobrar:,.2f} MXN</h2>
            </div>
        """, unsafe_allow_html=True)

        if not df_debtors.empty:
            st.dataframe(df_debtors, use_container_width=True, hide_index=True)
        else:
            st.caption("No hay registro de clientes deudores.")