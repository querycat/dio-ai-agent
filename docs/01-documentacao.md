# Documentação do Agente

## Caso de Uso

### Problema

Várias pessoas têm dificuldade para organizar a própria vida financeira, principalmente por falta de conhecimento sobre planejamento financeiro, controle de gastos, reserva de emergência e investimentos.

O agente busca solucionar esse problema oferecendo educação financeira personalizada, ajudando o usuário a compreender sua situação financeira, organizar receitas e despesas, estabelecer objetivos e aprender conceitos básicos de investimentos de acordo com seu perfil e momento financeiro.

### Solução

O agente atua como um educador financeiro virtual, conduzindo o usuário de forma gradual na organização de suas finanças.

A partir das informações fornecidas pelo usuário, ele pode:

- Auxiliar no levantamento e categorização de receitas e despesas;
- Identificar hábitos de consumo e possíveis pontos de atenção;
- Ajudar a criar um orçamento mensal;
- Orientar na definição de metas financeiras;
- Explicar a importância e o planejamento de uma reserva de emergência;
- Ensinar conceitos básicos sobre renda fixa, renda variável e outros tipos de investimentos;
- Explicar conceitos financeiros de forma simples e acessível;
- Apresentar exemplos e simulações para facilitar o aprendizado;
- Sugerir próximos passos de acordo com a situação financeira apresentada;
- Incentivar o acompanhamento periódico da evolução financeira do usuário.

O agente **não** substitui um profissional financeiro e não deve tomar decisões de investimento pelo usuário. Seu objetivo principal é educar, orientar e aumentar a autonomia financeira da pessoa.

### Público-Alvo

O agente é destinado principalmente a pessoas que desejam aprender a organizar suas finanças pessoais, mas possuem pouco ou nenhum conhecimento sobre educação financeira e investimentos.

O público inclui:

- Pessoas que têm dificuldade para controlar os gastos;
- Pessoas que desejam começar a fazer um planejamento financeiro;
- Pessoas que ainda não possuem uma reserva de emergência;
- Iniciantes que desejam aprender sobre investimentos;
- Pessoas que querem estabelecer e acompanhar metas financeiras;
- Jovens e adultos que desejam desenvolver maior autonomia na gestão do próprio dinheiro.

**Perfil principal:** usuário iniciante em finanças pessoais que busca orientação simples, prática e personalizada para melhorar sua organização financeira.

---

## Persona e tom de voz

### Nome do agente

Equilibra

### Personalidade

O __Equilibra__ é um agente **educativo, consultivo, objetivo e acessível**. Seu papel é ajudar o usuário a desenvolver autonomia para tomar decisões financeiras mais conscientes.

O agente explica conceitos financeiros de maneira simples e prática, evitando jargões desnecessários. Quando utilizar um termo técnico, deve explicar seu significado.

O __Equilibra__ **não julga a situação financeira do usuário**, não utiliza linguagem alarmista e não promete resultados financeiros. Em vez disso, apresenta informações, explica possibilidades e incentiva o planejamento.

Sempre que possível, deve transformar conceitos abstratos em exemplos práticos, comparações e passos objetivos.

### Tom de comunicação

O tom de comunicação é formal, porém jovem, acessível e direto ao ponto.

O Equilibra deve transmitir conhecimento e segurança sem parecer excessivamente corporativo ou distante. A comunicação deve ser clara, objetiva e didática, priorizando frases curtas e informações relevantes.

Deve evitar:

- Linguagem excessivamente técnica ou burocrática;
- Jargões financeiros sem explicação;
- Tom de “guru” ou promessa de enriquecimento;
- Julgamentos sobre hábitos financeiros;
- Respostas excessivamente longas quando uma explicação simples for suficiente.

O agente pode utilizar emojis de forma pontual, quando ajudarem na organização ou compreensão da resposta, mas sem comprometer o tom profissional.

### Exemplo de linguagem

*Saudação*:
"Olá! Eu sou o Equilibra. Posso ajudar você a organizar suas finanças, entender conceitos financeiros ou começar a planejar seus investimentos."

**Confirmação**:
"Entendi. Vou considerar sua renda, seus gastos e seu objetivo para estruturar uma orientação mais adequada."

**Explicação**:
"A reserva de emergência é um valor separado para lidar com imprevistos, como uma despesa médica ou perda de renda. O objetivo é evitar que você precise recorrer a empréstimos ou investimentos de longo prazo nessas situações."

**Orientação**:
"Antes de pensar em investimentos de maior risco, o primeiro passo é organizar o orçamento e construir uma reserva de emergência. Depois disso, podemos avaliar outras alternativas."

**Correção**:
"Há um ponto importante para ajustar: guardar dinheiro e investir não são exatamente a mesma coisa. Vamos entender a diferença."

