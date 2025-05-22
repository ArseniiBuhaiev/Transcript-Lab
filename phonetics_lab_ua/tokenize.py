import re
from .config import *
from ukrainian_word_stress import Stressifier

stressify = Stressifier(stress_symbol='\u0301')

def missing_stress(tokens: list) -> list:
    for token in tokens:
        if '\u0301' in token:
            pass
        if '%' in token:
            return re.sub(r"%", "\u0301", token)
        elif sum(1 for ch in token if ch in vowels) == 1:
            tokens[tokens.index(token)] = re.sub(r"([ауоеіиїєяю])", lambda match: f"{match.group(1)}\u0301", token)

    return tokens

def punctuation_to_pauses(text: str) -> str:
    def replace_match(match):
        char = pauses_map[match.group(1)]
        return char
    
    pauses = re.sub(r"(\"|\s'|'\s|,|\(|\[|\)|\]|—|\s\-\s|\.|;|!|\?)", replace_match, text)
    
    return pauses

def tokenize_phonetic_words(text: str) -> list:
    text = re.sub(r"(?<!\s)-(?!\s)", " ", punctuation_to_pauses(stressify(text.lower().strip())))

    token_list = missing_stress(text.split(" "))

    while "|" in token_list[-1]:
        token_list.pop(-1)
    while "|" in token_list[0]:
        token_list.pop(0)

    return token_list