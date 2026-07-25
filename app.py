import streamlit as st
import pandas as pd
import io
import hashlib
from PIL import Image

# Configuração da página
st.set_page_config(page_title="Conciliador Shopee PRO", page_icon="👑", layout="wide")

# ----------------------------------------
# SISTEMA DE LICENCIAMENTO COM BLINDAGEM CRIPTOGRÁFICA
# ----------------------------------------
CHAVE_MESTRA_VALIDA = "REI-SHOPEE-2026-PRO"
SEGREDO_CRIPTO = "O-REI-DO-ECOMMERCE-2026-SEGREDO-ABSOLUTO"

def gerar_assinatura(valor):
    """Gera um selo criptográfico impossível de ser forjado sem o segredo"""
    dados = f"{valor}-{SEGREDO_CRIPTO}"
    return hashlib.sha256(dados.encode()).hexdigest()[:10]

# Lê o contador e a assinatura direto da URL do navegador
params = st.query_params
try:
    tentativas_atuais = int(params.get("uso", 0))
    assinatura_recebida = params.get("hash", "")
    
    # Valida se a assinatura confere com o número de usos (Anti-Fraude)
    assinatura_esperada = gerar_assinatura(tentativas_atuais)
    if assinatura_recebida != assinatura_esperada and tentativas_atuais > 0:
        # Se alterou a URL na maldade, força o bloqueio imediato
        tentativas_atuais = 999 
except ValueError:
    tentativas_atuais = 999

if 'form_id' not in st.session_state:
    st.session_state['form_id'] = 0

