import streamlit as st
import re
import pandas as pd

st.title("Conversor de Bandas Horarias")

texto = st.text_area("Pegue aquí el texto:", height=200)

if st.button("Procesar"):

    indices = []

    for linea in texto.split("\n"):
        match = re.search(r'H(\d+)\s+QH(\d)', linea, re.IGNORECASE)
        if match:
            h = int(match.group(1))
            q = int(match.group(2))
            indice = (h-1)*4 + (q-1)
            indices.append(indice)

    if not indices:
        st.warning("No se detectaron horarios.")
        st.stop()

    indices = sorted(indices)

    bloques = []
    inicio = indices[0]
    anterior = indices[0]

    for i in indices[1:]:
        if i == anterior + 1:
            anterior = i
        else:
            bloques.append((inicio, anterior))
            inicio = i
            anterior = i

    bloques.append((inicio, anterior))

    timeline = []
    current = 0
    for b in bloques:
        if current < b[0]:
            timeline.append((current, b[0]-1, "Control Garray"))
        timeline.append((b[0], b[1], "Control Axpo"))
        current = b[1] + 1

    if current < 96:
        timeline.append((current, 95, "Gestion Garray"))

    resultados = []
    for t in timeline:
        start = t[0]*15
        end = (t[1]+1)*15

        sh = start//60
        sm = start%60
        eh = end//60
        em = end%60

        resultados.append({
            "Inicio": f"{sh:02d}:{sm:02d}",
            "Fin": f"{eh:02d}:{em:02d}",
            "Control": t[2]
        })

    df = pd.DataFrame(resultados)

    # ---- ESTILO DE TABLA ----

    styled_df = (
        df.style
        .set_table_styles([
            {"selector": "th", "props": [
                ("font-size", "18px"),
                ("font-weight", "bold"),
                ("text-align", "center"),
                ("border", "2px solid black")
            ]},
            {"selector": "td", "props": [
                ("font-size", "17px"),
                ("text-align", "center"),
                ("border", "1px solid black")
            ]},
            {"selector": "table", "props": [
                ("border-collapse", "collapse"),
                ("width", "100%")
            ]}
        ])
    )

    st.subheader("Resultado")

    st.dataframe(
        styled_df,
        hide_index=True,
        use_container_width=True
    )
