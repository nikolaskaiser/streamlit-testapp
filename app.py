
# streamlit_app.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Beispiel-Daten für die drei Reviere
data = {
    'Indikator': [
        'Kohleanteil (umgekehrt)',  # 100 = kein Kohleanteil mehr
        'Rückbau Kohlekapazität',
        'THG-Reduktion Energiewirtschaft',
        'Strukturwandel-Investitionen',
        'Politisches Commitment'
    ],
    'Rheinisches Revier': [60, 80, 75, 65, 90],
    'Lausitzer Revier': [30, 20, 25, 85, 70],
    'Mitteldeutsches Revier': [55, 85, 80, 40, 60]
}

# In DataFrame umwandeln
df = pd.DataFrame(data)

# Streamlit App
st.set_page_config(page_title="Energiewende-Indikator", layout="centered")
st.title("🌍 Energiewende-Indikator – Kohleausstieg in den drei Revieren")
st.markdown("Diese App zeigt den Fortschritt der drei Braunkohlereviere in fünf Indikatorfeldern.")

# Radar-Chart erstellen
fig = go.Figure()

for region in ['Rheinisches Revier', 'Lausitzer Revier', 'Mitteldeutsches Revier']:
    fig.add_trace(go.Scatterpolar(
        r=df[region],
        theta=df['Indikator'],
        fill='toself',
        name=region
    ))

# Layout anpassen
fig.update_layout(
    polar=dict(
        radialaxis=dict(visible=True, range=[0, 100])
    ),
    showlegend=True
)

# Plot anzeigen
st.plotly_chart(fig)

st.caption("Interaktive Visualisierung eines MVP-Indikators für den Kohleausstieg auf Revierebene.")




# ----------------------------
# Alle Daten als Dictionary
# ----------------------------
region_data = {
    'Nordrhein-Westfalen': {
        'Jahr': list(range(1990, 2023)),
        'Braunkohle_TWh': [
            72.8, 75.3, 77.8, 73.5, 75.3, 71.9, 73.0, 74.2, 75.4, 74.5, 74.7, 70.9, 73.8, 74.0, 73.1,
            71.2, 75.5, 74.3, 75.4, 66.5, 70.3, 73.6, 72.2, 70.4, 72.0, 75.0, 69.4, 66.5, 65.0, 52.3,
            41.5, 46.1, 38.3
        ],
        'Zieljahr': 2030
    },
    'Brandenburg': {
        'Jahr': list(range(2003, 2023)),
        'Braunkohle_TWh': [
            34.67, 35.85, 35.67, 33.92, 35.04, 33.48, 28.90, 32.89,
            32.32, 30.76, 28.51, 30.54, 29.81, 26.69, 25.59, 24.71,
            22.91, 19.44, 20.47, 17.95
        ],
        'Zieljahr': 2038
    },
    'Sachsen': {
        'Jahr': list(range(1990, 2023)),
        'Braunkohle_TWh': [
            40.43, 34.09, 32.94, 33.40, 32.39, 30.43, 29.54, 28.78, 27.61, 25.77, 25.33,
            24.26, 25.89, 26.89, 26.59, 25.10, 26.55, 26.46, 26.13, 21.39,
            23.97, 25.59, 25.25, 25.31, 26.39, 26.61, 24.85, 22.80, 21.94,
            18.83, 19.42, 19.74, 17.20
        ],
        'Zieljahr': 2038
    },
    'Sachsen-Anhalt': {
        'Jahr': list(range(1991, 2023)),
        'Braunkohle_TWh': [
            4.83, 3.48, 2.18, 2.24, 2.18, 2.36, 2.31, 2.36, 2.25,
            2.26, 2.18, 2.33, 2.28, 2.15, 2.04, 2.15, 2.18, 2.01,
            1.78, 2.03, 2.08, 2.02, 1.99, 1.89, 1.87, 1.79, 1.72,
            1.58, 1.59, 1.28, 1.36, 1.15
        ],
        'Zieljahr': 2038
    }
}

