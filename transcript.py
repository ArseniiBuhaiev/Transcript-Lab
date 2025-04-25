import re
from config import *
from ukrainian_word_stress import Stressifier

stressify = Stressifier(stress_symbol='\u0301')

# Функція наголосу
def stress(word: str) -> str:
  vowel_count = 0
  for char in word:
    if char in vowels:
      vowel_count += 1
  
  if '%' in word:
    return re.sub(r"%", "\u0301", word)
  elif vowel_count == 1:
    for char in word:
      if char in vowels:
        return word.replace(char, f'{char}\u0301')
  else:
    return stressify(word)

# Функція заміни йотованих літер на відповідні звуки
def jotted_letters(word: str) -> str:
  def two_sounds(match):
    prev_symb = match.group(1)
    if prev_symb == "'":
      prev_symb = ''
    else:
      pass
    jotted = match.group(2)
    result = f"{prev_symb}j{jotted_map[jotted]}"
    return result
  def one_sound(match):
    prev_symb = match.group(1)
    jotted = match.group(2)
    if prev_symb in half_palatalized:
      result = f"{prev_symb}ߴ{jotted_map[jotted]}"
    else:
      result = f"{prev_symb}\'{jotted_map[jotted]}"
    return result
  
  result = re.sub(r"й", "j", word)

  while bool(re.findall("[яюєї]", result)):
    step_one = re.sub(r"([ауоеіиїєяю']\u0301?|\b)([яюєї])", two_sounds, result)
    result = re.sub(r"([цкнгшзхфвпрлджчсмтбґй])([яюєї])", one_sound, step_one)

  return result

# Функція заміни "в" та "й" на відповідні вокалізовані приголосні
def vocalized_consonants(word: str) -> str:
  def replace(match):
    vowel = match.group(1)
    target = match.group(2)
    consonant = match.group(3)
    
    result = f"{vowel}{vocalized_map[target]}{consonant}"
    return result
  
  result = re.sub(r"([ауоеіиїєяю']\u0301?|\b)([вj])([цкнгшзхфвпрлджчсмтбґj]|\b)", replace, word)

  return result

# Функція назалізації голосного
def nasalisation(word: str) -> str:
  def replace_one(match):
    prev_symb = match.group(1)
    target = match.group(2)
    result = f"{prev_symb}{nasalized_map[target]}"
    return result
  
  def replace_two(match):
    target = match.group(1)
    stress = match.group(2)
    next_symb = match.group(3)
    result = f"{nasalized_map[target]}{stress}{next_symb}"
    return result

  step_one = re.sub(r"([нм]'?)([аоуеіи])", replace_one, word)
  step_two = re.sub(r"([аоуеіи])(\u0301?)([нм])", replace_two, step_one)

  return step_two

# Функція Щ, дж, дз
def shch(word: str) -> str:
  shch = re.sub(r"щ", "шч", word)
  dzh = re.sub(r"дж", "д͡ж", shch)
  dz = re.sub(r"дз", "д͡з", dzh)

  return dz

# Функція палаталізації приголосного
def palatalisation(word: str) -> str:
  def replace_soft(match):
    target = match.group(1)
    next_symb = match.group(2)
    if next_symb == "ь":
      result = f"{target}'"
    else:
      result = f"{target}'{next_symb}"
    return result
  def replace_half_soft(match):
    target = match.group(1)
    next_symb = match.group(2)
    if next_symb == "ь":
      result = f"{target}ߴ"
    else:
      result = f"{target}ߴ{next_symb}"
    return result

  palatalize = re.sub(r"([дтзсцлнр])([ьіĩ])", replace_soft, word)
  half_palatalize = re.sub(r"([бпвмфґгкхшчж])([ьіĩ])", replace_half_soft, palatalize)

  return half_palatalize

# Функція додавання огублення звуків
def labialisation(word: str) -> str:
  def replace(match):
    target = match.group(1)
    palatalisation = match.group(2)
    next_symb = match.group(3)
    result = f"{target}{palatalisation}°{next_symb}"
    return result

  result = re.sub(r"([бпвмфґкхшчжгдтзсцлнр])(['ߴ]?)([оõуỹ])", replace, word)

  return result

# Функція додавання знака подовження
def sound_lengthening(word: str) -> str:
  def replace(match):
    target = match.group(1)
    next_symb = match.group(2)
    result = f"{target[:len(target)//2]}{next_symb}:"
    return result
  
  def replace_contraction(match):
    target = match.group(1)
    next_symb = match.group(2)

    if next_symb == 'а':
      result = target + next_symb
    else:
      result = 'ц\'' + next_symb

    return result

  lengthening = re.sub(r"(б[ߴ°]?б|п[ߴ°]?п|в[ߴ°]?в|м[ߴ°]?м|ф[ߴ°]?ф|ґ[ߴ°]?ґ|к[ߴ°]?к|х[ߴ°]?х|ш[ߴ°]?ш|ч[ߴ°]?ч|(?<!д͡)ж[ߴ°]?ж|г[ߴ°]?г|д['°]?д|т['°]?т|(?<!д͡)з['°]?з|с['°]?с|ц['°]?ц|л['°]?л|н['°]?н|р['°]?р|д͡ж[ߴ°]?д͡ж|д͡з['°]?д͡з)([ߴ'°]*)", replace, word)
  contraction = re.sub(r"(ц':)(.)", replace_contraction, lengthening)

  return contraction

