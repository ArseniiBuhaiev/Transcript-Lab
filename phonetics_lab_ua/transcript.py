import re
from .config import *
from .tokenize import *

def jotted_letters(word: str) -> str:
  """
  Трансформує йотовані літери у звуки, які вони позначають.\n
  Transforms jotted letters into sounds, which they denote.

  Args:
    word (str): Word with jotted letters

  Returns:
    str: Word with jotted letters transformed to sounds
  """  
  def two_sounds(match):
    preposition = match.group(1)
    if preposition == "'":
      preposition = ''
    else:
      pass
    jotted = match.group(2)
    result = f"{preposition}j{jotted_map[jotted]}"
    return result
  def one_sound(match):
    preposition = match.group(1)
    jotted = match.group(2)
    if preposition in half_palatalized:
      result = f"{preposition}ߴ{jotted_map[jotted]}"
    else:
      result = f"{preposition}\'{jotted_map[jotted]}"
    return result
  
  result = re.sub(r"й", "j", word)

  while bool(re.findall("[яюєї]", result)):
    to_sound = re.sub(r"([ауоеіиїєяюьj']\u0301?|\b)([яюєї])", two_sounds, result)
    result = re.sub(r"([цкнгшзхфвпрлджчсмтбґj])([яюєї])", one_sound, to_sound)
  
  return result

def vocalised_consonants(word: str) -> str:
  """
  Позначає вокалізацію [в] та [j] після голосного/на початку слова перед приголосним/у кінці слова.\n
  Marks vocalisation of [в] and [j] after vowel/at the start of the word before the consonant/at the end of the word.

  Args:
    word (str): Word with [в] and/or [j] sounds

  Returns:
    str: Word with vocalized consonants
  """
  def replace(match):
    vowel = match.group(1)
    target = match.group(2)
    consonant = match.group(3)
    
    result = f"{vowel}{vocalized_map[target]}{consonant}"
    return result
  
  result = re.sub(r"([ауоеіиїєяю]\u0301?|\b)([вj])([цкнгшзхфвпрлджчсмтбґj]|\b)", replace, word)

  return result

def nasalisation(word: str) -> str:
  """
  Позначає назалізацію голосних в оточенні носових приголосних.\n
  Marks nasalisation of vowels in a nasal consonants surrounding.

  Args:
    word (str): Word with vowels in a nasal consonants surrounding

  Returns:
    str: Word with marked nasalisation
  """
  def replace_match(match):
    preposition = match.group(1)
    stress = match.group(2)
    nasal = match.group(3)
    postposition = match.group(4)
    try:
      result = f"{nasalized_map[preposition]}{stress}{nasal}{nasalized_map[postposition]}"
      return result
    except:
      return f"{preposition}{stress}{nasal}{postposition}"

  nasalisation = re.sub(r"([аоуеіи]?)(\u0301?)([нм]'?)([аоуеіи]?)", replace_match, word)
  
  return nasalisation

def letters_to_sounds(word: str) -> str:
  """
  Трансформує Щ, ДЖ, та ДЗ у відповідні звуки.\n
  Transforms Щ, ДЖ and ДЗ into corresponding sounds.

  Args:
    word (str): Word with Щ and/or ДЖ and/or ДЗ

  Returns:
    str: Word with Щ, ДЖ, ДЗ transformed to sounds
  """
  def replace(match):
    letter = match.group(1)
    result = conversion_map[letter]
    return result
  
  convert = re.sub(r"(щ|дж|дз)", replace, word)
  
  return convert

