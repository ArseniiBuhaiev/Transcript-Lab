import re
from .config import *
from ukrainian_word_stress import Stressifier

stressify = Stressifier(stress_symbol='\u0301')

text = 'Акомодація — якісна контактна регресивна чи прогресивна зміна; пристосування голосного до приголосного, або навпаки (в українській мові такі випадки рідші).'

pauses_dict = {
    "\"": "",
    " '": "",
    "' ": "",
    ",": " /",
    "(": "/ ",
    ")": " /",
    "—": "/",
    " - ": " / ",
    ".": " //",
    ";": " //",
    "!": " //",
    "?": " //"
}

def stress(tokens: list) -> list:
    for token in tokens:
        token_csfld = token.casefold()
        
        if '%' in token_csfld:
            return re.sub(r"%", "\u0301", token_csfld)
        else:
            tokens[tokens.index(token)] = stressify(token_csfld)

    return tokens

def punctuation_to_pauses(text: str) -> str:
    def replace_match(match):
        char = pauses_dict[match.group(1)]
        return char
    
    pauses = re.sub(r"(\"|\s'|'\s|,|\(|\)|—|\s\-\s|\.|;|!|\?)", replace_match, text)
    
    return pauses

def tokenize_phonetic_words(text: str) -> list:
    text = re.sub(r"(?<!\s)-(?!\s)", " ", punctuation_to_pauses(stressify(text.lower().strip())))

    token_list = text.split(" ")

    while "/" in token_list[-1]:
        token_list.pop(-1)

    for i, token in enumerate(token_list):
        syllables = sum(1 for ch in token if ch in vowels)
        try:
            if syllables < 2 and '/' not in token and '/' not in token_list[i+1] and sum(1 for ch in token_list[i+1] if ch in vowels) >= 2:
                token_list[i+1] = token + token_list[i+1]
                token_list.pop(i)
            elif syllables <2 and '/' not in token and sum(1 for ch in token_list[i+1] if ch in vowels) < 2:
                token_list[i+1] = re.sub(r"([ауоеіиїєяю])", lambda match: f"{match.group(1)}\u0301", token_list[i+1])
                token_list[i+1] = token + token_list[i+1]
                token_list.pop(i)
            elif syllables < 2 and '/' in token_list[i+1] or syllables < 2 and i == len(token_list) - 1:
                token_list[i] = re.sub(r"([ауоеіиїєяю])", lambda match: f"{match.group(1)}\u0301", token_list[i])
        except IndexError:
            pass

    return token_list

print(tokenize_phonetic_words("То що?"))