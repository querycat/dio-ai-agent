# Planejamento

## ETAPA 1

### Documentação do agente

- **Caso de uso (para que o agente serve, que problemas ele pode resolver):** __Ex:__ consultoria de investimentos, planejamento de metas, alertas de gastos.
- **Persona e tom de voz (personalidade do agente):**
- **Arquitetura:** Fluxo de dados e integração com a base de conhecimento. __Ex:__ Diagrama mostrando o fluxo de um usuário perguntando e o agente, consultando a base de conhecimento, validando e por fim respondendo.
- **Segurança e anti-alucinação:** Esse ponto é muito crítico no setor financeiro. O agente precisa responder apenas com os dados fornecidos. Quando algo que ele não sabe for perguntado, ele não pode inventar nada, e sim admitir que não sabe.

## ETAPA 2

### Base de conhecimento

Base de conhecimento
A base de conhecimento é a fonte de dados que o agente utilizará.

A base do Equilibra contém os seguintes arquivos:

`produtos_financeiros.json`
Lista os tipos de investimentos disponíveis, contém uma explicação sobre o investimento, nível de risco, liquidez, perfil indicado e objetivos comuns.

`perfil_investidor.json`
Dados fictícios de um investidor. Esse arquivo ajuda a personalizar as explicações e necessidades de aprendizado do usuário.

`transacoes.csv`
Dados fictícios de transações financeiras do usuário. Ajuda a analisar os padrões de gastos do usuário.


#### Como esses dados são carregados?

Os dados utilizados pelo agente são armazenados em arquivos locais dentro da pasta data/. Cada arquivo possui um formato adequado ao tipo de informação que contém.

Durante a inicialização, esses arquivos são carregados para a memória da aplicação e ficam disponíveis para que o agente possa analisar a situação financeira do usuário e utilizar a base de conhecimento para fornecer orientações contextualizadas.


```python

import panda as pd
import json

# CARREGAR DADOS
perfil = json.load(open('.data/perfil_investidor.json'))
produtos = json.load(open('.data/produtos_financeiros'))
transacoes = pd.read_csv('./data/transacoes.csv')

```

## ETAPA 3

### Prompts do Agente

Documenta os prompts que definem o comportamento do agente:

- **System Prompt**: Instruções gerais de comportamento e restrições.
- **Exemplos de Interação**: Cenários de uso com entrada e saída esperada.
- **Tratamento de Edge Cases**: Como o agente lida com situações limite.

Para mais detalhes sobre essas etapa, veja o seguinte arquivo: [prompts](https://github.com/querycat/dio-ai-agent/blob/main/docs/02-prompts.md)

## ETAPA 4

### Aplicação funcional

O código implementa a estrutura principal do **Equilibra**, integrando o carregamento dos dados financeiros do usuário, a base de conhecimento sobre investimentos, o modelo de linguagem executado localmente pelo Ollama e uma interface de chat desenvolvida com Streamlit.

#### Bibliotecas utilizadas
**pandas**: biblioteca utilizada para manipulação e análise de dados em formato tabular. No projeto, é utilizada para carregar o arquivo `transacoes.csv` e permitir que as transações financeiras sejam organizadas e apresentadas ao modelo.
**json**: biblioteca nativa do Python utilizada para trabalhar com arquivos no formato JSON. É utilizada para carregar o perfil do investidor e a base de produtos financeiros.
**requests**: biblioteca utilizada para realizar requisições HTTP. No projeto, é responsável por enviar as informações e a pergunta do usuário para a API do Ollama, que executa o modelo de linguagem localmente.
**streamlit**: framework Python utilizado para criar interfaces web de forma simplificada. É responsável pela interface de chat do Equilibra, permitindo que o usuário envie perguntas e visualize as respostas do agente.
Configuração

A variável OLLAMA_URL define o endereço da API local utilizada para comunicação com o Ollama. Já MODELO especifica qual modelo de linguagem será utilizado pelo agente.

#### Carregamento dos dados

Na etapa seguinte, o código carrega três fontes de informação:

**Perfil do investidor** — contém informações como nome, idade, perfil de investidor, objetivo financeiro, patrimônio e reserva de emergência.
**Produtos financeiros** — contém a base de conhecimento utilizada pelo agente para explicar os diferentes tipos de investimentos.
**Transações** — contém os registros financeiros do usuário, carregados como um DataFrame do pandas.

Esses dados são posteriormente reunidos para formar o contexto utilizado pelo modelo.

#### Construção do contexto

A variável contexto organiza as informações carregadas em um único texto. Dessa forma, o modelo recebe não apenas a pergunta do usuário, mas também informações relevantes sobre sua situação financeira e a base de produtos financeiros disponível.

As transações são convertidas para uma representação em texto utilizando to_string(), enquanto os dados dos produtos são convertidos novamente para JSON utilizando json.dumps(). Isso permite inserir essas informações no prompt enviado ao modelo.

#### System Prompt

O SYSTEM_PROMPT define o comportamento esperado do Equilibra. Ele estabelece sua função como educador financeiro, além de determinar regras como:

- explicar conceitos de finanças pessoais de maneira simples;
- utilizar os dados fornecidos para criar exemplos contextualizados;
- não recomendar investimentos específicos;
- admitir quando não possuir determinada informação;
- manter as respostas dentro do tema de educação financeira;
- verificar se o usuário compreendeu a explicação.

Esse prompt funciona como uma camada de orientação para manter as respostas do modelo alinhadas à proposta do agente.

#### Comunicação com o Ollama

A função perguntar() é responsável por construir o prompt final e enviá-lo ao modelo de linguagem.

**Ela combina:**

System Prompt + contexto financeiro do usuário + pergunta do usuário

Em seguida, `requests.post()` realiza uma requisição HTTP para a API do Ollama. O parâmetro `stream: False` indica que a resposta será recebida de uma única vez, em vez de ser transmitida gradualmente.

Após receber a resposta, `r.json()['response']` extrai o texto gerado pelo modelo.

#### Interface do usuário

Por fim, o Streamlit cria a interface de chat do Equilibra.

`st.title()` define o título da aplicação, enquanto `st.chat_input()` disponibiliza o campo para o usuário enviar sua dúvida. Quando uma pergunta é enviada, ela é exibida na interface e a função `perguntar()` é chamada para gerar a resposta.

Durante o processamento, `st.spinner()` apresenta um indicador visual de carregamento. A resposta gerada pelo modelo é então exibida utilizando `st.chat_message("assistant")`.

#### Fluxo geral

De forma simplificada, o funcionamento pode ser representado assim:

Dados do usuário → Construção do contexto → System Prompt → Pergunta do usuário → Ollama → Resposta → Streamlit

Assim, o código integra dados estruturados, regras de comportamento, modelo de linguagem e interface de usuário em um único fluxo, formando a aplicação funcional do Equilibra.

## ETAPA 5 

### Avaliação de métricas

## ETAPA 6

### Pitch

