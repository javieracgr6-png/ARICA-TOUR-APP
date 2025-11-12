# ==========================================================
#  ARICA GO! – Asistente Turístico (Streamlit)
#  Navegación sin radios; botones que cambian de sección.
#  Barra lateral mínima (logo + ubicación). “Volver al inicio”
# ==========================================================

import streamlit as st
import pandas as pd
from datetime import datetime
from math import radians, sin, cos, asin, sqrt
import requests
import os

# ------------- Config general -------------
LOGO_PATH = "logo.png"      # pon tu logo en la raíz con este nombre
APP_TITLE = "Asistente Turístico · Arica y Parinacota"

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=LOGO_PATH if os.path.exists(LOGO_PATH) else "🌞",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------- Estilos (CSS) tipo app móvil -------------
CARD_CSS = """
<style>
:root { --radius: 16px; --shadow: 0 10px 25px rgba(0,0,0,.08); }

.hero {
  border-radius: var(--radius); padding: 16px 18px;
  background: linear-gradient(135deg,#0ea5e9, #22d3ee);
  color: #fff; box-shadow: var(--shadow); margin-bottom: 14px;
}
.hero h2 { margin: 0 0 10px 0; font-weight: 800; }
.hero .chips { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.chip {
  background: rgba(255,255,255,.18); border-radius: 12px; padding: 10px 12px; backdrop-filter: blur(4px);
  border: 1px solid rgba(255,255,255,.25); font-size: 14px;
}

.grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }
.tile {
  border-radius: var(--radius); background: #ffffff; box-shadow: var(--shadow); padding: 16px;
  border: 1px solid #eef2f7;
}
.tile h4 { margin: 0 0 6px 0; font-weight: 800; }
.tile p { margin: 0 0 10px 0; color: #607083; font-size: 13px; min-height: 32px;}
.btn-full { width: 100%; border: none; border-radius: 10px; padding: 10px 12px; background: #0ea5e9; color: #fff; cursor: pointer; }
.badge { display:inline-block; padding: 2px 8px; border-radius: 999px; background: rgba(255,255,255,.25); font-size: 12px; }
.small { font-size: 12px; opacity: .9 }
</style>
"""
st.markdown(CARD_CSS, unsafe_allow_html=True)

# ------------- Helpers: distancia, ubicación, clima, cercanos -------------

def km_haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    p1, p2 = radians(lat1), radians(lat2)
    dphi = radians(lat2 - lat1)
    dlmb = radians(lon2 - lon1)
    a = sin(dphi/2)**2 + cos(p1)*cos(p2)*sin(dlmb/2)**2
    return 2 * R * asin(sqrt(a))

def ip_geolocate():
    """Ubicación aproximada por IP pública (puede devolver el país del servidor)."""
    try:
        r = requests.get("https://ipapi.co/json/", timeout=5)
        j = r.json()
        return float(j.get("latitude", -18.4783)), float(j.get("longitude", -70.3126)), j.get("city", "Arica"), j.get("country_name", "Chile")
    except Exception:
        return -18.4783, -70.3126, "Arica", "Chile"

def current_weather(lat, lon):
    """Clima actual (Open-Meteo)."""
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        j = requests.get(url, timeout=6).json()
        t = j["current_weather"]["temperature"]
        return t, "Despejado"
    except Exception:
        return None, "—"

def nearby_places(df, lat, lon, max_km=6.0, limit=8):
    rows = []
    for _, r in df.iterrows():
        d = km_haversine(lat, lon, r["lat"], r["lon"])
        if d <= max_km:
            rows.append((d, r["nombre"], r))
    rows.sort(key=lambda x: x[0])
    return rows[:limit]

# -------------------------------------------------------------------------
# ESTADO: página activa y selección
# -------------------------------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "HOME"   # HOME, CERCANOS, PLAN, FX, BUSCAR
if "seleccion" not in st.session_state:
    st.session_state.seleccion = set()

