import altair as alt
import pandas as pd
import streamlit as st

from src.data_loader import load_data

st.set_page_config(
    page_title="Avaliação de correlação e distribuição — ITBI Recife",
    layout="wide",
)

st.title("Avaliação de correlação e distribuição — ITBI Recife")

df = load_data()

# Variáveis quantitativas do estudo (mesma lista VARS_QUANT do notebook de EDA)
VARS_QUANT = ["ano_construcao", "area_terreno", "area_construida", "fracao_ideal", "valor_avaliacao"]

# Sidebar: filtros (variáveis + intervalo + tipo de ocupação)
with st.sidebar:
    st.header("Filtros")

    variaveis = st.multiselect(
        "Variáveis quantitativas",
        options=VARS_QUANT,
        default=VARS_QUANT,
        help="Selecione as variáveis quantitativas que deseja analisar no dashboard.",
    )

    separar_por_ocupacao = st.toggle(
        "Distinguir por tipo de ocupação",
        value=False,
        help="Colore a distribuição por tipo_ocupa_bin (Residencial ou Comercial).",
    )

    # Um slider de intervalo para cada variável selecionada
    intervalos = {}
    for var in variaveis:
        if pd.api.types.is_integer_dtype(df[var]):
            minimo, maximo, passo = int(df[var].min()), int(df[var].max()), 1
        else:
            minimo, maximo, passo = float(df[var].min()), float(df[var].max()), 0.1
        intervalos[var] = st.slider(
            f"Intervalo de {var}",
            min_value=minimo,
            max_value=maximo,
            value=(minimo, maximo),
            step=passo,
            key=f"intervalo_{var}",
        )

# Mantém só os imóveis dentro de todos os intervalos escolhidos
df_filtrado = df
for var, (inicio, fim) in intervalos.items():
    df_filtrado = df_filtrado[df_filtrado[var].between(inicio, fim)]

st.caption(f"{len(df_filtrado)} de {len(df)} imóveis dentro dos intervalos escolhidos.")

# Dashboard 1 (rascunho prompts/rascunho_dashboard1.png): sidebar à esquerda,
# Distribuição em cima e Correlação embaixo, empilhadas à direita.
st.subheader("Distribuição")

if not variaveis:
    st.warning("Selecione pelo menos uma variável para ver a distribuição.")
elif df_filtrado.empty:
    st.info("Nenhum imóvel dentro dos intervalos escolhidos — ajuste os filtros para ver a distribuição.")
else:
    variavel_hist = st.segmented_control(
        "Variável do histograma",
        options=variaveis,
        default=variaveis[0],
    )

    if variavel_hist is None:
        st.info("Selecione uma variável acima para gerar o histograma.")
    else:
        encode = {
            "x": alt.X(f"{variavel_hist}:Q", bin=alt.Bin(maxbins=40), title=variavel_hist),
            "y": alt.Y("count():Q", title="Contagem"),
        }
        if separar_por_ocupacao:
            encode["color"] = alt.Color("tipo_ocupa_bin:N", title="Tipo de ocupação")

        histograma = alt.Chart(df_filtrado).mark_bar().encode(**encode)
        st.altair_chart(histograma, alt=f"Distribuição de {variavel_hist} entre os imóveis filtrados")

st.subheader("Correlação")

if len(variaveis) < 2:
    st.warning("Selecione pelo menos 2 variáveis para calcular a correlação.")
elif len(df_filtrado) < 2:
    st.info("Menos de 2 imóveis dentro dos intervalos escolhidos — ajuste os filtros para calcular a correlação.")
else:
    matriz_corr = df_filtrado[variaveis].corr(method="spearman")
    corr_long = matriz_corr.reset_index(names="variavel_x").melt(
        id_vars="variavel_x", var_name="variavel_y", value_name="correlacao"
    )

    heatmap = (
        alt.Chart(corr_long)
        .mark_rect()
        .encode(
            x=alt.X("variavel_x:N", title=None, sort=variaveis),
            y=alt.Y("variavel_y:N", title=None, sort=variaveis),
            color=alt.Color(
                "correlacao:Q",
                title="Correlação (Spearman)",
                scale=alt.Scale(scheme="redblue", domain=[-1, 1]),
            ),
            tooltip=["variavel_x", "variavel_y", alt.Tooltip("correlacao:Q", format=".2f")],
        )
    )
    rotulos = heatmap.mark_text(baseline="middle").encode(
        text=alt.Text("correlacao:Q", format=".2f"),
        color=alt.condition("abs(datum.correlacao) > 0.5", alt.value("white"), alt.value("black")),
    )
    st.altair_chart(
        heatmap + rotulos,
        alt=f"Matriz de correlação de Spearman entre {', '.join(variaveis)}",
    )

# TODO: Dashboard 2 — KPIs (Aula 22)
