import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def generate_sales_chart(df_sales):
    plt.style.use('dark_background')
    
    if df_sales.empty:
        fig, ax = plt.subplots(figsize=(8, 3.5))
        fig.patch.set_alpha(0.0)
        ax.patch.set_alpha(0.0)
        ax.text(0.5, 0.5, "Sin ventas registradas hoy", ha="center", va="center", fontsize=14, color="#ffffff")
        ax.axis("off")
        return fig

    fig, ax = plt.subplots(figsize=(10, 4.2))
    
    # Fondo transparente para quitar la caja blanca fija
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)

    resumen = df_sales.groupby("tipo_pago")["ingreso_neto"].sum()
    colores = ["#2ecc71" if "EFECTIVO" in str(x) else "#3498db" for x in resumen.index]
    
    bars = ax.bar(resumen.index, resumen.values, color=colores, width=0.4, edgecolor="none")
    
    ax.set_ylabel("Ingresos Netos ($ MXN)", fontsize=11, fontweight="bold", color="#8b949e")
    ax.set_title("Rendimiento del Día por Canal de Pago", fontsize=14, fontweight="bold", color="#ffffff", pad=20)
    ax.grid(axis="y", linestyle="--", alpha=0.2, color="#ffffff")
    
    # Remover bordes rígidos superior y derecho del marco
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#30363d')
    ax.spines['bottom'].set_color('#30363d')
    
    max_val = resumen.max() if not resumen.empty else 100
    ax.set_ylim(0, max_val * 1.25)
    
    for bar in bars:
        yval = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width()/2, 
            yval + (max_val * 0.03), 
            f"${yval:,.2f}", 
            ha="center", 
            va="bottom", 
            fontweight="bold", 
            fontsize=12, 
            color="#ffffff"
        )

    plt.xticks(rotation=10, ha="right", fontsize=11, color="#c9d1d9")
    plt.yticks(fontsize=10, color="#8b949e")
    
    plt.tight_layout()
    return fig