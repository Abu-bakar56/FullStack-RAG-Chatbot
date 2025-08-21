import streamlit as st
from langchain_core.messages import HumanMessage
from services.search import process_query
from services.chat import create_thread, get_user_threads, get_chat_history, save_chat_message
import asyncio
import time


def main():
    st.title("Full Stack Chatbot on Netsol Document & Web Search")

    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = None
    if "message_history" not in st.session_state:
        st.session_state['message_history'] = []
    if "show_login_form" not in st.session_state:
        st.session_state.show_login_form = True
    if "show_register_form" not in st.session_state:
        st.session_state.show_register_form = False

    if not st.session_state.user_id:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Login", key="login_button"):
                st.session_state.show_login_form = True
                st.session_state.show_register_form = False
                st.rerun()
        with col2:
            if st.button("Register", key="register_button"):
                st.session_state.show_login_form = False
                st.session_state.show_register_form = True
                st.rerun()

        if st.session_state.show_login_form:
            st.subheader("Login")
            with st.form("login_form"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Login")
                if submit:
                    if email and password:
                        from services.auth import login_user    
                        user_id = login_user(email, password)
                        if user_id:
                            st.session_state.user_id = user_id
                            st.session_state.thread_id = create_thread(user_id)
                            st.session_state['message_history'] = []
                            st.success("Login successful! You can now start chatting.")
                            st.rerun()
                        else:
                            st.error("Invalid email or password.")
                    else:
                        st.error("Please fill in all fields.")

        if st.session_state.show_register_form:
            st.subheader("Register")
            with st.form("register_form"):
                username = st.text_input("Username")
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Register")
                if submit:
                    if username and email and password:
                        from services.auth import register_user
                        user_id = register_user(username, email, password)
                        if user_id:
                            st.session_state.user_id = user_id
                            st.session_state.thread_id = create_thread(user_id)
                            st.session_state['message_history'] = []
                            st.success("Registration successful! You can now start chatting.")
                            st.rerun()
                        else:
                            st.error("Registration failed. Email or username may already exist.")
                    else:
                        st.error("Please fill in all fields.")
    else:
        st.subheader("Chat")
        with st.sidebar:
            st.subheader("Your Chats")
            user_threads = get_user_threads(st.session_state.user_id)
            if not user_threads:
                st.write("No previous chats available.")
            else:
                thread_options = {}
                for i, thread_id in enumerate(user_threads):
                    chat_history = get_chat_history(thread_id, st.session_state.user_id)
                    first_message = chat_history[0]["content"] if chat_history else f"Chat {i+1}"
                    thread_options[first_message[:30]] = thread_id
                selected_title = st.selectbox("Select a chat to resume", list(thread_options.keys()), index=list(thread_options.keys()).index(first_message[:30]) if st.session_state.thread_id in user_threads else 0)
                if thread_options[selected_title] != st.session_state.thread_id:
                    st.session_state.thread_id = thread_options[selected_title]
                    st.session_state['message_history'] = get_chat_history(st.session_state.thread_id, st.session_state.user_id)
                    st.rerun()

            if st.button("Start New Chat", key="new_chat_button"):
                st.session_state.thread_id = create_thread(st.session_state.user_id)
                st.session_state['message_history'] = []
                st.rerun()
            if st.button("Logout", key="logout_button"):
                st.session_state.user_id = None
                st.session_state.thread_id = None
                st.session_state['message_history'] = []
                st.session_state.show_login_form = True
                st.session_state.show_register_form = False
                st.rerun()

        for message in st.session_state['message_history']:
            with st.chat_message(message['role'], avatar="👤" if message['role'] == "user" else "🤖"):
                st.text(message['content'])

        user_input = st.chat_input("Type here")
        if user_input and isinstance(user_input, str) and user_input.strip():
            if "message_history" not in st.session_state or not st.session_state['message_history']:
                st.session_state['message_history'] = []
            st.session_state['message_history'].append({'role': 'user', 'content': user_input})
            with st.chat_message('user', avatar="👤"):
                st.text(user_input)

            from core.models import AgentState
            initial_state = AgentState(
                messages=[HumanMessage(content=user_input)],
                retrieved_docs=[],
                web_results="",
                final_answer="",
                needs_web_search=False,
                user_id=st.session_state.user_id,
                thread_id=st.session_state.thread_id
            )

            # Simulate streaming by breaking the response into chunks
            def stream_response():
                result = asyncio.run(process_query(initial_state))
                if result is None or not isinstance(result, dict) or "final_answer" not in result or not result["final_answer"]:
                    return
                ai_message = result["final_answer"]
                # Split the response into words or small chunks for streaming effect
                words = ai_message.split()
                for i in range(0, len(words), 2):  # Stream 2 words at a time
                    yield " ".join(words[i:i+2]) + " "
                    time.sleep(0.05)  # Adjust delay for desired streaming speed

            with st.chat_message('assistant', avatar="🤖"):
                ai_message = st.write_stream(stream_response())
            
            if ai_message:
                st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
                save_chat_message(st.session_state.thread_id, st.session_state.user_id, {'role': 'user', 'content': user_input})
                save_chat_message(st.session_state.thread_id, st.session_state.user_id, {'role': 'assistant', 'content': ai_message})
            else:
                st.error("Error: No valid response from the AI. Please try again.")


if __name__ == "__main__":
    main()
