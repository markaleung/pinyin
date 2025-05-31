import os, pandas as pd
os.chdir(os.path.dirname(__file__)+'/..')
from classes import pivot
import streamlit as st

class Manager:
    def _select_character_language(self):
        self.pivot = pivot.Pivot()
        self.pivot.column = st.selectbox('Character Part', ['Rhyme', 'Initial'])
        self.pivot.pinyin = st.selectbox('Language', ['Mandarin', 'Cantonese'])
    def _select_value(self):
        self.segment = f'{self.pivot.column}_{self.pivot.pinyin}'
        self.unique = sorted(self.pivot.df_raw[self.segment].unique())
        self.default = self.unique.index('ang') if 'ang' in self.unique else 0
        self.pivot.value = st.selectbox(
            'Value', self.unique, index = self.default
        )
    def _run_pivot(self):
        self.pivot.main()
        self.columns_sort = self.pivot.df.sum().sort_values(ascending = False).index
        self.index_sort = self.pivot.df.sum(axis = 1).sort_values(ascending = False).index
        self.pivot.df = self.pivot.df.loc[self.index_sort, self.columns_sort]
        st.dataframe(self.pivot.df)
    def _filter_examples(self):
        self.column_name = st.selectbox(
            self.pivot.df.columns.name, self.pivot.df.columns
        )
        self.df_filtered = self.pivot.df.T.query(
            f'{self.pivot.df.columns.name} == @self.column_name'
        ).T.dropna()
        self.index_name = st.selectbox(
            self.df_filtered.index.name, self.df_filtered.index
        )
    def _run_examples(self):
        st.dataframe(self.pivot.df_raw.query(
            f'{self.segment} == @self.pivot.value ' 
            f'and {self.pivot.df.columns.name} == @self.column_name '
            f'and {self.pivot.df.index.name} == @self.index_name '
        )[self.pivot.df_raw.columns[0:3]])
    def main(self):
        self._select_character_language()
        self._select_value()
        self._run_pivot()
        self._filter_examples()
        self._run_examples()

manager = Manager()
manager.main()