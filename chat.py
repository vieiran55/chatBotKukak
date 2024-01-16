import streamlit as st
import json
import base64

def carregar_perguntas(file_path="questionario_kukac.json"):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        perguntas = data.get("perguntas", [])
    return perguntas
  
def main():
    st.title("Chat Bot - Questionário Kukac")

    with st.chat_message(name="assistant"):
        st.write("Seja bem-vindo ao Questionário Kukac! Jovem Padawan")

    perguntas = carregar_perguntas()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "pontuacao" not in st.session_state:
        st.session_state.pontuacao = 0

    if "current_question_index" not in st.session_state:
        st.session_state.current_question_index = 0

    if "respostas_usuario" not in st.session_state:
        st.session_state.respostas_usuario = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if st.session_state.current_question_index < len(perguntas):
        pergunta = perguntas[st.session_state.current_question_index]
        pergunta_apresentada = any(message["content"] == pergunta["texto"] for message in st.session_state.messages)

        if not pergunta_apresentada:
            with st.chat_message("assistant"):
                st.markdown(pergunta["texto"])
            st.session_state.messages.append({"role": "assistant", "content": pergunta["texto"]})
            
        resposta_usuario = st.chat_input("Digite sua resposta")
        if resposta_usuario:
            with st.chat_message("user"):
                st.markdown(resposta_usuario)
            st.session_state.messages.append({"role": "user", "content": resposta_usuario})
            resposta_correta = pergunta.get("resposta_correta", "")
            correto = resposta_usuario.lower() == resposta_correta.lower()

            st.session_state.respostas_usuario.append({"pergunta": pergunta["texto"], "resposta_usuario": resposta_usuario, "correto": correto})

            if resposta_correta:
                response = "Correto! 🎉" if correto else f"Incorreto. A resposta correta é: {resposta_correta}"
                st.session_state.pontuacao += 1 if correto else 0
                with st.chat_message("assistant"):
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
            
            st.session_state.current_question_index += 1

            if st.session_state.current_question_index < len(perguntas):
                next_pergunta = perguntas[st.session_state.current_question_index]
                with st.chat_message("assistant"):
                    st.markdown(next_pergunta["texto"])
                    
            else:
                st.balloons()
                st.write("Você concluiu o questionário!")
                st.write(f"Sua pontuação final é: {st.session_state.pontuacao}")
                
                st.session_state.respostas_usuario.append({"pontuacao_final": st.session_state.pontuacao})
                
                download_link = f'<a href="data:application/json;base64,{base64.b64encode(json.dumps(st.session_state.respostas_usuario, indent=2, ensure_ascii=False).encode()).decode()}" download="respostas_usuario.json">Download Respostas</a>'
                st.markdown(download_link, unsafe_allow_html=True)
                
                st.write("Respostas do Usuário:")
                st.json(st.session_state.respostas_usuario)
          
if __name__ == "__main__":
    main()