# ----------------------------
# Streamlit UI
# ----------------------------
st.subheader("📊 Vergleich: Braunkohlestromerzeugung nach Bundesland")
regionen = list(region_data.keys())
selected_region = st.selectbox("Wähle ein Bundesland oder 'Deutschland gesamt'", ["Deutschland gesamt"] + regionen)

if selected_region == "Deutschland gesamt":
    # Neue offizielle Daten für Deutschland (2019–2024)
    df = pd.DataFrame({
        "Jahr": [2019, 2020, 2021, 2022, 2023, 2024],
        "Bruttostrom_TWh": [608.2, 574.7, 587.1, 577.9, 511.3, 497.3],
        "Braunkohle_TWh": [114.0, 91.7, 110.1, 116.2, 86.3, 79.2],
    })
    df["Braunkohle_Anteil_%"] = (df["Braunkohle_TWh"] / df["Bruttostrom_TWh"]) * 100
    zieljahr = 2038

    fig = go.Figure()

    # Balken für TWh
    fig.add_trace(go.Bar(
        x=df["Jahr"],
        y=df["Braunkohle_TWh"],
        name="Braunkohle-Strom (TWh)",
        marker_color="firebrick",
        yaxis="y1"
    ))

    # Linie für Anteil %
    fig.add_trace(go.Scatter(
        x=df["Jahr"],
        y=df["Braunkohle_Anteil_%"],
        mode="lines+markers",
        name="Braunkohle-Anteil (%)",
        line=dict(color="royalblue", width=3, dash="dash"),
        yaxis="y2"
    ))

    # Zielmarke
    fig.add_trace(go.Scatter(
        x=[zieljahr],
        y=[0],
        mode="markers+text",
        name=f"Ziel {zieljahr}",
        marker=dict(color="green", size=12),
        text=["Ziel: 0 TWh"],
        textposition="top center",
        yaxis="y1"
    ))

    # Layout mit zwei y-Achsen
    fig.update_layout(
        title="Braunkohlestrom in Deutschland – absolut & relativ",
        xaxis=dict(title="Jahr"),
        yaxis=dict(
            title="Braunkohle-Strom (TWh)",
            side="left",
            showgrid=False
        ),
        yaxis2=dict(
            title="Anteil Braunkohle (%)",
            overlaying="y",
            side="right",
            showgrid=False,
            range=[0, max(df["Braunkohle_Anteil_%"]) + 5]
        ),
        barmode='group',
        legend=dict(x=0.01, y=1.1, orientation="h"),
        height=600
    )

    st.plotly_chart(fig)

else:
    region = region_data[selected_region]
    df = pd.DataFrame({
        'Jahr': region['Jahr'],
        'Braunkohle_TWh': region['Braunkohle_TWh']
    })
    zieljahr = region['Zieljahr']

# ----------------------------
# Plotly-Grafik
# ----------------------------
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df['Jahr'],
    y=df['Braunkohle_TWh'],
    mode='lines+markers',
    name=f'{selected_region} – Braunkohle'
))

fig.add_trace(go.Scatter(
    x=[zieljahr],
    y=[0],
    mode='markers+text',
    name=f'Ziel {zieljahr}',
    marker=dict(color='green', size=12),
    text=[f"Ziel: 0 TWh"],
    textposition='top center'
))

fig.update_layout(
    title=f'Bruttostromerzeugung aus Braunkohle – {selected_region}',
    xaxis_title='Jahr',
    yaxis_title='TWh',
    showlegend=True
)

st.plotly_chart(fig)




