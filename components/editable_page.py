import copy
from streamlit_ace import st_ace
import streamlit as st
from base_streamlit_state import BaseStreamlitState
from sqlite_utils.db import NotFoundError

class EditablePage(BaseStreamlitState):
    def __init__(self, page, edit=False):
        super().__init__()
        self.page = page
        try:
            self.data = self.state.db['page_content'].get(self.page)
            self.content = self.data['content']
        except Exception  as e:
            self.content = ""
            st.exception(e)

        self.edit = edit
        
        if self.content is None:
            self.edit = True
            self.content = ''

    def _exec(self, content):
        #override import fn
        exec(content)

    def builder_view(self):
        if self.edit:
            with st.container():
                self.content = st_ace(
                    self.content if self.content else '', language='python')
                st.write('Preview:')
                if self.content is not None:
                    self._exec(self.content)
                save = st.button('Save')

        if save and self.edit:
            self.state.db['page_content'].upsert(
                {'content': self.content, 'page': self.page}, pk="page")
            self.edit = False


    def render(self):
        with st.container():
            st.header(self.page)
            self.edit = st.checkbox('Edit this Page')
            if self.edit:
                self.builder_view()
                return
            self._exec(self.content)
