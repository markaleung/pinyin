# pinyin
Tools for Chinese Pinyin

# Annotate Chinese Texts with Pinyin

## How to Install
- Install python
- `pip install -r requirements.txt'

## How to Run
- Run Jupyter
    - notebooks/Notebook Pinyin.ipynb
- Run Streamlit web app
    - `streamlit run streamlit_app.py` to run locally
    - [pinyin.streamlit.app](pinyin.streamlit.app) to use cloud version

## Module Tree
- MultiFile: Run all files in folder
    - OneFile: Add translation to each line in file
        - OneLine: Translate each character in line
            - OneChar: Translate 1 character
                - MultiplePronunciation: merge multiple pronunciations of a character (Cantonese only)

## Class Tree
- OneText: read text from config
    - OneFile: read file to config text, write output to file
- OneChar
    - Cantonese: use jyutping, call MultiplePronunciation
    - Mandarin: use pinyin
