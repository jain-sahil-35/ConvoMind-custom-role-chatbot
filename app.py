import streamlit as st
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="ConvoMind",
    page_icon="🤖",
    layout="centered"
)

st.title("ConvoMind - Custom Role Chatbot")
st.caption("Powered by HuggingFace + LangChain")

with st.sidebar:
    st.header("Chatbot Settings")

    system_role = st.text_area(
        "Define the role of the chatbot",
        value="You are a helpful assistant",
        height=120
    )

    temperature = st.slider(
        "Creativity (temperature)",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1
    )

    if st.button("🔄 Reset Chat"):
        st.session_state.chat_history = [
            SystemMessage(content=system_role)
        ]
        st.rerun()

@st.cache_resource
def load_model(temp):
    llm = HuggingFaceEndpoint(
        repo_id="openai/gpt-oss-safeguard-20b",
        task="text-generation",
        temperature=temp
    )
    return ChatHuggingFace(llm=llm)

model = load_model(temperature)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        SystemMessage(content=system_role)
    ]

st.session_state.chat_history[0] = SystemMessage(content=system_role)

for msg in st.session_state.chat_history[1:]:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(msg.content)

user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.chat_history.append(
        HumanMessage(content=user_input)
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = model.invoke(st.session_state.chat_history)
            response = result.content
            st.markdown(response)

    st.session_state.chat_history.append(
        AIMessage(content=response)
    )
