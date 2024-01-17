import streamlit as st
import json
import base64
import time

# Adiciona um container para o conteúdo do chat
chat_container = st.empty()

# Carrega a lista de perguntas
def carregar_perguntas(file_path="questionario_kukac.json"):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        perguntas = data.get("perguntas", [])
    return perguntas

# Início do programa
def main():
    # Importa o styles.css
    with open("static/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Título da aplicação
    st.title("💻 Chat Bot 💬 - Questionário Kukac ")

    # Mensagem de boas-vindas
    with st.chat_message(name="assistant"):
        st.write("Seja bem-vindo ao Questionário Kukac! Jovem Padawan")

    # Carrega as perguntas
    perguntas = carregar_perguntas()

    # Faz um delay entre as perguntas
    time.sleep(2)

    # Inicia as mensagens
    st.session_state.messages = st.session_state.get("messages", [])

    # Inicia a pontuação
    st.session_state.pontuacao = st.session_state.get("pontuacao", 0)

    # Inicia o índice da questão
    st.session_state.current_question_index = st.session_state.get("current_question_index", 0)

    # Inicia o array com as respostas do usuário
    st.session_state.respostas_usuario = st.session_state.get("respostas_usuario", [])

    # Define o histórico de mensagens
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Verifica se há mais perguntas a serem respondidas
    if st.session_state.current_question_index < len(perguntas):
        # Obtém a pergunta atual
        pergunta = perguntas[st.session_state.current_question_index]
        pergunta_apresentada = any(message["content"] == pergunta["texto"] for message in st.session_state.messages)

        # Se a pergunta ainda não foi apresentada
        if not pergunta_apresentada:
            with st.chat_message(name="assistant"):
                st.markdown(pergunta["texto"])
            # Adiciona a mensagem ao histórico
            st.session_state.messages.append({"role": "assistant", "content": pergunta["texto"]})

        # Recebe a resposta do usuário
        resposta_usuario = st.chat_input("Digite sua resposta")
        if resposta_usuario:
            with st.chat_message("user"):
                st.markdown(resposta_usuario)
            st.session_state.messages.append({"role": "user", "content": resposta_usuario})
            resposta_correta = pergunta.get("resposta_correta", "")
            correto = resposta_usuario.lower() == resposta_correta.lower()

            st.session_state.respostas_usuario.append({
                "pergunta": pergunta["texto"],
                "resposta_usuario": resposta_usuario,
                "correto": correto
            })

            if resposta_correta:
                response = "Correto! 🎉" if correto else f"Incorreto. A resposta correta é: {resposta_correta}"
                st.session_state.pontuacao += 1 if correto else 0
                with st.chat_message(name="assistant"):
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})

            st.session_state.current_question_index += 1

            # Se houver mais perguntas, apresenta a próxima
            if st.session_state.current_question_index < len(perguntas):
                next_pergunta = perguntas[st.session_state.current_question_index]
                with st.chat_message(name="assistant"):
                    st.markdown(next_pergunta["texto"])
            else:
                st.balloons()
                st.write("Você concluiu o questionário!")
                st.write(f"Sua pontuação final é: {st.session_state.pontuacao}")
                
                st.session_state.respostas_usuario.append({"pontuacao_final": st.session_state.pontuacao})
                
                download_link = f'<a href="data:application/json;base64,{base64.b64encode(json.dumps(st.session_state.respostas_usuario, indent=2, ensure_ascii=False).encode()).decode()}" download="respostas_usuario.json">Download Respostas</a>'
                st.markdown(download_link, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
