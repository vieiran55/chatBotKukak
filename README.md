# Questionário Kukac - Chat Bot 💬

Este é um aplicativo de questionário interativo implementado em Streamlit para o teste pratico do processo seletivo de Estácio na Kucak.

## Funcionalidades

- Apresenta um chat bot interativo para guiar o usuário por um questionário.
- Carrega perguntas a partir de um arquivo JSON.
- Registra e exibe as respostas do usuário.
- Calcula a pontuação do usuário com base nas respostas corretas.
- Oferece a opção de fazer o download das respostas do usuário em formato JSON.

## Como Executar

1. **Instale as dependências necessárias:**

    ```bash
    pip install streamlit
    ```

2. **Execute o aplicativo Streamlit:**

    ```bash
    streamlit run nome_do_arquivo.py
    ```

   Substitua `nome_do_arquivo.py` pelo nome do arquivo que contém o código fornecido.

## Estrutura do Código

- `carregar_perguntas`: Função que carrega as perguntas a partir de um arquivo JSON.
- `main`: Função principal que implementa a lógica do chat bot e do questionário.
- **Histórico de Mensagens:** Utiliza a estrutura de `st.session_state` para armazenar e exibir mensagens do chat.
- **Pontuação:** A pontuação do usuário é calculada com base nas respostas corretas.
- **Download de Respostas:** Permite que o usuário faça o download das respostas em formato JSON.

## Estilo

O aplicativo utiliza um arquivo de estilo `styles.css` para personalização do visual.

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests para melhorar o aplicativo.

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---