def palatalisation(word: str) -> str:
  """
  Позначає (напів-)палаталізацію приголосних.\n
  Marks (half)palatalised consonants.

  Args:
    word (str): Word with palatalised consonants

  Returns:
    str: Word with marked palatalised consonants
  """
  def replace_soft(match):
    target = match.group(1)
    postposition = match.group(2)
    if postposition == "ь":
      result = f"{target}'"
    else:
      result = f"{target}'{postposition}"
    return result
  def replace_half_soft(match):
    target = match.group(1)
    postposition = match.group(2)
    if postposition == "ь":
      result = f"{target}ߴ"
    else:
      result = f"{target}ߴ{postposition}"
    return result

  palatalize = re.sub(r"([дтзсцлнр])([ьіĩ])", replace_soft, word)
  half_palatalize = re.sub(r"([бпвмфґгкхшчж])([ьіĩ])", replace_half_soft, palatalize)

  return half_palatalize

def labialisation(word: str) -> str:
  """
  Позначає лабіалізацію приголосних.\n
  Marks labialised consonants.

  Args:
    word (str): Word with labialised consonants

  Returns:
    str: Word with marked labialised consonants
  """
  def replace(match):
    target = match.group(1)
    palatalisation = match.group(2)
    postposition = match.group(3)
    result = f"{target}{palatalisation}°{postposition}"
    return result

  result = re.sub(r"([бпвмфґкхшчжгдтзсцлнрj])(['ߴ]?)([оõуỹ])", replace, word)

  return result

def sound_lengthening(word: str) -> str:
  """
  Позначає подовження приголосних.\n
  Marks consonant lenghthening.

  Args:
    word (str): Word with legthened consonants

  Returns:
    str: Word with marked legthened consonants
  """
  def replace(match):
    target = match.group(1)
    postposition = match.group(2)
    result = f"{target[:len(target)//2]}{postposition}:"
    return result

  lengthening = re.sub(r"(бб|пп|вв|мм|фф|ґґ|кк|хх|шш|чч|(?<!д͡)жж|гг|д'?д|т'?т|(?<!д͡)з'?з|с'?с|ц'?ц|л'?л|н'?н|рр|jj|д͡жд͡ж|д͡зд͡з)([ߴ'°]*)", replace, word)

  return lengthening

def i_type_articulation(word: str) -> str:
  """
  Позначає зміну артикуляції голосних на і-подібну.\n
  Marks change of the vowels articulation to that, similar of [і].

  Args:
    word (str): Word with legthened consonants

  Returns:
    str: Word with marked legthened consonants
  """
  def replace_regressive(match):
    target = match.group(1)
    stress = match.group(2)
    postposition = match.group(3)
    result = f"{target}{stress}·{postposition}"
    return result
  def replace_progressive(match):
    target = match.group(2)
    preposition = match.group(1)
    result = f"{preposition}·{target}"
    return result

  regressive = re.sub(r"([аоуеãõỹẽ])(\u0301?)(j|\w'|д͡з')", replace_regressive, word)
  progressive = re.sub(r"([j'][:°]*)([аоуеãõỹẽ])", replace_progressive, regressive)

  return progressive

def vowels_reduction(word: str) -> str:
  """
  Позначає редукцію ненаголошених голосних.\n
  Marks unstressed vowels reduction.

  Args:
    word (str): Word with unstressed vowels

  Returns:
    str: Word with marked unstressed vowels reduction
  """
  def e_to_y(match):
    target = match.group(1)
    result = f"{target}ᴻ"
    return result
  def e_to_i(match):
    target = match.group(1)
    result = f"·{target}ⁱ·"
    return result
  def y_to_e(match):
    target = match.group(1)
    result = f"{target}ᵉ"
    return result
  
  reduction = re.sub(r"([еẽ](?!\u0301))", e_to_y, word)
  reduction = re.sub(r"·([еẽ])ᴻ·", e_to_i, reduction)
  reduction = re.sub(r"([иũ])(?!\u0301)", y_to_e, reduction)

  return reduction

def o_assimilation(word: str) -> str:
  """
  Позначає гармонійну асиміляцію [о].\n
  Marks harmonic assimilation of [o].

  Args:
    word (str): Word with [o]

  Returns:
    str: Word with marked harmonic assimilation
  """
  def replace(match):
    target = match.group(1)
    postposition = match.group(2)
    result = f"{target}ʸ{postposition}"
    return result

  result = re.sub(r"([оõ])((?:[^аоуеиі]*)(?:[уі]\u0301))", replace, word)

  return result

