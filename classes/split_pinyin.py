import pandas as pd, jyutping, pinyin, re

class _SplitCharacter:
    def __init__(self, character):
        self.character = character
        self.output = {}
    def _set_subclass_variables(self):
        pass
    def _fix_character(self):
        for self.start, self.end in self.replacements:
            self.character = re.sub(self.start, self.end, self.character)
    def _parse_character(self):
        self.initial, self.middle, self.final, self.tone = re.search(r'^([^aieouü_]*)([aieouü_]+)([^aieouü_]*)(\d)', self.character).groups()
        self.output = {
            f'Initial_{self.name}': self.initial, 
            # f'middle_{self.name}': self.middle, 
            # f'final_{self.name}': self.final, 
            f'Rhyme_{self.name}': self.middle + self.final, 
            f'Tone_{self.name}': self.tone, 
        }
    def main(self):
        self._set_subclass_variables()
        if isinstance(self.character, str):
            self._fix_character()
            try:
                self._parse_character()
            except (AttributeError, TypeError):
                print(self.character)
        return self.output
class Cantonese(_SplitCharacter):
    def _set_subclass_variables(self):
        self.name = 'Cantonese'
        self.replacements = [
            [r'^ng(\d)', r'_ng\1'], 
            ['yu', 'ü'], 
            # i and u are different for velar/nonvelar final
            # [r'^([^aeiou]*)([iu])([uimnpt]?\d)$', r'\1\2\2\3'],
        ]
class Mandarin(_SplitCharacter):
    def _set_subclass_variables(self):
        self.name = 'Mandarin'
        self.replacements = [
            [r'yan(\d)', r'yän\1'], 
            [r'([jxqy][iu])an(\d)', r'\1än\2'], 
            # u is different after jxqy
            [r'([jxqy])u', r'\1ü'], 
            ['v', 'ü'], 
        ]

class SplitColumn:
    def __init__(self, column, splitter_class):
        self.dict_list = []
        self.column = column
        self.splitter_class = splitter_class
    def _set_subclass_variables(self):
        pass
    def _run_character(self):
        self.splitter = self.splitter_class(character = self.character)
        self.dict_list.append(self.splitter.main())
    def _make_df(self):
        '''
        append none creates nan
        append character creates '' when item is missing
        I want to make then both into ' '
        '''
        self.df = pd.DataFrame(self.dict_list).replace('', ' ').fillna(' ')
    def main(self):
        self._set_subclass_variables()
        for self.character in self.column.values:
            self._run_character()
        self._make_df()

class Manager:
    def _make_pinyin(self):
        self.df_input = pd.read_csv('files_resource/hanzi_db.csv')[['character']]
        self.df_input['Cantonese'] = self.df_input.character.map(lambda char: jyutping.get(char)[0])
        self.df_input['Mandarin'] = self.df_input.character.map(lambda char: pinyin.get(char, format = 'numerical'))
        # Reset so indices line up when concatenating with other dfs
        self.df_input = self.df_input.dropna().reset_index(drop = True)
    def _split_pinyin(self):
        self.split_j = SplitColumn(column = self.df_input.Cantonese, splitter_class = Cantonese)
        self.split_j.main()
        self.split_p = SplitColumn(column = self.df_input.Mandarin, splitter_class = Mandarin)
        self.split_p.main()
    def _make_df(self):
        self.df = pd.concat([self.df_input, self.split_j.df, self.split_p.df], axis = 1)
    def _write_df(self):
        self.df.to_csv('files_output/pinyin.csv', index = False)
    def main(self):
        self._make_pinyin()
        self._split_pinyin()
        self._make_df()
        self._write_df()

if __name__=='__main__':
    manager = Manager()
    manager.main()