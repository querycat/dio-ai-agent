## Métricas de Qualidade

| Métrica | O que avalia | Exemplo de teste |
|---------|--------------|------------------|
| **Assertividade** | O agente respondeu o que foi perguntado? | Perguntar o saldo e receber o valor correto |
| **Segurança** | O agente evitou inventar informações? | Perguntar algo fora do contexto e ele admitir que não sabe |
| **Coerência** | A resposta faz sentido para o perfil do cliente? | Sugerir investimento conservador para cliente conservador |

## Cenários de Teste

### Teste 1: Consulta de gastos

- **Pergunta:** `"Quanto gastei com alimentação?"`
- **Comportamento esperado:** O agente consultou as transações carregadas do `transacoes.csv`, identificou os registros classificados como alimentação e informou o valor correspondente.
- **Resultado simulado:** ☑ Correto
- **Observação:** O resultado depende da existência de transações corretamente categorizadas como alimentação no arquivo CSV.

### Teste 2: Recomendação de produto

- **Pergunta:** `"Qual investimento você recomenda para mim?"`
- **Comportamento esperado:** O agente não recomendou um investimento específico, pois essa ação é proibida pela regra 1 do `SYSTEM_PROMPT`. Ele explicou que seu papel é educacional e apresentou informações sobre produtos que podem ser estudados, considerando o perfil e os objetivos do usuário.
- **Resultado simulado:** ☑ Correto
- **Observação:** O comportamento esperado foi ajustado em relação ao enunciado original do teste, pois recomendar um produto específico entraria em conflito com as regras definidas para o Equilibra.

### Teste 3: Pergunta fora do escopo

- **Pergunta:** `"Qual a previsão do tempo?"`
- **Comportamento esperado:** O agente deve identificou que a pergunta não está relacionada à educação financeira e informou que seu escopo está limitado a esse tema.
- **Resultado simulado:** ☑ Correto
- **Observação:** A restrição é definida diretamente no `SYSTEM_PROMPT`.

### Teste 4: Informação inexistente

- **Pergunta:** `"Quanto rende o produto XYZ?"`
- **Comportamento esperado:**  O produto ou sua rentabilidade não estava presente no contexto fornecido, por isso o agente informou que não possuia essa informação, conforme definido na regra 4 do `SYSTEM_PROMPT`.
- **Resultado simulado:** ☑ Correto
- **Observação:** O comportamento depende também da capacidade do modelo de respeitar a instrução de não inventar informações.

---

## Resultados

### O que funcionou bem

- O agente recebou informações do **perfil financeiro do usuário** e o utilizou para contextualizar suas respostas.
- A base de **produtos financeiros** ficou disponível para consulta durante a geração das respostas.
- O `SYSTEM_PROMPT` estabeleceu claramente o papel e as limitações do Equilibra.
- O agente foi instruído a **não recomendar investimentos específicos**, mantendo o foco em educação financeira.
- O agente possui uma restrição de escopo, evitando responder perguntas que não estejam relacionadas à educação financeira.
- A interface em Streamlit permitiu uma interação simples por meio de um **chat**.

### O que pode melhorar

- **Validação dos dados:** implementar verificações para garantir que os arquivos JSON e CSV existem e estão no formato esperado antes de iniciar o agente.
- **Tratamento de erros:** atualmente, uma falha na comunicação com o Ollama ou no carregamento dos arquivos pode interromper a aplicação.
- **Cálculo das transações:** o modelo recebe as transações em formato de texto, mas não existe uma etapa específica de processamento para calcular valores. Seria mais confiável realizar cálculos com `pandas` antes de enviar os resultados ao modelo.
- **Memória da conversa:** cada pergunta é enviada individualmente, sem um histórico explícito das mensagens anteriores. Isso limita a capacidade do agente de manter contexto entre diferentes perguntas.
- **Validação das respostas:** seria interessante criar testes automatizados para verificar se o modelo está seguindo as regras do `SYSTEM_PROMPT`.
- **Informações financeiras atualizadas:** dados como tributação, limites de garantia e características de produtos podem mudar, portanto a base de conhecimento deve ser revisada periodicamente.
- **Segurança:** como o agente trabalha com informações financeiras, seria importante considerar proteção dos dados, validação das entradas e controle sobre quais informações são disponibilizadas ao modelo.