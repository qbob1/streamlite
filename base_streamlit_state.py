import marshal
import types
import streamlit as st
from pyparsing import col
from sqlite_utils import Database
from enum import IntFlag, auto
from sqlite_utils.db import NotFoundError
import os

class BaseStreamlitState:
    def __init__(self):
        self.state = st.session_state
        self.state.db = Database('streamlite.db')
        self.init_pages()

        if 'initializer' not in self.state:
            try:
                self.parse_initializer(self.state.db['initializer'].get(1)['boot'])
            except Exception as e:
                st.write(str(e))

        if 'initializer' in self.state:
            try:
                self.state.initializer.initialize(self)
            except Exception as e:
                st.warning(str(e))

    def parse_initializer(self, initializer):
        exec(marshal.loads(initializer), globals())
        self.state.initializer = Initializer

    def init_pages(self):
        import os
        
        path = './pages'
        if not os.path.exists(path):
            os.makedirs(path)

        if self.state.db["page_content"].exists():
            for page in self.state.db.query('select distinct page from page_content'):
                if not os.path.exists(path+'/'+page['page']+'.py'):
                    with open(path+'/'+page['page']+'.py', 'w') as f:
                        f.write(self.page_template(page['page']))
                    
    def page_template(self, page):
        return f"""from components.editable_page import EditablePage\nEditablePage('{page}').render()""".strip()
