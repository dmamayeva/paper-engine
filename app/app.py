import streamlit as st
import ingest
import rag
import time
import uuid

from dotenv import load_dotenv
load_dotenv(dotenv_path='../.envrc')


def print_log(message):
    print(message, flush=True)

def main():
    print_log("Paper Engine start>>>Time to grind!")
    st.title("Paper Engine")
    st.subheader("Helping to grind")
    
    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = str(uuid.uuid4())
        print_log(
            f"New conversation started with ID: {st.session_state.conversation_id}"
        )
    if "count" not in st.session_state:
        st.session_state.count=0
        print_log("Feedback count set to 0")

    user_input = st.text_input("Enter question")
    if st.button("Ask"):
        print_log(f"Your question: '{user_input}'")
        with st.spinner("Thinking>>"):
            start_time = time.time()
            answer = rag.rag(user_input)
            end_time = time.time()
            print_log(f"Answer received in {end_time - start_time:.2f} seconds")
            st.success("Completed!")
            st.write(answer)
     # Feedback buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("+1"):
            st.session_state.count += 1
            print_log(
                f"Positive feedback received. New count: {st.session_state.count}"
            )
            # save_feedback(st.session_state.conversation_id, 1)
            print_log("Positive feedback saved to database")
    with col2:
        if st.button("-1"):
            st.session_state.count -= 1
            print_log(
                f"Negative feedback received. New count: {st.session_state.count}"
            )
            # save_feedback(st.session_state.conversation_id, -1)
            print_log("Negative feedback saved to database")

    st.write(f"Current count: {st.session_state.count}")

if __name__ == "__main__":
    print_log("Time to grind!")
    main()
