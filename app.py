import pandas as pd
import streamlit as st

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Simulador de Custos e Orçamento",
    page_icon="💰",
    layout="wide",
)

st.title("💰 Simulador de Custos e Orçamento")
st.caption(
    "Ferramenta interativa para gestão orçamentária e controle de despesas."
)


# ==========================================
# 2. BASE DE DADOS INTERNA
# ==========================================
@st.cache_data
def carregar_dados():
    dados = [
        {
            "Item": "Insumos Plásticos",
            "Categoria": "Matéria-Prima",
            "Valor (R$)": 4500.00,
            "Prioridade": "Alta",
        },
        {
            "Item": "Componentes Eletrônicos",
            "Categoria": "Matéria-Prima",
            "Valor (R$)": 3200.00,
            "Prioridade": "Alta",
        },
        {
            "Item": "Equipe de Montagem",
            "Categoria": "Mão de Obra",
            "Valor (R$)": 6000.00,
            "Prioridade": "Alta",
        },
        {
            "Item": "Consultoria Técnica",
            "Categoria": "Mão de Obra",
            "Valor (R$)": 2500.00,
            "Prioridade": "Média",
        },
        {
            "Item": "Frete de Entrega",
            "Categoria": "Logística",
            "Valor (R$)": 1800.00,
            "Prioridade": "Média",
        },
        {
            "Item": "Armazenamento Local",
            "Categoria": "Logística",
            "Valor (R$)": 1200.00,
            "Prioridade": "Baixa",
        },
        {
            "Item": "Conta de Energia Elétrica",
            "Categoria": "Energia",
            "Valor (R$)": 1100.00,
            "Prioridade": "Alta",
        },
        {
            "Item": "Licenças de Software",
            "Categoria": "Ferramentas",
            "Valor (R$)": 950.00,
            "Prioridade": "Média",
        },
        {
            "Item": "Manutenção de Máquinas",
            "Categoria": "Ferramentas",
            "Valor (R$)": 2100.00,
            "Prioridade": "Alta",
        },
        {
            "Item": "Embalagens",
            "Categoria": "Matéria-Prima",
            "Valor (R$)": 800.00,
            "Prioridade": "Baixa",
        },
    ]
    return pd.DataFrame(dados)


df_base = carregar_dados()

# ==========================================
# 3. BARRA LATERAL (SIDEBAR) - FILTROS
# ==========================================
st.sidebar.header("⚙️ Configurações de Filtro")

orcamento_total = st.sidebar.slider(
    label="Orçamento Total Disponível (R$)",
    min_value=5000,
    max_value=50000,
    value=20000,
    step=500,
    format="R$ %d",
)

categorias_disponiveis = df_base["Categoria"].unique().tolist()

categorias_selecionadas = st.sidebar.multiselect(
    label="Selecione as Categorias:",
    options=categorias_disponiveis,
    default=categorias_disponiveis,
)

# ==========================================
# 4. PROCESSAMENTO E FILTRAGEM DOS DADOS
# ==========================================
if categorias_selecionadas:
    df_filtrado = df_base[df_base["Categoria"].isin(categorias_selecionadas)]
else:
    df_filtrado = pd.DataFrame(columns=df_base.columns)

gasto_total = df_filtrado["Valor (R$)"].sum()
saldo = orcamento_total - gasto_total

# ==========================================
# 5. PAINEL DE MÉTRICAS & ALERTAS DInÂMICOS
# ==========================================
col1, col2, col3 = st.columns(3)

col1.metric(
    label="Orçamento Definido",
    value=f"R$ {orcamento_total:,.2f}".replace(",", "X")
    .replace(".", ",")
    .replace("X", "."),
)

col2.metric(
    label="Gasto Filtrado",
    value=f"R$ {gasto_total:,.2f}".replace(",", "X")
    .replace(".", ",")
    .replace("X", "."),
)

col3.metric(
    label="Saldo Restante",
    value=f"R$ {saldo:,.2f}".replace(",", "X")
    .replace(".", ",")
    .replace("X", "."),
    delta=f"R$ {saldo:,.2f}".replace(",", "X")
    .replace(".", ",")
    .replace("X", "."),
)

st.divider()

if saldo >= 0:
    st.success(
        f"✅ **Projeto dentro da meta!** Você ainda possui R$ {saldo:,.2f} disponíveis para alocação.".replace(
            ",", "X"
        )
        .replace(".", ",")
        .replace("X", ".")
    )
else:
    excedente = abs(saldo)
    st.error(
        f"🚨 **Atenção: Orçamento Excedido!** Os custos selecionados ultrapassam o limite em R$ {excedente:,.2f}.".replace(
            ",", "X"
        )
        .replace(".", ",")
        .replace("X", ".")
    )

# ==========================================
# 6. GRÁFICO E TABELA DE DADOS
# ==========================================
st.subheader("📊 Distribuição de Gastos por Categoria")

if not df_filtrado.empty:
    gastos_por_categoria = (
        df_filtrado.groupby("Categoria")["Valor (R$)"]
        .sum()
        .reset_index()
        .sort_values(by="Valor (R$)", ascending=True)
    )

    # Exibição leve utilizando gráfico nativo do Streamlit
    st.bar_chart(
        data=gastos_por_categoria,
        x="Categoria",
        y="Valor (R$)",
        horizontal=True,
    )
else:
    st.info("Nenhuma categoria selecionada para exibir o gráfico.")

st.subheader("📋 Detalhamento dos Itens Filtrados")

if not df_filtrado.empty:
    st.dataframe(
        df_filtrado,
        use_container_width=True,
        hide_index=True,
    )
else:
    st.warning("Selecione ao menos uma categoria na barra lateral.")
