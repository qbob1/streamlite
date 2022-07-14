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
        if 'initializer' not in self.state:
            try:
                st.session_state.initializer = self.parse_initializer(self.state.db['initializer'].get(1)['boot'])
            except NotFoundError:
                self.init_pages()
        if 'initializer' in self.state:
            self.state.initializer(self)
        

    def parse_initializer(self, initializer):
        return types.FunctionType(marshal.loads(initializer), globals(), 'initializer')

    def init_pages(self):
        import os
        path = './pages'
        if not os.path.exists(path):
            os.makedirs(path)
        
        for page in self.state.db.query('select distinct page from page_content'):
            if not os.path.exists(path+'/'+page['page']+'.py'):
                with open(path+'/'+page['page']+'.py', 'w') as f:
                    f.write(self.page_template(page['page']))
                    
    def page_template(self, page):
        return f"""from components.editable_page import EditablePage\nEditablePage('{page}').render()""".strip()