# -------------------------------------------------------------------------
# SIDEBAR mínimo (solo branding + ubicación)
# -------------------------------------------------------------------------
if os.path.exists(LOGO_PATH):
    st.sidebar.image(LOGO_PATH, width=140)

st.sidebar.title("📌 Ubicación")
modo_ubi = st.sidebar.selectbox("Elegir:", ["Arica (fijar)", "Detectar por IP", "Manual"], index=0)

if modo_ubi == "Arica (fijar)":
    lat, lon = -18.4783, -70.3126
    city, country = "Arica", "Chile"
elif modo_ubi == "Manual":
    lat = st.sidebar.number_input("Latitud", value=-18.478300, step=0.0001, format="%.6f")
    lon = st.sidebar.number_input("Longitud", value=-70.312600, step=0.0001, format="%.6f")
    city, country = "Ubicación manual", "—"
else:
    lat, lon, city, country = ip_geolocate()

temp, wx = current_weather(lat, lon)
st.sidebar.markdown(f"**Clima**: {wx} {(str(temp)+'°C') if temp is not None else ''}")
st.sidebar.caption(f"Lat: {round(lat,4)}  Lon: {round(lon,4)}")

# Botón global para volver al inicio si no estamos en HOME
if st.session_state.page != "HOME":
    if st.sidebar.button("← Volver al inicio", use_container_width=True):
        st.session_state.page = "HOME"
        st.rerun()

# -------------------------------------------------------------------------
# DATOS (puedes reemplazar por tu dataset real)
# -------------------------------------------------------------------------
# Ejemplo mínimo por si no tienes CSV aún:
data_ejemplo = [
    {"id": 1, "nombre": "Playa Chinchorro", "tipo":"Playa", "lat": -18.4527, "lon": -70.3106,
     "desc":"Amplia playa urbana, ideal para caminar.", "img": ""},
    {"id": 2, "nombre": "Cuevas de Anzota", "tipo":"Mirador", "lat": -18.5306, "lon": -70.3326,
     "desc":"Formaciones rocosas con sendero y vistas al mar.", "img": ""},
    {"id": 3, "nombre": "Museo San Miguel de Azapa", "tipo":"Museo", "lat": -18.5180, "lon": -70.1813,
     "desc":"Muestra arqueológica de cultura Chinchorro.", "img": ""},
    {"id": 4, "nombre": "Humedal del Río Lluta", "tipo":"Naturaleza", "lat": -18.4235, "lon": -70.3207,
     "desc":"Santuario de aves cercano a la ciudad.", "img": ""},
]
ATRACTIVOS = pd.DataFrame(data_ejemplo)

# -------------------------------------------------------------------------
# VISTAS
# -------------------------------------------------------------------------