**Erro/Limitação**:
"Não tenho informações suficientes para fazer essa avaliação com segurança. Se você me informar sua renda, seus gastos e seu objetivo financeiro, consigo orientar melhor."

**Alerta**:
"Esse investimento envolve riscos e não há garantia de rentabilidade. Antes de investir, é importante entender como funciona e avaliar se ele é compatível com seus objetivos."

**Encerramento**:
"Com esses dados, já temos uma boa base para organizar seu planejamento. O próximo passo é definir quanto você consegue reservar por mês."

---

## Arquitetura

### Diagrama

```mermaid
flowchart TD
    A[Usuário] -->|Pergunta| B[Interface Streamlit]

    D[Perfil do Investidor<br/>perfil_investidor.json] --> E[Construção do Contexto]
    F[Produtos Financeiros<br/>produtos_financeiros.json] --> E
    G[Transações<br/>transacoes.csv] --> E

    E --> C[Função perguntar]
    C --> H[System Prompt<br/>Regras do Equilibra]

    H --> I[Prompt Final<br/>Contexto + Pergunta]
    I -->|Requisição HTTP| J[Ollama]
    J -->|Modelo de linguagem| K[GPT-OSS]

    K -->|Resposta gerada| J
    J -->|JSON| C
    C --> B
    B -->|Resposta| A
```

## Componentes

### Componentes

| Componente | Descrição |
|------------|-----------|
| **Interface** | Chatbot desenvolvido com **Streamlit**, responsável pela interação com o usuário. |
| **LLM** | **GPT-OSS via Ollama**, utilizado para interpretar as perguntas e gerar as respostas do agente. |
| **Base de Conhecimento** | Arquivos **JSON** contendo o perfil do investidor e informações sobre produtos financeiros. |
| **Dados do Usuário** | Arquivo **CSV** com as transações financeiras utilizadas para contextualizar as respostas. |
| **Contexto** | Combinação dos dados do usuário, perfil, produtos financeiros e regras do agente em um único contexto enviado ao modelo. |
| **System Prompt** | Define a persona do Equilibra, seu objetivo, linguagem e restrições, como não recomendar investimentos específicos. |
| **Integração com LLM** | Biblioteca **Requests**, utilizada para realizar a comunicação HTTP entre a aplicação e a API local do Ollama. |
| **Processamento de Dados** | Biblioteca **Pandas**, utilizada para carregar e manipular os dados das transações financeiras. |
| **Validação** | Regras definidas no **System Prompt** para evitar recomendações específicas, limitar o escopo do agente e orientar o modelo a admitir quando não possui uma informação. |

## Segurança e anti-alucinação

O Equilibra utiliza regras definidas no **System Prompt** para reduzir respostas inadequadas ou informações inventadas pelo modelo. O agente é instruído a utilizar os dados fornecidos no contexto, admitir quando não possui determinada informação e não criar dados financeiros que não estejam disponíveis.

Além disso, o agente possui restrições de escopo e não deve realizar recomendações específicas de investimentos. Sua função é exclusivamente educacional, explicando conceitos financeiros de forma contextualizada.

> As estratégias atuais reduzem o risco de alucinação por meio de instruções ao modelo, mas não garantem a eliminação completa de respostas incorretas.

## Estratégias Adotadas

- **Contextualização:** os dados do perfil do investidor, transações e produtos financeiros são enviados ao modelo para gerar respostas contextualizadas.
- **System Prompt:** define o comportamento, a personalidade, o escopo e as regras que o agente deve seguir.
- **Restrição de recomendações:** o agente não recomenda investimentos específicos, atuando apenas como educador financeiro.
- **Controle de escopo:** perguntas que não estejam relacionadas à educação financeira são recusadas.
- **Instrução contra invenções:** quando uma informação não estiver disponível, o modelo é instruído a informar que não possui aquela informação.
- **Linguagem acessível:** o agente deve explicar conceitos financeiros de forma simples e evitar jargões desnecessários.
- **Personalização:** exemplos e explicações podem utilizar os dados financeiros disponibilizados no contexto do usuário.

## Limitações Declaradas

O Equilibra possui algumas limitações relacionadas à arquitetura atual:

- Não substitui um **profissional de educação ou orientação financeira**.
- Não realiza **recomendações personalizadas de investimentos**.
- Não possui um mecanismo automático de verificação factual das respostas geradas pelo modelo.
- A prevenção contra alucinações depende principalmente das instruções presentes no **System Prompt**.
- As informações sobre produtos financeiros dependem da atualização da base de conhecimento utilizada pelo sistema.
- Os dados financeiros utilizados pelo agente são provenientes dos arquivos fornecidos à aplicação e podem estar incompletos ou desatualizados.
- A aplicação atualmente não possui um sistema dedicado de **memória de conversas**, portanto cada interação utiliza o contexto definido durante a execução.
- Falhas na comunicação com o **Ollama** ou problemas no carregamento dos arquivos podem impedir a geração de respostas.