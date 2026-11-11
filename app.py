import streamlit as st
from streamlit_option_menu import option_menu

from src.components.register_sale import render_register_sale
from src.components.dashboard import render_dashboard
from src.components.debtors_ledger import render_debtors_ledger
from src.components.tickets import render_tickets

st.set_page_config(
    page_title="Puente Digital POS",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inyección de CSS Premium Avanzado
st.markdown("""
    <style>
        /* Importar fuente moderna Google Inter */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
        
        * {
            font-family: 'Inter', sans-serif !important;
        }

        /* Reducir espacio superior y expandir contenedor */
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 3rem !important;
            max-width: 95% !important;
        }
        
        /* Fondo principal de la app */
        .stApp {
            background-color: #0d1117;
        }

        /* Estilo de los encabezados principales */
        h1, h2, h3 {
            font-weight: 800 !important;
            letter-spacing: -0.5px !important;
        }

        /* Botones de acción principales (Efectivo / Digital) */
        .stButton>button {
            border-radius: 12px !important;
            font-weight: 700 !important;
            font-size: 1.25rem !important;
            padding: 0.8rem 1.5rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0px 4px 15px rgba(46, 204, 113, 0.2) !important;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0px 6px 20px rgba(46, 204, 113, 0.4) !important;
        }

        /* Cajas de entrada de texto e importes */
        div[data-baseweb="input"] {
            border-radius: 10px !important;
            background-color: #161b22 !important;
            border: 1px solid #30363d !important;
        }

        /* Tarjetas personalizadas para métricas */
        .metric-card {
            background: linear-gradient(135deg, #161b22 0%, #21262d 100%);
            border: 1px solid #30363d;
            border-radius: 16px;
            padding: 20px 25px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
        }
        .metric-card h4 {
            color: #8b949e;
            font-size: 0.95rem;
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .metric-card h2 {
            color: #ffffff;
            font-size: 2.2rem;
            margin: 0;
        }
        .metric-card.success h2 { color: #2ecc71; }
        .metric-card.warning h2 { color: #e74c3c; }
        .metric-card.info h2 { color: #3498db; }
    </style>
""", unsafe_allow_html=True)

# Menú lateral profesional
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 10px 0;">
            <h1 style="color: #2ecc71; margin: 0; font-size: 2rem;">🏪 PUENTE DIGITAL</h1>
            <p style="color: #8b949e; margin-top: 5px; font-weight: 600;">SISTEMA POS & REGISTRO</p>
        </div>
    """, unsafe_allow_html=True)
    st.divider()
    
    selected = option_menu(
        menu_title=None,
        options=["Registrar Venta", "Panel de Ganancias", "Libreta de Fiados", "Tickets WhatsApp"],
        icons=["cart-plus-fill", "pie-chart-fill", "journal-bookmark-fill", "whatsapp"],
        default_index=0,
        styles={
            "container": {"padding": "0px!", "background-color": "transparent"},
            "icon": {"color": "#2ecc71", "font-size": "20px"},
            "nav-link": {
                "font-size": "16px", 
                "text-align": "left", 
                "margin": "8px 0px", 
                "color": "#c9d1d9",
                "padding": "12px 16px",
                "border-radius": "10px",
                "--hover-color": "#21262d"
            },
            "nav-link-selected": {
                "background": "linear-gradient(90deg, #2ecc71 0%, #27ae60 100%)", 
                "color": "#ffffff", 
                "font-weight": "700",
                "box-shadow": "0 4px 12px rgba(46, 204, 113, 0.3)"
            },
        }
    )

if selected == "Registrar Venta":
    render_register_sale()

elif selected == "Panel de Ganancias":
    render_dashboard()

elif selected == "Libreta de Fiados":
    render_debtors_ledger()

elif selected == "Tickets WhatsApp":
    render_tickets()