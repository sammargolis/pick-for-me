import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 Pick my meal for me")
st.write(
    "This is a chatbot that helps you decide what to order. "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
    )

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # System prompt
    system_prompt = {
        "role": "system",
        "content": "Select an order at a restaurant based on customer reviews. Focus on the dishes people loved the most. Use only the information provided about the number of starters, mains, or people. Provide a concise suggestion without asking additional questions or adding unnecessary details."
    }


    # Initialize session state if it doesn't exist, including the system prompt
    if "messages" not in st.session_state:
        st.session_state.messages = [system_prompt]


    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages[1:]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("Give some information on the meal you want"):

        # Here is the system prompt to use: Select an order at a restaurant based on customer reviews. Focus on the dishes people loved the most. Use only the information provided about the number of starters, mains, or people. Provide a concise suggestion without asking additional questions or adding unnecessary details.

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
