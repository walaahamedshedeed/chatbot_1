import streamlit as st
import sys
from main import memory, Chatbot1

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = Chatbot1(memory=memory)

def main():
    st.title("CrewAI Chatbot")
    
    initialize_session_state()

    # Chat input
    user_input = st.chat_input("Type your message here...")
    
    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        try:
            # Get chatbot response
            response = st.session_state.chatbot.process_input(user_input)
            # Add bot response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Error: {str(e)}")

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

if __name__ == "__main__":
    main()