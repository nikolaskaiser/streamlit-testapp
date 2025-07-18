import streamlit as st

st.title("🚀 Test-App")
st.write("Willkommen bei deiner ersten Streamlit-Test-App!")

name = st.text_input("Wie heißt du?")
if name:
    st.success(f"Hallo, {name} 👋")
