import altair as alt
import pandas as pd
import streamlit as st

from src.data_loader import load_data

st.set_page_config(
    page_title="ITBI Recife — dashboards",
    layout="wide",
)

st.title("ITBI Recife — dashboards")

df = load_data()

# Variáveis quantitativas do estudo (mesma lista VARS_QUANT do notebook de EDA)
VARS_QUANT = ["ano_construcao", "area_terreno", "area_construida", "fracao_ideal", "valor_avaliacao"]

# Sidebar: filtros do Dashboard 1 (variáveis + intervalo + tipo de ocupação).
# O Dashboard 2 tem seus próprios widgets (período + categoria), definidos dentro da aba.
with st.sidebar:
    st.header("Filtros — Dashboard 1")

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

tab_dashboard1, tab_dashboard2 = st.tabs(
    ["Dashboard 1 — correlação e distribuição", "Dashboard 2 — KPIs"]
)

with tab_dashboard1:
    # Rascunho: entregas/rascunho-dashboard1.png — sidebar à esquerda, Distribuição
    # em cima e Correlação embaixo, empilhadas à direita.
    st.caption(f"{len(df_filtrado)} de {len(df)} imóveis dentro dos intervalos escolhidos.")

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

with tab_dashboard2:
    # Rascunho: entregas/rascunho-dashboard2.png — filtros no topo, 4 KPIs numa
    # linha, gráfico de barras embaixo. Métricas justificadas em
    # entregas/justificativa-metricas.md.
    ano_minimo, ano_maximo = int(df["ano"].min()), int(df["ano"].max())

    col_periodo, col_categoria = st.columns([2, 1])
    with col_periodo:
        periodo = st.slider(
            "Período (ano da transação)",
            min_value=ano_minimo,
            max_value=ano_maximo,
            value=(ano_minimo, ano_maximo),
        )
    with col_categoria:
        categoria = st.segmented_control(
            "Tipo de ocupação",
            options=["Todos", "Residencial", "Comercial"],
            default="Todos",
        )

    df_dashboard2 = df[df["ano"].between(*periodo)]
    if categoria and categoria != "Todos":
        df_dashboard2 = df_dashboard2[df_dashboard2["tipo_ocupa_bin"] == categoria]

    # Gráfico de barras com seleção cruzada (ver ALTAIR-CROSSFILTER.md, exemplo 3):
    # clicar numa barra filtra os KPIs acima só para aquele(s) ano(s).
    clique_ano = alt.selection_point(name="clique_ano", fields=["ano"])

    barras_ano = (
        alt.Chart(df_dashboard2)
        .mark_bar()
        .encode(
            x=alt.X("ano:O", title="Ano da transação"),
            y=alt.Y("count():Q", title="Transações"),
            opacity=alt.condition(clique_ano, alt.value(1), alt.value(0.4)),
            tooltip=[alt.Tooltip("ano:O", title="Ano"), alt.Tooltip("count():Q", title="Transações")],
        )
        .add_params(clique_ano)
    )

    if df_dashboard2.empty:
        st.info("Nenhuma transação dentro do período/tipo de ocupação escolhidos — ajuste os filtros acima.")
    else:
        evento = st.altair_chart(
            barras_ano,
            key="barras_ano_dashboard2",
            on_select="rerun",
            alt="Número de transações de ITBI por ano; clique numa barra para destacar aquele ano nos indicadores",
        )

        itens_clicados = evento.selection.get("clique_ano", [])
        anos_selecionados = [item["ano"] for item in itens_clicados]
        df_destaque = (
            df_dashboard2[df_dashboard2["ano"].isin(anos_selecionados)] if anos_selecionados else df_dashboard2
        )

        if anos_selecionados:
            st.caption(f"Indicadores destacados para: {', '.join(str(a) for a in sorted(anos_selecionados))}.")

        col1, col2, col3, col4 = st.columns(4)

        if df_destaque.empty:
            st.info("Nenhum imóvel no filtro/seleção atual.")
        else:
            imoveis_construidos = df_destaque[df_destaque["area_construida"] > 0]
            valor_m2_mediano = (
                (imoveis_construidos["valor_avaliacao"] / imoveis_construidos["area_construida"]).median()
                if not imoveis_construidos.empty
                else None
            )
            pct_residencial = (df_destaque["tipo_ocupa_bin"] == "Residencial").mean() * 100

            col1.metric("Total de transações", f"{len(df_destaque):,}".replace(",", "."))
            col2.metric(
                "Valor mediano de avaliação",
                f"R$ {df_destaque['valor_avaliacao'].median():,.0f}".replace(",", "."),
            )
            col3.metric(
                "Valor mediano por m²",
                f"R$ {valor_m2_mediano:,.0f}".replace(",", ".") if valor_m2_mediano is not None else "—",
            )
            col4.metric("% Residencial", f"{pct_residencial:.1f}%")
