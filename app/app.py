import streamlit as st
import ingest
import rag
import time
import uuid
from db import (
    save_conversation,
    save_feedback,
    get_recent_conversations,
    get_feedback_stats,
)

def print_log(message):
    print(message, flush=True)

def main():
    print_log("Paper Engine start>>>Time to grind!")
    st.title("Paper Engine")
    st.subheader("Helping to grind")

    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = str(uuid.uuid4())
        print_log(f"New conversation started with ID: {st.session_state.conversation_id}")

    if "count" not in st.session_state:
        st.session_state.count = 0
        print_log("Feedback count set to 0")

    user_input = st.text_input("Enter question")

    if st.button("Ask"):
        print_log(f"Your question: '{user_input}'")
        with st.spinner("Thinking>>"):
            start_time = time.time()
            answer_data = rag.rag(user_input)
            end_time = time.time()
            print_log(f"Answer received in {end_time - start_time:.2f} seconds")

        st.success("Completed!")
        st.write(answer_data['answer'])
        st.write(f"Response time: {answer_data['response_time']:.2f} seconds")
        st.write(f"Relevance: {answer_data['relevance']}")
        st.write(f"Total tokens: {answer_data['total_tokens']}")
        if answer_data["openai_cost"] > 0:
            st.write(f"OpenAI cost: ${answer_data['openai_cost']:.4f}")

        print_log("Saving conversation to database")
        save_conversation(st.session_state.conversation_id, user_input, answer_data)
        print_log("Conversation saved successfully")

        # Generate a new conversation ID for next question
        st.session_state.conversation_id = str(uuid.uuid4())

        # Feedback buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Cool answer!"):
                st.session_state.count += 1
                print_log(f"Positive feedback received. New count: {st.session_state.count}")
                save_feedback(st.session_state.conversation_id, 1)
                print_log("Positive feedback saved to database")
        with col2:
            if st.button("Wrong thing"):
                st.session_state.count -= 1
                print_log(f"Negative feedback received. New count: {st.session_state.count}")
                save_feedback(st.session_state.conversation_id, -1)
                print_log("Negative feedback saved to database")

        st.write(f"Current count: {st.session_state.count}")

    st.subheader("Recent Conversations")
    relevance_filter = st.selectbox(
        "Filter by relevance:", ["All", "RELEVANT", "PARTLY_RELEVANT", "NON_RELEVANT"]
    )
    try:
        recent_conversations = get_recent_conversations(
            limit=5, relevance=relevance_filter if relevance_filter != "All" else None
        )
        if recent_conversations:
            for conv in recent_conversations:
                st.write(f"Q: {conv.get('question', 'N/A')}")
                st.write(f"A: {conv.get('answer', 'N/A')}")
                st.write(f"Relevance: {conv.get('relevance', 'N/A')}")
                st.write("---")
        else:
            st.write("No recent conversations found.")
    except Exception as e:
        print_log(f"Error retrieving recent conversations: {e}")
        st.error("Unable to retrieve recent conversations at this time.")

    # Display feedback stats
    try:
        feedback_stats = get_feedback_stats()
        st.subheader("Feedback Statistics")
        st.write(f"Thumbs up: {feedback_stats['thumbs_up']}")
        st.write(f"Thumbs down: {feedback_stats['thumbs_down']}")
    except Exception as e:
        print_log(f"Error retrieving feedback stats: {e}")
        st.error("Unable to retrieve feedback statistics at this time.")

    print_log("Streamlit app loop completed")

if __name__ == "__main__":
    print_log("Time to grind!")
    main()
