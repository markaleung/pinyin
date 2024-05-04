import jyutping, re, os, pinyin, tqdm

class Config:
    def __init__(self):
        self.newline = '\n'
        self.split_text_on_punctuation = True
        self.cantonese_multiple_pronunciation = True
        self.chinese_punctuation = r'([，。？])'
        # language, folder, filename, text, line, char must be added

class OneChar:
    def __init__(self, config_):
        self.config = config_
    def _translate(self):
        pass
    def main(self):
        # Detect Chinese characters
        if re.search(u'[\u4e00-\u9fff]', self.config.char):
            self._translate()
            return self.output + ' '
        else:
            return self.config.char
class Cantonese(OneChar):
    def _translate(self):
        self.output = jyutping.get(self.config.char, multiple = self.config.cantonese_multiple_pronunciation)[0]
        if self.config.cantonese_multiple_pronunciation:
            # Invalid character is empty set
            if len(self.output) == 0:
                self.output = self.config.char
            elif len(self.output) > 1:
                self.output = f'({"".join(self.output)})'
            # Even single pronunciation is a set
            elif len(self.output) == 1:
                self.output = list(self.output)[0]
        else:
            # No sets for single pronunciation
            if self.output is None:
                self.output = self.config.char
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
    'mandarin': Mandarin
}
MAPPING = {
    'cantonese': 'jyutping', 
    'mandarin': 'pinyin', 
}