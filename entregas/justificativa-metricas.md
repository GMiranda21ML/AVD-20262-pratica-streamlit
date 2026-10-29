# Justificativa das métricas — Dashboard 2

Dataset: ITBI Recife (2015-2023), transações de transmissão de imóveis. Os KPIs abaixo usam
`data/clean/meu_dataset.csv` e respondem aos filtros de **período** (intervalo de anos, coluna
`ano`) e **tipo de ocupação** (`tipo_ocupa_bin`: Residencial/Comercial) do Dashboard 2.

## Métrica 1: Total de transações
- **Variável:** contagem de linhas (uma linha = uma transação de ITBI)
- **O que mede:** o volume de transações de ITBI dentro do período e do tipo de ocupação selecionados
- **Por que foi escolhida:** é o indicador mais direto de atividade do mercado imobiliário — toda
  análise de valor só faz sentido com o volume por trás
- **Público-alvo:** gestores da Prefeitura do Recife (planejamento fiscal e urbano) e imprensa/público
  interessado no mercado imobiliário local
- **Qual decisão pode ser apoiada por essa métrica?** priorizar fiscalização ou investimento em
  infraestrutura nos bairros/anos com maior volume de transações
- **O que comunica ao público-alvo:** "quantos imóveis mudaram de dono nesse recorte de tempo/tipo"

## Métrica 2: Valor médio de avaliação
- **Variável:** `valor_avaliacao` (mediana, não a média — a distribuição é extremamente assimétrica,
  como vimos na EDA)
- **O que mede:** o valor típico de avaliação dos imóveis transacionados no filtro selecionado
- **Por que foi escolhida:** é a base de cálculo do próprio ITBI; resume em um número só "quanto
  valem" os imóveis sendo negociados
- **Público-alvo:** gestores da Prefeitura (estimativa de arrecadação) e público geral
- **Qual decisão pode ser apoiada por essa métrica?** comparar o patamar de valor entre períodos ou
  entre Residencial/Comercial, para calibrar expectativa de arrecadação
- **O que comunica ao público-alvo:** "quanto vale, em média, um imóvel transacionado aqui", sem
  precisar interpretar um histograma

## Métrica 3: Valor médio por m² construído
- **Variável:** `valor_avaliacao / area_construida` (mediana; linhas com `area_construida <= 0` são
  excluídas do cálculo, pra não distorcer com divisão por valores perto de zero)
- **O que mede:** o preço típico por metro quadrado construído
- **Por que foi escolhida:** normaliza o valor pelo tamanho do imóvel — métrica padrão do mercado
  imobiliário para comparar imóveis de tamanhos muito diferentes
- **Público-alvo:** compradores/investidores e gestores públicos
- **Qual decisão pode ser apoiada por essa métrica?** identificar se uma região/tipo de imóvel está
  caro ou barato em termos comparáveis, independente do tamanho do imóvel
- **O que comunica ao público-alvo:** "quanto custa, em média, o metro quadrado construído" nesse
  recorte

## Métrica 4: Proporção Residencial x Comercial
- **Variável:** `tipo_ocupa_bin`
- **O que mede:** a porcentagem das transações do filtro que são Residenciais (o complemento é
  Comercial)
- **Por que foi escolhida:** simplifica a variável categórica mais relevante do dataset (já usada na
  distinção de cor do Dashboard 1) em um número único
- **Público-alvo:** planejamento urbano/zoneamento e investidores
- **Qual decisão pode ser apoiada por essa métrica?** entender se um período ou região está se
  tornando mais residencial ou mais comercial, relevante para política de zoneamento
- **O que comunica ao público-alvo:** "de cada 10 imóveis negociados nesse recorte, quantos são
  residenciais"