import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ----------------------------
# Alle Daten
# ----------------------------
region_data = {
    'Nordrhein-Westfalen': {
        'Jahr': list(range(1990, 2023)),
        'Braunkohle_TWh': [
            72.8, 75.3, 77.8, 73.5, 75.3, 71.9, 73.0, 74.2, 75.4, 74.5, 74.7, 70.9, 73.8, 74.0, 73.1,
            71.2, 75.5, 74.3, 75.4, 66.5, 70.3, 73.6, 72.2, 70.4, 72.0, 75.0, 69.4, 66.5, 65.0, 52.3,
            41.5, 46.1, 38.3
        ],
        'Zieljahr': 2030
    },
    'Brandenburg': {
        'Jahr': list(range(2003, 2023)),
        'Braunkohle_TWh': [
            34.67, 35.85, 35.67, 33.92, 35.04, 33.48, 28.90, 32.89,
            32.32, 30.76, 28.51, 30.54, 29.81, 26.69, 25.59, 24.71,
            22.91, 19.44, 20.47, 17.95
        ],
        'Zieljahr': 2038
    },
    'Sachsen': {
        'Jahr': list(range(1990, 2023)),
        'Braunkohle_TWh': [
            40.43, 34.09, 32.94, 33.40, 32.39, 30.43, 29.54, 28.78, 27.61, 25.77, 25.33,
            24.26, 25.89, 26.89, 26.59, 25.10, 26.55, 26.46, 26.13, 21.39,
            23.97, 25.59, 25.25, 25.31, 26.39, 26.61, 24.85, 22.80, 21.94,
            18.83, 19.42, 19.74, 17.20
        ],
        'Zieljahr': 2038
    },
    'Sachsen-Anhalt': {
        'Jahr': list(range(1991, 2023)),
        'Braunkohle_TWh': [
            4.83, 3.48, 2.18, 2.24, 2.18, 2.36, 2.31, 2.36, 2.25,
            2.26, 2.18, 2.33, 2.28, 2.15, 2.04, 2.15, 2.18, 2.01,
            1.78, 2.03, 2.08, 2.02, 1.99, 1.89, 1.87, 1.79, 1.72,
            1.58, 1.59, 1.28, 1.36, 1.15
        ],
        'Zieljahr': 2038
    },
    "Berlin": {
        "Jahr": [2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017],
        "Braunkohle_TWh": [0.77, 0.81, 0.76, 0.68, 0.72, 0.71, 0.74, 0.79, 0.73, 0.75, 0.68, 0.69, 0.65, 0.69, 0.33],
        "Zieljahr": 2038
    },
    "Hessen": {
        "Jahr": list(range(1990, 2024)),
        "Braunkohle_TWh": [
            0.738, 0.473, 0.153, 0.150, 0.142, 0.155, 0.167, 0.148, 0.150, 0.082, 0.093,
            0.144, 0.100, 0.058, 0.070, 0.084, 0.088, 0.100, 0.118, 0.077, 0.069, 0.073,
            0.051, 0.057, 0.076, 0.088, 0.089, 0.082, 0.062, 0.084, 0.080, 0.099, 0.089, 0.085
        ],
        "Zieljahr": 2038
    },
    "Niedersachsen": {
        "Jahr": list(range(2003, 2019)),
        "Braunkohle_TWh": [
            2.94, 2.72, 2.50, 2.22, 2.61, 2.54, 2.21, 2.31, 1.79, 2.27, 1.56, 2.83, 2.33, 1.87, 0.0, 0.0
        ],
        "Zieljahr": 2038
    },
    "Saarland": {
        "Jahr": list(range(2003, 2018)),
        "Braunkohle_TWh": [
            0.015, 0.004, 0.017, 0.014, 0.010, None, 0.001, None, None, 0.004, 0.033, 0.030, 0.014, None, None
        ],
        "Zieljahr": 2038
    },
    "Thüringen": {
        "Jahr": [1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998],
        "Braunkohle_TWh": [1.30, 1.10, 1.14, 0.33, 0.13, 0.07, 0.03, 0.02],
        "Zieljahr": 2038
    }
}