# Функція додавання знака і-подібної артикуляції
def i_type_articulation(word: str) -> str:
  def replace_regressive(match):
    target = match.group(1)
    stress = match.group(2)
    next_symb = match.group(3)
    result = f"{target}{stress}·{next_symb}"
    return result
  def replace_progressive(match):
    target = match.group(2)
    prev_symb = match.group(1)
    result = f"{prev_symb}·{target}"
    return result

  regressive = re.sub(r"([аоуеãõỹẽ])(\u0301?)(j|\w'|д͡з')", replace_regressive, word)
  progressive = re.sub(r"([j'][:°]*)([аоуеãõỹẽ])", replace_progressive, regressive)

  return progressive

# Функція редукції ненаголошених
def vowels_reduction(word: str) -> str:
  def replace(match):
    target = match.group(1)
    nasalisation = match.group(2)
    next_symb = match.group(3)
    result = f"{target}{nasalisation}{reduction_map[target]}{next_symb}"
    return result

  result = re.sub(r"([еẽи])(\u0303?)([аоуеиіãõỹẽиĩбпвўмфґкхшчжгдтзсцлнрjĭ·])", replace, word)

  return result

# Функція наближення о до у
def o_assimilation(word: str) -> str:
  def replace(match):
    target = match.group(1)
    next_symb = match.group(2)
    result = f"{target}ʸ{next_symb}"
    return result

  result = re.sub(r"(о)((?:[^аоуеиі]+)(?:[уі]\u0301))", replace, word)

  return result

# Функція асиміляції за дзвінкістю
def voice_assimilation(word: str) -> str:
  def replace_match(match):
    voiceless = match.group(1)
    voiced = match.group(2)
    result = voice_assimilation_map[voiceless] + voiced

    return result

  return re.sub(r"([цкшхфпчст])([гзджбґ]|д͡з|д͡ж)", replace_match, word)

# Функція обов'язкової асиміляції за глухістю
def voicelessness_assimilation(word: str) -> str:
  def replace_match(match):
    voiceless = match.group(2)
    return "с" + voiceless

  def exceptions(match):
    preposition = match.group(1)
    stress = match.group(2)
    postposition = match.group(3)

    return f'{preposition}{stress}х{postposition}'
  
  is_exception = re.sub(r"(ле|в°о|(?:кߴ|н')і|д'°о)(\u0301?)г(к|т)", exceptions, word)
  obligatory = re.sub(r"(\bз)([цкшхфпчст])", replace_match, is_exception)
  
  return obligatory

# Функція асиміляції за способом творення
def WOP_assimilation(word: str) -> str:
  def replace_regressive(match):
    target = match.group(1)
    misc = match.group(2)
    assimilator = match.group(3)
    result = WOP_assimilation_map[target] + misc + assimilator
    
    return result
  
  def replace_progressive(match):
    assimilator = match.group(1)
    misc = match.group(2)

    result = assimilator + misc + "ц"
    
    return result

  regressive = re.sub(r"([дт])('?)([зсц]|д͡з)", replace_regressive, word)
  progressive = re.sub(r"(ц)('?)(с)", replace_progressive, regressive)

  return progressive

# Функція асиміляції за місцем та способом творення
def POPWOP_assimilation(word: str) -> str:
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

# Функція асиміляції за м'якістю
def softness_assimilation(word: str) -> str:
  def replace_match(match):
    target = match.group(1)
    palatalized = match.group(2)
    sign = match.group(3)
    result = f"{target}'{palatalized}{sign}"

    return result

  obligatory = re.sub(r"([дтн])([дтн])(['])", replace_match, word)
  optional = re.sub(r"([зсц])([цкнгґшзхфвпрлджчсмтб]|д͡з|д͡ж)(['ߴ])", replace_match, obligatory)
  
  return optional

def consonant_reduction(word: str, original: str) -> str:
  def obligatory_replace(match):
    prev = match.group(1)
    next = match.group(2)
    
    result = f'{prev}{next}'

    return result

  if re.findall(r'зап\'ястн|хвастн', original):
    return word
  else:
    return re.sub(r"(?:)(с|н)т(ч|ц'|н|д|с)", obligatory_replace, word)

# Функція транскрибування слова
def main_phonetic(word: str) -> str:
  word_cleared = ((word.strip()).casefold()).replace("-", "")
  char_check = re.findall(r"[qwertyuiopasdfghjklzxcvbnm,\.;!+=\$№#@\"&]", word_cleared)
  if char_check:
    return "ПОМИЛКА: Виявлено невідомі символи"
  elif " " in word_cleared:
    return "ПОМИЛКА: Було введено більше одного слова"
  for i, char in enumerate(word_cleared):
    if char == "!" and word_cleared[i-1] not in vowels:
      return "ПОМИЛКА: Приголосний позначено як наголошений"
  else:
    transcription = stress(word_cleared)
    transcription = jotted_letters(transcription)
    transcription = vocalized_consonants(transcription)
    transcription = nasalisation(transcription)
    transcription = shch(transcription)
    transcription = palatalisation(transcription)
    transcription = consonant_reduction(transcription, word_cleared)
    transcription = labialisation(transcription)
    transcription = voice_assimilation(transcription)
    transcription = voicelessness_assimilation(transcription)
    transcription = WOP_assimilation(transcription)
    transcription = POPWOP_assimilation(transcription)
    transcription = softness_assimilation(transcription)
    transcription = sound_lengthening(transcription)
    transcription = i_type_articulation(transcription)
    transcription = o_assimilation(transcription)
    transcription = vowels_reduction(transcription)

    if '\u0301' in transcription:
      result = f"[{transcription}]"
      return result
    else:
      return 'ПОМИЛКА: У слові не визначено наголос'
  
def main_phonematic(word: str) -> str:
  phonematic = main_phonetic(word)
  


  result = f"/{phonematic.replace('j', 'й')}/"
  return result