# ----------------------------------------
# BLINDAGEM VISUAL (CÓDIGO CSS PROFISSIONAL)
# ----------------------------------------
st.markdown("""
    <style>
    [data-testid="stElementToolbar"] {
        display: none !important;
    }
    .stButton button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# ----------------------------------------
# BARRA LATERAL (DESIGN COMERCIAL LIMPO)
# ----------------------------------------
with st.sidebar:
    try:
        logo = Image.open("O FILHO DO REI.png")
        st.image(logo, use_container_width=True)
    except FileNotFoundError:
        st.warning("⚠️ Imagem não encontrada ('O FILHO DO REI.png').")
    
    st.markdown("### Desenvolvido por:")
    st.markdown("👑 **O Filho do Rei**")
    st.divider()
    
    st.markdown("### 🔑 Ativação da Licença")
    licenca_inserida = st.text_input("Digite sua Chave PRO:", type="password")
    
    st.divider()
    st.markdown("### 🛒 Licença Comercial PRO")
    st.markdown("🔥 **Promoção Exclusiva:**")
    st.markdown("## **R$ 49,90**")
    st.write("Tenha acesso definitivo, ilimitado e elimine os furos de repasse.")
    
    link_whatsapp = "https://wa.me/5511916476903?text=Olá,%20quero%20adquirir%20a%20chave%20de%20ativação%20do%20Conciliador%20Shopee%20PRO%20por%20R$%2049,90!"
    st.link_button("💬 Comprar por R$ 49,90", link_whatsapp, type="primary")
    
    st.divider()
    st.caption("Licença Comercial - Versão 5.6 PRO")

# Validação se a licença informada é a válida
sistema_liberado = False
if licenca_inserida == CHAVE_MESTRA_VALIDA:
    sistema_liberado = True
    st.sidebar.success("✅ Licença PRO Ativada (Ilimitado)!")
else:
    if licenca_inserida != "":
        st.sidebar.error("❌ Chave inválida.")

# ----------------------------------------
# CABEÇALHO PRINCIPAL
# ----------------------------------------
st.title("🚨 Auditoria e Conciliação Shopee")
st.markdown("Sistema automatizado de auditoria para cruzamento de dados, cálculo exato de taxas por unidade e blindagem de caixa.")

# Botão de Nova Conciliação
col_btn1, col_btn2 = st.columns([1, 3])
with col_btn1:
    if st.button("🔄 Nova Conciliação"):
        for key in list(st.session_state.keys()):
            if key != 'form_id':
                del st.session_state[key]
        st.session_state['form_id'] += 1
        st.rerun()

st.divider()

# VERIFICAÇÃO DO LIMITE DE TRIAL (TRAVA APÓS 2 USOS COMPLETOS)
if not sistema_liberado and tentativas_atuais >= 2:
    st.warning("🔒 **VOCÊ ATINGIU O LIMITE DE TESTES GRATUITOS (2 CONCILIAÇÕES)**")
    st.info("Para continuar auditando sua operação de forma ilimitada, adquire a sua licença definitiva por apenas **R$ 49,90** clicando no botão do WhatsApp na barra lateral ou digite sua chave PRO válida para liberar o acesso instantaneamente.")
    st.stop()

if not sistema_liberado:
    chances_restantes = 2 - tentativas_atuais
    st.info(f"💡 **Modo Demonstração Ativo:** Você tem **{chances_restantes} conciliação(ões) gratuita(s)** de teste antes do bloqueio comercial.")

# ========================================
# FLUXO DE UPLOAD E PROCESSAMENTO
# ========================================
fid = st.session_state['form_id']

col1, col2 = st.columns(2)
with col1:
    st.markdown("#### 1. Vendas do Período")
    file_pedidos = st.file_uploader("📂 Relatório de Pedidos", type=["xlsx"], key=f"up_pedidos_{fid}")

with col2:
    st.markdown("#### 2. Recebimentos")
    file_repasses_1 = st.file_uploader("💰 Renda (Mês da Venda)", type=["xlsx"], key=f"up_rep_1_{fid}")
    file_repasses_2 = st.file_uploader("💰 Renda (Mês Seguinte - Opcional)", type=["xlsx"], key=f"up_rep_2_{fid}")
    file_repasses_3 = st.file_uploader("💰 Renda (Mês Retrasado - Opcional)", type=["xlsx"], key=f"up_rep_3_{fid}")

arquivos_repasses = [f for f in [file_repasses_1, file_repasses_2, file_repasses_3] if f is not None]

def calcular_taxa_unidade(preco_unitario):
    if preco_unitario < 80:
        return (preco_unitario * 0.20) + 4
    elif preco_unitario < 100:
        return (preco_unitario * 0.14) + 16
    elif preco_unitario < 200:
        return (preco_unitario * 0.14) + 20
    else:
        return (preco_unitario * 0.14) + 26

def limpar_moeda(coluna):
    if coluna.dtype == object:
        coluna = coluna.astype(str).str.replace('R$', '', regex=False).str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
    return pd.to_numeric(coluna, errors='coerce').fillna(0)

# Motor de Processamento
if file_pedidos and len(arquivos_repasses) > 0:
    if st.button("🚀 Processar Conciliação", type="primary"):
        with st.spinner("Consolidando bases financeiras, abatendo devoluções e auditando transações..."):
            try:
                # PROCESSAR PEDIDOS
                df_pedidos = pd.read_excel(file_pedidos)
                
                if 'Status da Devolução / Reembolso' not in df_pedidos.columns:
                    df_pedidos['Status da Devolução / Reembolso'] = ''

                df_pedidos['Quantidade'] = pd.to_numeric(df_pedidos['Quantidade'], errors='coerce').fillna(1)
                df_pedidos['Subtotal do produto'] = limpar_moeda(df_pedidos['Subtotal do produto'])
                
                df_pedidos['Preco_Unitario'] = df_pedidos['Subtotal do produto'] / df_pedidos['Quantidade']
                df_pedidos['Taxa_Unidade'] = df_pedidos['Preco_Unitario'].apply(calcular_taxa_unidade)
                df_pedidos['Liquido_Linha'] = df_pedidos['Subtotal do produto'] - (df_pedidos['Taxa_Unidade'] * df_pedidos['Quantidade'])

                df_agrupado = df_pedidos.groupby('ID do pedido').agg(
                    Status=('Status do pedido', 'first'),
                    Status_Reembolso=('Status da Devolução / Reembolso', 'first'),
                    Data=('Data de criação do pedido', 'first'),
                    Logistica=('Opção de envio', 'first'),
                    Valor_Total_Venda=('Subtotal do produto', 'sum'),
                    Liquido_Calculado=('Liquido_Linha', 'sum')
                ).reset_index()

                df_agrupado['Liquido_Calculado'] = df_agrupado.apply(
                    lambda row: row['Liquido_Calculado'] + 8 if isinstance(row['Logistica'], str) and 'entrega direta' in row['Logistica'].lower() else row['Liquido_Calculado'], 
                    axis=1
                )

                # PROCESSAR REPASSES
                list_df_repasses = []
                for arquivo in arquivos_repasses:
                    df_temp = pd.read_excel(arquivo, sheet_name='Renda', header=2)
                    df_temp = df_temp[df_temp['Ver'] == 'Order']
                    list_df_repasses.append(df_temp)
                
                df_repasses_total = pd.concat(list_df_repasses, ignore_index=True)
                df_repasses_total['Quantia total lançada (R$)'] = limpar_moeda(df_repasses_total['Quantia total lançada (R$)'])
                
                col_afiliado = 'Taxa de comissão Afiliados do Vendedor'
                if col_afiliado in df_repasses_total.columns:
                    df_repasses_total['Taxa_Afiliado'] = limpar_moeda(df_repasses_total[col_afiliado])
                else:
                    df_repasses_total['Taxa_Afiliado'] = 0

                df_rep_agrupado = df_repasses_total.groupby('ID do pedido').agg(
                    Repasse_Realizado=('Quantia total lançada (R$)', 'sum'),
                    Taxa_Afiliado=('Taxa_Afiliado', 'sum')
                ).reset_index()

                # CRUZAMENTO FINAL
                df_final = pd.merge(df_agrupado, df_rep_agrupado, on='ID do pedido', how='left')
                df_final['Repasse_Realizado'] = df_final['Repasse_Realizado'].fillna(0)
                df_final['Taxa_Afiliado'] = df_final['Taxa_Afiliado'].fillna(0)
                
                df_final['Liquido_Calculado'] = df_final['Liquido_Calculado'] - df_final['Taxa_Afiliado'].abs()
                df_final['Diferenca'] = df_final['Repasse_Realizado'] - df_final['Liquido_Calculado']

                def is_returned_or_cancelled(row):
                    status_str = str(row['Status']).lower()
                    reembolso_str = str(row['Status_Reembolso']).strip().lower()
                    if 'cancelado' in status_str or 'devolvido' in status_str: return True
                    if reembolso_str and reembolso_str != 'nan': return True
                    return False

                def status_financeiro(row):
                    if is_returned_or_cancelled(row): return 'Cancelado/Devolvido'
                    if row['Repasse_Realizado'] > 0: return 'Pago'
                    return 'Pendente'

                def auditoria(row):
                    if is_returned_or_cancelled(row): return '-'
                    if row['Repasse_Realizado'] == 0: return 'Ainda não recebido'
                    if abs(row['Diferenca']) <= 0.10: return 'Bateu Perfeito'
                    return 'Divergente'

                df_final['Status Financeiro'] = df_final.apply(status_financeiro, axis=1)
                df_final['Auditoria'] = df_final.apply(auditoria, axis=1)
                df_final.drop(columns=['Status_Reembolso'], errors='ignore', inplace=True)

                df_final = df_final.sort_values(
                    by=['Auditoria', 'Diferenca'], 
                    ascending=[False, True], 
                    key=lambda x: x.map({'Divergente': 1, 'Bateu Perfeito': 2, 'Ainda não recebido': 3, '-': 4})
                )

                if not sistema_liberado:
                    novo_uso = tentativas_atuais + 1
                    # Grava o novo uso junto com a assinatura criptografada na URL
                    st.query_params["uso"] = novo_uso
                    st.query_params["hash"] = gerar_assinatura(novo_uso)

                st.session_state['df_resultado'] = df_final
                st.success("✅ Auditoria finalizada com precisão.")
                st.rerun()

            except Exception as e:
                st.error(f"Erro ao processar. Verifique o formato das planilhas. Detalhe técnico: {e}")

if 'df_resultado' in st.session_state:
    df_final = st.session_state['df_resultado']
    
    st.divider()
    
    col_busca, col_filtro = st.columns([2, 1])
    with col_busca:
        busca_id = st.text_input("🔍 Buscar por ID do Pedido:", placeholder="Cole o ID aqui para filtrar...")
    with col_filtro:
        opcoes = ['Todos', 'Divergente', 'Bateu Perfeito', 'Ainda não recebido', '- (Cancelados)']
        filtro_selecionado = st.selectbox("📌 Filtrar por Status de Auditoria:", opcoes)
    
    df_exibicao = df_final.copy()
    
    if busca_id:
        df_exibicao = df_exibicao[df_exibicao['ID do pedido'].astype(str).str.contains(busca_id, case=False, na=False)]
    
    if filtro_selecionado != 'Todos':
        if filtro_selecionado == '- (Cancelados)':
            df_exibicao = df_exibicao[df_exibicao['Auditoria'] == '-']
        else:
            df_exibicao = df_exibicao[df_exibicao['Auditoria'] == filtro_selecionado]

    st.markdown("### 📊 Visão Geral da Operação")
    
    col_metrica, col_grafico = st.columns([1, 2])
    
    with col_metrica:
        divergentes = df_exibicao[df_exibicao['Auditoria'] == 'Divergente']
        st.metric(
            label="🚨 Divergências Financeiras (Furos)", 
            value=f"{len(divergentes)} pedidos", 
            delta=f"R$ {divergentes['Diferenca'].sum():.2f}",
            delta_color="inverse"
        )
        
        perfeitos = df_exibicao[df_exibicao['Auditoria'] == 'Bateu Perfeito']
        st.metric(label="✅ Pagamentos Corretos", value=f"{len(perfeitos)} pedidos")

    with col_grafico:
        contagem_status = df_exibicao['Auditoria'].value_counts().reset_index()
        contagem_status.columns = ['Status da Auditoria', 'Quantidade de Pedidos']
        st.bar_chart(data=contagem_status, x='Status da Auditoria', y='Quantidade de Pedidos', color="#D4AF37", use_container_width=True)

    def color_auditoria(val):
        if val == 'Divergente': return 'color: white; background-color: #8B0000; font-weight: bold;'
        if val == 'Bateu Perfeito': return 'color: green;'
        if val == 'Ainda não recebido': return 'color: #D2691E;'
        return ''

    st.dataframe(
        df_exibicao.style.map(color_auditoria, subset=['Auditoria']).format({
            'Valor_Total_Venda': 'R$ {:.2f}',
            'Liquido_Calculado': 'R$ {:.2f}',
            'Repasse_Realizado': 'R$ {:.2f}',
            'Taxa_Afiliado': 'R$ {:.2f}',
            'Diferenca': 'R$ {:.2f}'
        }), 
        use_container_width=True
    )

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_final.to_excel(writer, index=False, sheet_name='Auditoria_Blindada')
    
    st.download_button(
        label="📥 Baixar Relatório Completo (Excel)",
        data=output.getvalue(),
        file_name="Auditoria_Resultados.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