def voice_assimilation(word: str) -> str:
  """
  Асимілює приголосні за дзвінкістю.\n
  Assimilates consonants by voice.

  Args:
    word (str): Word with consonant assimilation by voice

  Returns:
    str: Word with consonants assimilated
  """
  def replace_match(match):
    voiceless = match.group(1)
    palatalisation = match.group(2)
    voiced = match.group(3)
    result = f"{voice_assimilation_map[voiceless]}{palatalisation}{voiced}"

    return result
  
  result = re.sub(r"([цкшхпчст])('?)([гзджбґ])", replace_match, word)

  return result

def voicelessness_assimilation(word: str) -> str:
  """
  Асимілює приголосні за глухістю.\n
  Assimilates consonants by voicelessness.

  Args:
    word (str): Word with consonant assimilation by voicelessness

  Returns:
    str: Word with consonants assimilated
  """
  def replace_match(match):
    voiceless = match.group(2)
    return "с" + voiceless

  def exceptions(match):
    preposition = match.group(1)
    stress = match.group(2)
    postposition = match.group(3)

    return f'{preposition}{stress}х{postposition}'
  
  is_exception = re.sub(r"(ле|в°?о|(?:кߴі|н'[ĩі])|д'°?о)(\u0301?)г(к|т)", exceptions, word)
  obligatory = re.sub(r"^(з)([цкшхфпчст])", replace_match, is_exception)

  return obligatory

def WOP_assimilation(word: str) -> str:
  """
  Асимілює приголосні за місцем творення, стягує за потреби.\n
  Assimilates consonants by the way of its production; contracts them if needed.

  Args:
    word (str): Word with consonant assimilation by the way of production

  Returns:
    str: Word with consonants assimilated
  """
  def replace_regressive(match):
    target = match.group(1)
    misc = match.group(2)
    assimilator = match.group(3)
    result = WOP_assimilation_map[target] + misc + assimilator
    
    return result
  
  in_verbs = re.sub(r"т'с'а$", "ц':а", word)
  regressive = re.sub(r"([дт])('?)([зсц]|д͡з)", replace_regressive, in_verbs)
  progressive_in_non_verbs = re.sub(r"цс'", "ц'", regressive)

  return progressive_in_non_verbs

def POPWOP_assimilation(word: str) -> str:
  """
  Асимілює приголосні за місцем та способом творення.\n
  Assimilates consonants by the place and the way of its production.

  Args:
    word (str): Word with consonant assimilation by the place and the way of its production

  Returns:
    str: Word with consonants assimilated
  """
  def replace_match(match):
    target = match.group(1)
    misc = match.group(2)
    assimilator = match.group(3)
    result = POPWOP_assimilation_map[target] + misc + assimilator
    
    return result

  step1 = re.sub(r"([дт])('?)([жшч]|д͡ж)", replace_match, word)
  step2 = re.sub(r"([зсц]|д͡з)('?)([жшч]|д͡ж)", replace_match, step1)
  step3 = re.sub(r"([жшч]|д͡ж)('?)([зсц]|д͡з)", replace_match, step2)

  return step3

def softness_assimilation(word: str) -> str:
  """
  Асимілює приголосні за м'якістю.\n
  Assimilates consonants by softness.

  Args:
    word (str): Word with consonant assimilation by softness

  Returns:
    str: Word with consonants assimilated
  """
  def replace_match(match):
    target = match.group(1)
    palatalized = match.group(2)
    result = f"{target}'{palatalized}'"

    return result

  result = word

  while re.findall(r"([дтнлзсц]|д͡з)([дтнлзсц]|д͡з)'", result):
    result = re.sub(r"([дтнлзсц]|д͡з)([дтнлзсц]|д͡з)'", replace_match, result)
  
  return result

