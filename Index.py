import streamlit as st
from components.editable_page import EditablePage
from sqlite_utils import Database

p = EditablePage('index')
if p.content == "":
    p.content = """
st.write('Hello and welcome to streamlite, an automation framework built on streamlit and sqlite')
with st.container():
    st.write('To get started you can')
    st.button('Add a page')
    st.write('Or click the checkbox above to edit this page')"""
p.render()


