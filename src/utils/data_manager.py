import os
import json
import pandas as pd
from datetime import datetime

DATA_DIR = "data"
SALES_FILE = os.path.join(DATA_DIR, "sales_db.csv")
DEBTORS_FILE = os.path.join(DATA_DIR, "debtors_db.csv")
PENDING_SYNC_FILE = os.path.join(DATA_DIR, "pending_sync.json")

def init_db():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(SALES_FILE):
        df_sales = pd.DataFrame(columns=["id", "fecha", "monto", "tipo_pago", "comision", "ingreso_neto"])
        df_sales.to_csv(SALES_FILE, index=False)
        
    if not os.path.exists(DEBTORS_FILE):
        df_debtors = pd.DataFrame(columns=["cliente", "deuda_total", "ultima_actualizacion"])
        df_debtors.to_csv(DEBTORS_FILE, index=False)
        
    if not os.path.exists(PENDING_SYNC_FILE):
        with open(PENDING_SYNC_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)

def get_sales():
    init_db()
    if os.path.exists(SALES_FILE) and os.path.getsize(SALES_FILE) == 0:
        # Recrea las columnas si el archivo se quedó vacío
        df_sales = pd.DataFrame(columns=["id", "fecha", "monto", "tipo_pago", "comision", "ingreso_neto"])
        df_sales.to_csv(SALES_FILE, index=False)
        return df_sales
    
    try:
        return pd.read_csv(SALES_FILE)
    except pd.errors.EmptyDataError:
        df_sales = pd.DataFrame(columns=["id", "fecha", "monto", "tipo_pago", "comision", "ingreso_neto"])
        df_sales.to_csv(SALES_FILE, index=False)
        return df_sales

def add_sale(monto, tipo_pago, comision=0.0):
    init_db()
    df = get_sales()
    ingreso_neto = monto - comision
    nueva_venta = {
        "id": len(df) + 1,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "monto": float(monto),
        "tipo_pago": tipo_pago,
        "comision": float(comision),
        "ingreso_neto": float(ingreso_neto)
    }
    df = pd.concat([df, pd.DataFrame([nueva_venta])], ignore_index=False)
    df.to_csv(SALES_FILE, index=False)
    return nueva_venta

def get_debtors():
    init_db()
    return pd.read_csv(DEBTORS_FILE)

def add_or_update_debtor(cliente, monto_adicional):
    init_db()
    df = get_debtors()
    cliente = cliente.strip()
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if cliente in df["cliente"].values:
        df.loc[df["cliente"] == cliente, "deuda_total"] += float(monto_adicional)
        df.loc[df["cliente"] == cliente, "ultima_actualizacion"] = ahora
    else:
        nuevo = {"cliente": cliente, "deuda_total": float(monto_adicional), "ultima_actualizacion": ahora}
        df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=False)
        
    df.to_csv(DEBTORS_FILE, index=False)

def pay_debt(cliente, monto_pago):
    init_db()
    df = get_debtors()
    if cliente in df["cliente"].values:
        df.loc[df["cliente"] == cliente, "deuda_total"] -= float(monto_pago)
        df.loc[df["cliente"] == cliente, "ultima_actualizacion"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Evitar deudas negativas
        df.loc[df["deuda_total"] < 0, "deuda_total"] = 0
        df.to_csv(DEBTORS_FILE, index=False)
        add_sale(monto_pago, "EFECTIVO (Pago Fiado)")