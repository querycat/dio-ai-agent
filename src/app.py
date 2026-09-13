import pandas as pd
import json
import requests
import streamlit as st

# CONFIGURAÇÃO
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "gpt=oss"

# CARREGAR DADOS
perfil = json.load(open('.data/perfil_investidor.json'))
produtos = json.load(open('.data/produtos_financeiros'))
transacoes = pd.read_csv('./data/transacoes.csv')

# CONTEXTO
contexto = f"""
CLIENTE: {perfil['nome']}, {perfil['idade']}, anos, perfil {perfil['perfil_investidor']}
OBJETIVO: {perfil['objetivo_principal']}
PATRIMÔNIO: R$ {perfil['patrimonio_total']} | RESERVA: R$ {perfil['reserva_emergencia_atual']}

TRANSAÇÕES RECENTES:
{transacoes.to_string(index=False)}

PRODUTOS DISPONÍVEIS:
{json.dumps(produtos, indent=2, ensure_ascii=False)}
"""

# SYSTEM PROMPT
SYSTEM_PROMPT = """
Você é o Equilibra, um educador financeiro didático e direto ao ponto.

OBJETIVO:
Ensinar conceitos de finanças pessoais de forma simples.

REGRAS
1. NUNCA recomende investimentos específicos - apenas explique como funcionam;
2. Use os dados fornecidos para dar exemplos personalizados;
3. Use linguagem simples;
4. Se não souber algo, admita: "Não tenho essa informação";
5. Sempre pergunte se o usuário entendeu;
6. JAMAIS responda a perguntas fora do tema ensino de finanças pessoais. Quando ocorrer, responda lembrando o seu papel de educador financeiro.
"""

# CHAMAR OLLAMA
def perguntar(msg):
    prompt = f"""
    {SYSTEM_PROMPT}

    CONTEXTO DO USUÁRIO:
    {contexto}

    Pergunta: {msg}"""

    r = requests.post(OLLAMA_URL, json={"model": MODELO, "prompt": prompt, "stream": False})
    return r.json()['response']

# INTERFACE
st.title("Equilibra")

if pergunta := st.chat_input("Sua dúvida sobre finanças..."):
    st.chat_message("user").write(pergunta)
    with st.spinner("..."):
        st.chat_message("assistant").write(perguntar(pergunta))