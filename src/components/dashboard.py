import streamlit as st
from src.utils.data_manager import get_sales
from src.utils.charts import generate_sales_chart
from src.services.sync_service import sync_pending_transactions

def render_dashboard():
    col_t, col_b = st.columns([3, 1])
    with col_t:
        st.markdown("<h2 style='color: #ffffff;'>📊 Dashboard de Rendimiento Diario</h2>", unsafe_allow_html=True)
    with col_b:
        if st.button("🔄 Sincronizar Nube", use_container_width=True):
            exito, cant = sync_pending_transactions()
            if exito:
                st.toast(f"¡Sincronizadas {cant} ventas!")
            else:
                st.toast("Todo sincronizado correctamente.")

    df_sales = get_sales()
    
    total_acumulado = df_sales["monto"].sum() if not df_sales.empty else 0.0
    comisiones_totales = df_sales["comision"].sum() if not df_sales.empty else 0.0
    rentabilidad_real = df_sales["ingreso_neto"].sum() if not df_sales.empty else 0.0
    
    # Tarjetas Métricas KPI en 3 Columnas
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown(f"""
            <div class="metric-card info">
                <h4>Ventas Totales (Bruto)</h4>
                <h2>${total_acumulado:,.2f}</h2>
            </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown(f"""
            <div class="metric-card warning">
                <h4>Comisiones Operativas</h4>
                <h2>-${comisiones_totales:,.2f}</h2>
            </div>
        """, unsafe_allow_html=True)
        
    with c3:
        st.markdown(f"""
            <div class="metric-card success">
                <h4>Rentabilidad Real (Neto)</h4>
                <h2>${rentabilidad_real:,.2f}</h2>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Gráfica Principal de Rendimiento
    fig = generate_sales_chart(df_sales)
    st.pyplot(fig)
    
    with st.expander("📄 Ver Historial Completo de Transacciones"):
        st.dataframe(df_sales, use_container_width=True)