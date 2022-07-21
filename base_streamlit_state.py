import marshal
import types
import streamlit as st
from pyparsing import col
from sqlite_utils import Database
from sqlite_utils.db import NotFoundError


class BaseStreamlitState:
    def __init__(self):
        self.state = st.session_state
        self.state.db = Database('streamlite.db')
        if 'initializer' not in self.state:
            try:
                st.session_state.initializer = self.parse_initializer(self.state.db['initializer'].get(1)['boot'])
            except NotFoundError:
                pass
        if 'initializer' in self.state:
            self.state.initializer(self)
        self.init_pages()
        

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

    def _import(name, *args, **kwargs):
        try:
            __import__(name)
        except ImportError:
            import pip
            pip.main(['install', name]) 
                    
    def page_template(self, page):
        return f"""from components.editable_page import EditablePage\nEditablePage('{page}').render()""".strip()