import streamlit as st
import chatbot_backend as chat_bot

# Set Title for Chatbot
st.title("Ausura 😎")

model_id = st.selectbox('Please select a model:', ('anthropic.claude-3-haiku-20240307-v1:0', 'meta.llama3-8b-instruct-v1:0'))

if 'llm' not in st.session_state:
    st.session_state.llm = chat_bot.initialize_chatbot(model_id)

if 'memory' not in st.session_state or st.session_state.memory is None:
    st.session_state.memory = chat_bot.initialize_memory(st.session_state.llm)

if 'context_appended' not in st.session_state:
    st.session_state.context_appended = False

if 'plant_name' not in st.session_state:
    st.session_state.plant_name = None

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Re-render the chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])

# Enter the details for chatbot input box
input_text = st.chat_input(f"Powered by {model_id}")

if input_text:
    with st.chat_message("user"):
        st.markdown(input_text)
        st.session_state.chat_history.append({"role": "user", "text": input_text})

        plant_names = chat_bot.extract_plant_names()

        # Call attach_context with plant_names
        input_text, st.session_state.context_appended, plant_name = chat_bot.attach_context(input_text, st.session_state.context_appended, plant_names, st.session_state)
        chat_response, st.session_state.context_appended = chat_bot.start_conversation(input_text, st.session_state.llm, st.session_state.memory, model_id, st.session_state.context_appended, plant_names, st.session_state)

        # Append new assistant message to chat history
        st.session_state.chat_history.append({"role": "assistant", "text": chat_response})

    with st.chat_message("assistant"):
        st.markdown(chat_response)


