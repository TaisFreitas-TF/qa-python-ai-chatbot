# Importa o Streamlit para criar a interface web
import streamlit as st

# Importa o cliente oficial da OpenAI
from openai import OpenAI


# ===============================
# CONFIGURAÇÃO DA PÁGINA
# ===============================

# Define título e ícone da aba do navegador
st.set_page_config(
    page_title="ChatBot com IA",
    page_icon="🤖"
)

# Título exibido na página
st.write("### ChatBot com IA")


# ===============================
# CONEXÃO COM A OPENAI
# ===============================

# Cria o cliente da OpenAI usando a chave salva em .streamlit/secrets.toml
# Isso evita expor a API Key no código
modelo = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


# ===============================
# HISTÓRICO DE MENSAGENS
# ===============================

# Se ainda não existir histórico na sessão do usuário,
# cria uma lista vazia (ou com uma mensagem de sistema)
if "lista_mensagens" not in st.session_state:
    st.session_state["lista_mensagens"] = [
        {
            "role": "system",
            "content": "Você é um assistente educado e responde em português."
        }
    ]


# ===============================
# EXIBIR MENSAGENS ANTERIORES
# ===============================

# Percorre todo o histórico e exibe as mensagens no chat
for mensagem in st.session_state["lista_mensagens"]:
    role = mensagem["role"]        # "user", "assistant" ou "system"
    content = mensagem["content"]  # texto da mensagem
    st.chat_message(role).write(content)


# ===============================
# ENTRADA DO USUÁRIO
# ===============================

# Campo de texto no estilo chat
mensagem_usuario = st.chat_input("Escreva sua mensagem aqui")


# ===============================
# PROCESSAR NOVA MENSAGEM
# ===============================

# Se o usuário digitou algo
if mensagem_usuario:

    # Exibe a mensagem do usuário no chat
    st.chat_message("user").write(mensagem_usuario)

    # Salva a mensagem do usuário no histórico
    st.session_state["lista_mensagens"].append(
        {"role": "user", "content": mensagem_usuario}
    )

    try:
        # Tentativa de chamada à OpenAI
        # Envia todo o histórico para a OpenAI
        resposta_modelo = modelo.chat.completions.create(
            model="gpt-4o",
            messages=st.session_state["lista_mensagens"]
        )   

        # Extrai apenas o texto da resposta do modelo
        resposta_ia = resposta_modelo.choices[0].message.content

        # Exibe a resposta da IA no chat
        st.chat_message("assistant").write(resposta_ia)

        # Salva a resposta da IA no histórico
        st.session_state["lista_mensagens"].append(
            {"role": "assistant", "content": resposta_ia}
        )



    except Exception as e:
        # Tratamento genérico para outros erros
        st.error(f"❌ Ocorreu um erro inesperado: {e}")