def vista_home():
    today = datetime.now().strftime("%d %b %Y")

    st.markdown(
        f"""
        <div class="hero">
          <h2>🌍 {APP_TITLE}</h2>
          <div class="chips">
            <div class="chip"><b>📍 Ubicación</b><br><span class="small">{city}, {country}</span></div>
            <div class="chip"><b>☀️ Clima</b><br><span class="small">{wx} {(str(temp)+'°C') if temp is not None else ''}</span></div>
            <div class="chip"><b>📅 Hoy</b><br><span class="small">{today}</span></div>
            <div class="chip"><b>🧭 Coords</b><br><span class="small">{round(lat,4)}, {round(lon,4)}</span></div>
          </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="grid">', unsafe_allow_html=True)

    # Tile 1: cercanos
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="tile"><h4>📍 Lugares cerca de ti</h4>'
                    '<p>Explora atracciones a menos de ~6 km.</p>', unsafe_allow_html=True)
        if st.button("Ver cercanos", use_container_width=True):
            st.session_state.page = "CERCANOS"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Tile 2: planificador
    with c2:
        st.markdown('<div class="tile"><h4>🗺️ Planificar itinerario</h4>'
                    '<p>Optimiza por cercanía, tiempos y gustos.</p>', unsafe_allow_html=True)
        if st.button("Ir al planificador", use_container_width=True):
            st.session_state.page = "PLAN"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown('<div class="tile"><h4>💱 Convertir moneda</h4>'
                    '<p>CLP ⇄ USD/EUR/BOB/PEN con tasas reales.</p>', unsafe_allow_html=True)
        if st.button("Abrir conversor", use_container_width=True):
            st.session_state.page = "FX"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with c4:
        st.markdown('<div class="tile"><h4>⭐ Buscar atracciones</h4>'
                    '<p>Filtra por tipo, busca y agrega a tu plan.</p>', unsafe_allow_html=True)
        if st.button("Ir a explorar", use_container_width=True):
            st.session_state.page = "BUSCAR"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

def vista_cercanos():
    st.subheader("📍 Lugares cerca de ti")
    cercanos = nearby_places(ATRACTIVOS, lat, lon, max_km=6.0, limit=10)
    if not cercanos:
        st.info("No se encontraron lugares a ~6 km.")
        return
    for d, nombre, r in cercanos:
        with st.container(border=True):
            st.markdown(f"**{nombre}** · {d:.1f} km — {r['tipo']}")
            st.caption(r["desc"])
            if st.button(f"Añadir al itinerario (+)", key=f"add_{r['id']}"):
                st.session_state.seleccion.add(int(r["id"]))
                st.success("Añadido ✅")

def vista_plan():
    st.subheader("🗺️ Planificador (borrador)")
    st.write("Elementos seleccionados:")
    if st.session_state.seleccion:
        df_sel = ATRACTIVOS[ATRACTIVOS["id"].isin(st.session_state.seleccion)]
        st.dataframe(df_sel[["nombre","tipo","lat","lon"]], use_container_width=True)
    else:
        st.info("Aún no agregas lugares. Ve a 'Lugares cerca de ti' o 'Buscar atracciones' y añade algunos.")

def vista_fx():
    st.subheader("💱 Conversor de moneda")
    cols = ["CLP","USD","EUR","BOB","PEN"]
    m_from = st.selectbox("Desde", cols, index=0)
    m_to   = st.selectbox("Hacia", cols, index=1)
    monto  = st.number_input("Monto", min_value=0.0, value=10000.0, step=100.0, format="%.2f")

    if st.button("Convertir", type="primary"):
        try:
            url = f"https://api.exchangerate.host/convert?from={m_from}&to={m_to}&amount={monto}"
            j = requests.get(url, timeout=8).json()
            st.success(f"≈ {j['result']:,.2f} {m_to}")
        except Exception:
            st.error("No fue posible consultar las tasas en este momento.")

def vista_buscar():
    st.subheader("⭐ Buscar atracciones")
    q = st.text_input("🔎 Busca por nombre o filtra por tipo (ej: playa, museo, mirador)")
    tipo = st.multiselect("Filtrar por tipo", sorted(ATRACTIVOS["tipo"].unique().tolist()))
    df = ATRACTIVOS.copy()
    if q:
        df = df[df["nombre"].str.contains(q, case=False, na=False)]
    if tipo:
        df = df[df["tipo"].isin(tipo)]
    if df.empty:
        st.info("Sin resultados.")
        return
    for _, r in df.iterrows():
        with st.container(border=True):
            st.markdown(f"**{r['nombre']}** — {r['tipo']}")
            st.caption(r["desc"])
            if st.button("Añadir al itinerario (+)", key=f"b_{r['id']}"):
                st.session_state.seleccion.add(int(r["id"]))
                st.success("Añadido ✅")

# -------------------------------------------------------------------------
# ROUTER
# -------------------------------------------------------------------------
if st.session_state.page == "HOME":
    vista_home()
elif st.session_state.page == "CERCANOS":
    vista_cercanos()
elif st.session_state.page == "PLAN":
    vista_plan()
elif st.session_state.page == "FX":
    vista_fx()
elif st.session_state.page == "BUSCAR":
    vista_buscar()