def consonant_reduction(word: str) -> str:
  """
  Спрощує приголосні у групах приголосних, стягує за потреби.\n
  Reducts the consonants in consonant groups; contracts them if needed.

  Args:
    word (str): Word with consonant assimilation by softness

  Returns:
    str: Word with consonants assimilated
  """
  def obligatory_replace(match):
    prev = match.group(1)
    next = match.group(2)
    
    result = f'{prev}{next}'

    return result

  if re.findall(r'запj·а́стн|хвастн', word):
    return word
  else:
    reduction = re.sub(r"(с|н)т(ч|ц'|н|д|с)", obligatory_replace, word)
    result = reduction
    if reduction != word and word != 'шߴістсо́т':
      contraction = re.sub(r"сс", "с", reduction)
      if contraction != reduction:
        result = contraction

    return result

def check_input(word: str) -> str:
  """
  Перевіряє вхідні дані на недозволені символи, очищує від зайвих символів, приводить до нижнього регістру.\n
  Checks the input for forbidden characters, cleans it up and lowercases it.

  Args:
    word (str): Word

  Returns:
    str: Clean, lowercased word with a marked stressed vowel
  """
  word_cleared = re.sub(r"(\w\-\w)", lambda match: (match.group(1)).replace("-", ""), (word.strip()).casefold())
  char_check = re.findall(r"[qwertyuiopasdfghjklzxcvbnm+=\$№#@\"&]", word_cleared)
  if char_check:
    return f"ПОМИЛКА: Виявлено невідомі символи у слові {word_cleared}"
  for i, char in enumerate(word_cleared):
    if char == "%" and word_cleared[i-1] not in vowels:
      return f"ПОМИЛКА: У слові {word_cleared} приголосний позначено як наголошений"
  else:
    return word_cleared

def phonetic(word: str) -> str:
  """
  Фонетично транскрибує слово за набором правил.\n
  Phonetically transcribes the word following a rule-set.

  Args:
    word (str): Orthographically written word

  Returns:
    str: Phonetic transcription of the word
  """
  word = check_input(word)
  if 'ПОМИЛКА' in word:
    return word
  elif word == "":
    return ""
  
  transformations = (
    jotted_letters,
    vocalised_consonants,
    nasalisation,
    letters_to_sounds,
    palatalisation,
    consonant_reduction,
    labialisation,
    voice_assimilation,
    voicelessness_assimilation,
    WOP_assimilation,
    POPWOP_assimilation,
    softness_assimilation,
    sound_lengthening,
    i_type_articulation,
    o_assimilation,
    vowels_reduction
  )

  for transformation in transformations:
    word = transformation(word)

  result = word.replace('ũ', 'и\u0303').replace('і\u0301', 'í')
  return f'{result}'

def phonetic_text(text: str) -> str:
    transcription = ""
    token_list = tokenize_phonetic_words(text)
    for token in token_list:
        transcription += phonetic(token) + " "
    return f"[{transcription[:-1]}]"

def phonematic(word: str) -> str:
  """
  Фонематично транскрибує слово за набором правил.\n
  Phonematically transcribes the word following a rule-set.

  Args:
    word (str): Orthographically written word

  Returns:
    str: Phonematic transcription of the word
  """
  word = check_input(word)
  if 'ПОМИЛКА' in word:
    return word
  elif word == "":
    return ""

  transformations = (
    jotted_letters,
    vocalised_consonants,
    letters_to_sounds,
    palatalisation,
    consonant_reduction,
    voice_assimilation,
    voicelessness_assimilation,
    WOP_assimilation,
    POPWOP_assimilation,
    softness_assimilation,
    sound_lengthening,
    o_assimilation,
    i_type_articulation,
    vowels_reduction
  )

  for transformation in transformations:
    word = transformation(word)

  result = word.replace('j', 'й').replace('·', '')
  return f'{result}'
  
def phonematic_text(text: str) -> str:
    transcription = ""
    token_list = tokenize_phonetic_words(text)
    for token in token_list:
        transcription += phonematic(token) + " "
    return f"/{transcription[:-1]}/"