# Declaração de Uso de IA

**Nome:** Gabriel Miranda Mucarbel de Lima
**Data:** 22/10/2026 (Aula 21) e 29/10/2026 (Aula 22)

## Ferramenta

Claude Code (Claude Sonnet 5), via terminal.

## Como acompanhei o uso

Não pedi pra IA gerar tudo de uma vez: usei ela como apoio pra escrever o código, mas conduzindo e
revisando cada etapa.

- Pedi explicitamente pra dividir a Aula 22 em 7 partes pequenas, pra eu revisar e **comitar cada
  uma eu mesmo**, em vez de um commit único gerado pela IA.
- Antes de cada commit, conferi o `git diff`/resultado da parte (ex.: rodei o app, testei os
  widgets, olhei os números das métricas batendo com o que eu já conhecia da minha própria EDA).
- Fiz perguntas quando não tinha certeza do que tinha sido gerado (ex.: o que era o
  `meu_dataset.csv` em `data/raw/`) em vez de aceitar sem entender.
- Tomei decisões de design por conta própria quando o resultado não estava do jeito que eu queria
  (ex.: rejeitei o primeiro rascunho do Dashboard 1 com a sidebar à direita e pedi pra voltar pra
  esquerda).

## Prompt usado

### Aula 21 — Streamlit, parte 1 (22/10/2026)

- Pedi pra gerar os datasets `raw`/`clean` da minha própria EDA (ITBI Recife), seguindo o mesmo
  padrão de exportação que a professora usou no notebook de exemplo, a partir do meu notebook e do
  dataset original (zip baixado pela prefeitura).
- Pedi pra desenhar um rascunho do layout do Dashboard 1, baseado no exemplo da professora mas
  adaptado pro meu dataset.
- Pedi pra trocar a posição da sidebar nesse rascunho (voltar pra esquerda).

### Aula 22 — Streamlit, parte 2 (29/10/2026)

- Pedi pra seguir com a parte 2 da atividade, com base no slide da aula e no `ROTEIRO.md`
  atualizado pela professora, mas **dividindo o trabalho em partes pequenas** pra eu revisar e
  comitar cada uma por conta própria

A partir daí, confirmei cada uma das 7 partes individualmente, depois de revisar o diff/resultado de
cada uma, antes de dar o commit.

## O que foi aceito, modificado ou rejeitado e por quê

- **Aceito:**
  - Geração de `data/raw/meu_dataset.csv` e `data/clean/meu_dataset.csv` a partir do pipeline de tratamento do meu notebook de EDA (ITBI Recife), seguindo o padrão de `notebooks/eda-com-downloads.ipynb` do professor (raw = concat bruto dos 9 CSVs; clean = estado final do `df` tratado).
  - Rascunho e widgets do Dashboard 1 (sidebar com filtros + Distribuição/Correlação em Altair).
  - Sincronização do repositório com as atualizações da professora (`ALTAIR-CROSSFILTER.md`, seção `entregas/` e link pro `ROTEIRO.md` no `README.md`).
  - Tratamento dos casos de borda do Dashboard 1 (0/1/2+ variáveis selecionadas, filtros que zeram os dados).
  - Identidade visual terracota em `.streamlit/config.toml` (tema ligado ao assunto do dataset — imóveis).
  - Planejamento das 4 métricas do Dashboard 2 (contagem, valor mediano de avaliação, valor mediano por m², % Residencial) com a justificativa completa.
  - Estrutura em abas (`st.tabs`) e implementação do Dashboard 2 com seleção cruzada em Altair (clicar numa barra do gráfico de anos destaca os KPIs).
- **Modificado:**
  - O primeiro rascunho do Dashboard 1 veio com a sidebar à direita; pedi para mover de volta para a esquerda, mantendo os dois blocos de conteúdo (Distribuição/Correlação) empilhados — layout diferente do exemplo da professora, que é lado a lado.
- **Rejeitado:**
  - Nenhuma entrega foi descartada por completo;