# ----------------------------
# Streamlit UI
# ----------------------------
st.subheader("📈 Braunkohlestromerzeugung – Regionenvergleich")
selected_regions = st.multiselect(
    "Wähle Bundesländer zum Vergleich",
    options=list(region_data.keys()),
    default=["Nordrhein-Westfalen", "Brandenburg"]
)

# ----------------------------
# Plot erstellen
# ----------------------------
fig = go.Figure()

for region in selected_regions:
    region_info = region_data[region]
    df = pd.DataFrame({
        'Jahr': region_info['Jahr'],
        'Braunkohle_TWh': region_info['Braunkohle_TWh']
    })

    fig.add_trace(go.Scatter(
        x=df['Jahr'],
        y=df['Braunkohle_TWh'],
        mode='lines+markers',
        name=region
    ))

    # Zieljahr markieren
    fig.add_trace(go.Scatter(
        x=[region_info['Zieljahr']],
        y=[0],
        mode='markers+text',
        marker=dict(size=10, color='green'),
        text=[f"{region_info['Zieljahr']} Ziel"],
        textposition='top center',
        showlegend=False
    ))

fig.update_layout(
    title='Bruttostromerzeugung aus Braunkohle im Vergleich',
    xaxis_title='Jahr',
    yaxis_title='TWh',
    legend_title='Bundesland',
    height=600
)

st.plotly_chart(fig)



import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Daten laden
@st.cache_data

def load_data():
    df = pd.read_csv("bereinigte_daten.csv")  # Du kannst das DataFrame direkt einbinden, falls nicht als Datei
    return df

data = load_data()

# Seitenlayout
st.title("🔌 Bruttostromerzeugung aus Braunkohle in Deutschland")
st.markdown("""
Wähle Bundesländer aus, um deren Stromerzeugung aus Braunkohle über die Jahre zu vergleichen. 
Bei Auswahl von **Deutschland** wird zusätzlich der Anteil an der Gesamtstromerzeugung angezeigt.
""")

# Auswahl
bundeslaender = sorted(data['Bundesland'].unique())
default_value = ["Deutschland"] if "Deutschland" in bundeslaender else [bundeslaender[0]]
auswahl = st.multiselect("Bundesländer auswählen:", options=bundeslaender, default=default_value)

# Plot absolute Erzeugung
fig, ax = plt.subplots(figsize=(10, 5))

for land in auswahl:
    df_land = data[data['Bundesland'] == land]
    ax.plot(df_land['Jahr'], df_land['Braunkohle_GWh'], label=land)

    # Marker für politische Ziele
    if land == "Deutschland":
        ax.axvline(2038, color='red', linestyle='--', linewidth=1)
        ax.text(2038, ax.get_ylim()[1]*0.95, 'Ausstieg 2038', rotation=90, color='red')
    elif land == "Nordrhein-Westfalen":
        ax.axvline(2030, color='orange', linestyle='--', linewidth=1)
        ax.text(2030, ax.get_ylim()[1]*0.95, 'NRW-Aus. 2030', rotation=90, color='orange')

ax.set_title("Bruttostromerzeugung aus Braunkohle (in GWh)")
ax.set_xlabel("Jahr")
ax.set_ylabel("GWh")
ax.legend()
st.pyplot(fig)

# Nur wenn "Deutschland" gewählt wurde: Anteil anzeigen
if "Deutschland" in auswahl:
    df_dt = data[data['Bundesland'] == "Deutschland"]
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    ax2.plot(df_dt['Jahr'], df_dt['Braunkohle_Anteil_%'], color='green')
    ax2.axvline(2038, color='red', linestyle='--', linewidth=1)
    ax2.text(2038, ax2.get_ylim()[1]*0.95, 'Ausstieg 2038', rotation=90, color='red')

    ax2.set_title("Anteil Braunkohle an Bruttostromerzeugung Deutschland (%)")
    ax2.set_xlabel("Jahr")
    ax2.set_ylabel("% Anteil")
    st.pyplot(fig2)


