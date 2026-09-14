# Import Streamlit to create our web application
import streamlit as st

# Import our main question-answering function
from src.router import answer_business_question


# Configure the Streamlit page
st.set_page_config(
    page_title="Mercato AI Business Analyst",
    page_icon="🛒",
    layout="wide"
)


# Display the application title
st.title("🛒 Mercato AI Business Analyst")


# Explain what the application does
st.markdown(
    """
    Ask questions about **Mercato's business data and company policies**.

    The AI automatically decides whether your question should use
    **business data, company documents, or both**.
    """
)


# Create a divider
st.divider()


# Create conversation memory for the current session
if "messages" not in st.session_state:

    # Start with an empty conversation
    st.session_state.messages = []


# Display previous conversation messages
for message in st.session_state.messages:

    # Display each message with its appropriate role
    with st.chat_message(message["role"]):

        # Display the saved message
        st.markdown(message["content"])


# Create the chat input box
question = st.chat_input(
    "Ask your business question..."
)


# Run this section when the user submits a question
if question:

    # Save the user's question
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )


    # Display the user's question
    with st.chat_message("user"):

        # Show the question
        st.markdown(question)


    # Create the assistant response area
    with st.chat_message("assistant"):

        # Show a loading indicator
        with st.spinner("Analyzing your question..."):

            # Process the question through our backend
            try:

                # Send the question to the router
                result = answer_business_question(question)

            # Handle unexpected application errors
            except Exception:

                # Show a friendly error message
                st.error(
                    "Something went wrong while processing "
                    "your question. Please try again."
                )

                # Stop processing this request
                st.stop()


        # Display the route selected by the router
        st.caption(
            f"Data source used: **{result['route']}**"
        )


        # Display the final answer
        st.markdown(result["answer"])


        # Show sources when RAG was used
        if result["route"] in ["RAG", "BOTH"]:

            # Create a collapsible source section
            with st.expander("📄 View document sources"):

                # Get the backend details
                details = result["details"]


                # Get sources from a RAG response
                if result["route"] == "RAG":

                    # Retrieve RAG source results
                    sources = details["sources"]


                # Get sources from a BOTH response
                else:

                    # Retrieve RAG source results
                    sources = details["rag_sources"]


                # Display every retrieved document
                for source in sources:

                    # Get the original document path
                    source_name = source["chunk"].metadata.get(
                        "source",
                        "Unknown source"
                    )

                    # Extract only the filename
                    source_name = source_name.replace(
                        "\\",
                        "/"
                    ).split("/")[-1]

                    # Display the document name
                    st.write(
                        f"📄 **{source_name}**"
                    )


        # Save the AI answer in the conversation
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": result["answer"]
            }
        )