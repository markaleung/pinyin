import jyutping, re, os, pinyin, tqdm

class Config:
    def __init__(self):
        self.newline = '\n'
        self.split_text_on_punctuation = True
        self.cantonese_multiple_pronunciation = True
        self.chinese_punctuation = r'([，。？])'
        self.yale_filters = (('oe', 'eu'), ('eo', 'eu'), ('j', 'y'), ('z', 'j'), ('c', 'ch'), ('yy', 'y'))
        # line, char, character_is_chinese is auto added
        # language, folder, filename, text must be added

class MultiplePronunciation:
    def __init__(self, config_):
        self.config = config_
        self.option_dict = {}
    def _parse_option(self):
        self.start, self.tone = re.search(r'^([a-z]+)([0-9]$)', self.option).groups()
        if self.start not in self.option_dict:
            self.option_dict[self.start] = []
        self.option_dict[self.start].append(self.tone)
    def _join_options(self):
        self.option_dict[self.start] = ''.join(sorted(self.option_dict[self.start]))
    def _make_output(self):
        self.output = ''.join([start+tone for start, tone in sorted(self.option_dict.items())])
        if len(self.option_dict) > 1:
            self.output = f'({self.output})'
    def main(self):
        for self.option in self.config.char_options:
            self._parse_option()
        for self.start in self.option_dict:
            self._join_options()
        if len(self.option_dict) > 0:
            self._make_output()
        else: # Invalid character is empty set
            self.output = self.config.char
        return self.output

class OneChar:
    def __init__(self, config_):
        self.config = config_
    def _translate(self):
        pass
    def _after_translate(self):
        self.output = ' ' + self.output
        self.config.character_is_chinese = True
    def _no_translate(self):
        self.spacer = ' ' if self.config.character_is_chinese is True else ''
        self.output = self.spacer + self.config.char
        self.config.character_is_chinese = False
    def main(self):
        # Detect Chinese characters
        if re.search(u'[\u4e00-\u9fff]', self.config.char):
            self._translate()
            self._after_translate()
        else:
            self._no_translate()
        return self.output
class Cantonese(OneChar):
    def _translate(self):
        self.output = jyutping.get(self.config.char, multiple = self.config.cantonese_multiple_pronunciation)[0]
        # All output is sets
        if self.config.cantonese_multiple_pronunciation:
            self.config.char_options = self.output
            self.multiple = MultiplePronunciation(config_ = self.config)
            self.output = self.multiple.main()
        elif self.output is None:
            self.output = self.config.char
class Yale(Cantonese):
    def _translate(self):
        super()._translate()
        if self.output is not None:
            for self.old, self.new in self.config.yale_filters:
                self.output = self.output.replace(self.old, self.new)
class Mandarin(OneChar):
    def _translate(self):
        self.output = pinyin.get(self.config.char, format = 'numerical')

class OneLine:
    def __init__(self, config_):
        self.config = config_
        self.chars = []
    def _translate(self):
        self.one_char = CLASSES[self.config.language](config_ = self.config)
        self.chars.append(self.one_char.main())
    def _make_output(self):
        self.translation = ''.join(self.chars)
        # Only print original line if chinese characters have been translated
        if self.translation != self.config.line:
            self.output = f'{self.translation}{self.config.newline}{self.config.line}'
        else:
            self.output = self.translation
    def main(self):
        '''
        Must reset for every line
        Otherwise, if the previous line ends with a Chinese character
        And the next line has no Chinese characters
        A space will be inserted at the beginning
        i.e. 'abc' becomes ' abc'
        And the program will print it twice
        Because the line has changed
        '''
        self.config.character_is_chinese = False
        for self.config.char in self.config.line:
            self._translate()
        self._make_output()
        return self.output

class OneText:
    def __init__(self):
        self.config = Config()
        self.lines = []
    def _split_text(self):
        if self.config.split_text_on_punctuation:
            self.config.text = re.sub(self.config.chinese_punctuation, r'\1\n', self.config.text)
    def _run_line(self):
        self.one_line = OneLine(config_ = self.config)
        self.lines.append(self.one_line.main())
    def _make_output(self):
        self.output = self.config.newline.join(self.lines)
    def main(self):
        self._split_text()
        for self.config.line in self.config.text.split('\n'):
            self._run_line()
        self._make_output()
        return self.output
class OneFile(OneText):
    def __init__(self, config_):
        self.config = config_
        self.lines = []
    def _read_file(self):
        with open(f'{self.config.folder_input}/{self.config.filename}') as file:
            self.config.text = file.read()
        if 'cantonese.txt' in self.config.filename:
            self.config.language = 'cantonese'
        elif 'mandarin.txt' in self.config.filename:
            self.config.language = 'mandarin'
        else:
            raise ValueError("filename doesn't contain cantonese or mandarin")
    def _write_file(self):
        self.filename_output = self.config.filename.replace(self.config.language, MAPPING[self.config.language])
        with open(f'{self.config.folder_output}/{self.filename_output}', 'w') as file:
            file.write(self.output)
    def main(self):
        self._read_file()
        super().main()
        self._write_file()

class MultiFile:
    def __init__(self):
        self.config = Config()
    def _run_file(self):
        self.one_file = OneFile(config_ = self.config)
        self.one_file.main()
    def main(self):
        for self.config.filename in tqdm.tqdm(os.listdir(self.config.folder_input)):
            if re.search(r'(mandarin|cantonese).txt$', self.config.filename):
                self._run_file()

CLASSES = {
    'cantonese': Cantonese, 
    'cantonese yale': Yale, 
    'mandarin': Mandarin
}
MAPPING = {
    'cantonese': 'jyutping', 
    'cantonese yale': 'yale', 
    'mandarin': 'pinyin', 
}