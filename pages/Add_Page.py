import streamlit as st
from components.editable_page import EditablePage
page = st.text_input('Page Name')
if page:
    EditablePage(page, edit=True).render()