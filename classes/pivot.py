import pandas as pd

class Pivot:
    def __init__(self):
        self.df_raw = pd.read_csv('files_output/pinyin.csv')
        self.column = None
        self.pinyin = None
        self.value = None
    def _make_dict(self, pair):
        assert len(pair) == 2
        return dict([pair, reversed(pair)])
    def _make_reverse(self):
        self.columns = self._make_dict(['Initial', 'Rhyme'])
        self.pinyins = self._make_dict(['Cantonese', 'Mandarin'])
        self.column2 = self.columns[self.column]
        self.pinyin2 = self.pinyins[self.pinyin]
    def _make_columns(self):
        self.column_query = f'{self.column}_{self.pinyin}'
        self.columns_group = [f'{self.column}_{self.pinyin2}', f'{self.column2}_{self.pinyin}']
    def _pivot(self):
        self.df = self.df_raw.query(f'{self.column_query} == "{self.value}"').groupby(self.columns_group).size().unstack()
        self.df = self.df.fillna('').astype(str)
        if self.df.shape[1] > self.df.shape[0]:
            self.df = self.df.T
    def main(self):
        self._make_reverse()
        self._make_columns()
        self._pivot()