import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns

st.header('Pós Graduação em Inteligência Artificial para Ciência de Dados - Prof. Clovis Reis', divider='rainbow')


# funções são definidas para realizar cálculos específicos nos dados:
def somar_valores(df):
    soma_resultado = df['Valor'].sum()
    return f"{soma_resultado:,.2f}"

def qtd_notas_municipio(df):
    resultado_contar_por_municipio = df.groupby(['Município'])['Nota Fiscal'].count()
    return resultado_contar_por_municipio

def somar_por_municipio(df):
    resultado_somar_municipios = df.groupby(['Município'])['Valor'].sum()
    return resultado_somar_municipios

#Lê os dados da planilha
arquivo_excel = 'Movimentações.xlsx'
df_mov = pd.read_excel(arquivo_excel, sheet_name='Pagamentos')

# Contar registros sem data de pagamento
registros_sem_data_pagamento = df_mov['Data Pagamento'].isnull().sum()

# Calcular os valores
chamar_soma_valores = somar_valores(df_mov)
resultado_notas_por_municipio = qtd_notas_municipio(df_mov)
chamar_valores_por_municipio = somar_por_municipio(df_mov)

st.markdown("<h1 style='font-size: 24px;'>Análise de Movimentações Financeiras</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='font-size: 24px;'>Amostra dos dados</h1>", unsafe_allow_html=True)
st.dataframe(df_mov.head())
st.metric(label="Soma de todas as notas fiscais", value=chamar_soma_valores)

if registros_sem_data_pagamento > 0:
    st.warning(f"Existem {registros_sem_data_pagamento} registros sem data de pagamento.")
else:
    st.success("Todos os registros têm data de pagamento.")

pagamentos_em_atraso = (df_mov['Data Pagamento'] > df_mov['Data Vencimento']).sum()
st.write("### Pagamentos em Atraso")

if pagamentos_em_atraso > 0:
    st.warning(f"Foram feitos {pagamentos_em_atraso} pagamentos em atraso.")
else:
    st.success("Todos os pagamentos foram feitos dentro do prazo.")
    
# Média
media_valor = df_mov['Valor'].mean()
st.write(f"A média dos valores é: {media_valor:.2f}") 

# Desvio padrão 
desvio_padrao = df_mov['Valor'].std()
st.write(f"O desvio padrão é: {desvio_padrao:.2f}") 

# Mediana 
mediana_valor = df_mov['Valor'].median()
st.write(f"A mediana é: {media_valor:.2f}") 

# Coeficiente de variação 
coeficiente_variacao = (desvio_padrao / media_valor) * 100
coeficiente_variacao_formatado = f"{coeficiente_variacao:.2f}%"
st.write(f"O coeficiente de variação dos valores é: {coeficiente_variacao_formatado}")

registros_em_branco_por_coluna = df_mov.isnull().sum()

if registros_em_branco_por_coluna.any():
    st.warning("Existem registros em branco em algumas colunas:")
    st.write(registros_em_branco_por_coluna)
else:
    st.success("Não há registros em branco em nenhuma coluna.")

st.write("### Gráfico de somas de valores por município")
fig, ax = plt.subplots()
chamar_valores_por_municipio.plot(kind='bar', ax=ax)

for container in ax.containers:
    ax.bar_label(container, labels=[f'{int(label):,}'.replace(',', '.') for label in container.datavalues])

plt.xticks(rotation=45)
plt.xlabel('Município')
plt.ylabel('Soma dos Valores')
plt.title('Soma dos Valores por Município')
st.pyplot(fig)

st.write("### Quantidade de Pessoa Física e Jurídica")
pessoas = df_mov['Tipo Pessoa'].value_counts()
fig2, ax2 = plt.subplots()
ax2.pie(pessoas, labels=pessoas.index, autopct='%1.1f%%', startangle=120, colors=['#ff9999','#66b3ff'])
ax2.axis('equal') 
plt.title('Quantidade de Pessoa Física e Jurídica')
st.pyplot(fig2)

st.write("### Quantidade de Notas Fiscais por Município")
fig, ax = plt.subplots(figsize=(10, 8))
sns.barplot(x=resultado_notas_por_municipio.values, y=resultado_notas_por_municipio.index, palette='viridis', ax=ax)
ax.set_xlabel('Quantidade de Notas Fiscais')
ax.set_ylabel('Município')
ax.set_title('Quantidade de Notas Fiscais por Município')

for i, v in enumerate(resultado_notas_por_municipio.values):
    ax.text(v + 0.2, i, str(v), color='black', va='center')

st.pyplot(fig)