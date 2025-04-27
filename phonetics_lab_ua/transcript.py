import re
from .config import *
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
  global rules_used
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
    step_one = re.sub(r"([ауоеіиїєяюьj']\u0301?|\b)([яюєї])", two_sounds, result)
    result = re.sub(r"([цкнгшзхфвпрлджчсмтбґj])([яюєї])", one_sound, step_one)

  if result != word:
    rules_used.append('-Перетворення йотованих літер')

  return result

# Функція заміни "в" та "й" на відповідні вокалізовані приголосні
def vocalized_consonants(word: str) -> str:
  global rules_used
  def replace(match):
    vowel = match.group(1)
    target = match.group(2)
    consonant = match.group(3)
    
    result = f"{vowel}{vocalized_map[target]}{consonant}"
    return result
  
  result = re.sub(r"([ауоеіиїєяю']\u0301?|\b)([вj])([цкнгшзхфвпрлджчсмтбґj]|\b)", replace, word)
  
  if result != word:
    rules_used.append('-Вокалізація приголосних')

  return result

# Функція назалізації голосного
def nasalisation(word: str) -> str:
  global rules_used
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
  
  if nasalisation != word:
    rules_used.append('-Назалізація')
  
  return nasalisation

# Функція Щ, дж, дз
def letters_to_sounds(word: str) -> str:
  global rules_used
  shch = re.sub(r"щ", "шч", word)
  dzh = re.sub(r"дж", "д͡ж", shch)
  dz = re.sub(r"дз", "д͡з", dzh)

  if shch != word:
    rules_used.append('-Перетворення щ на [шч]')
  if dzh != word:
    rules_used.append('-Перетворення дж на [д͡ж]')
  if dz != word:
    rules_used.append('-Перетворення дз на [д͡з]')
  

  return dz

# Функція палаталізації приголосного
def palatalisation(word: str) -> str:
  global rules_used
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

  if palatalize != word:
    rules_used.append('-Палаталізація приголосних')
  if half_palatalize != word and half_palatalize != palatalize:
    rules_used.append('-Напівпалаталізація приголосних')

  return half_palatalize

# Функція додавання огублення звуків
def labialisation(word: str) -> str:
  global rules_used
  def replace(match):
    target = match.group(1)
    palatalisation = match.group(2)
    postposition = match.group(3)
    result = f"{target}{palatalisation}°{postposition}"
    return result

  result = re.sub(r"([бпвмфґкхшчжгдтзсцлнрj])(['ߴ]?)([оõуỹ])", replace, word)

  if result != word:
    rules_used.append('-Лабіалізація приголосних')

  return result

# Функція додавання знака подовження
def sound_lengthening(word: str) -> str:
  global rules_used
  def replace(match):
    target = match.group(1)
    postposition = match.group(2)
    result = f"{target[:len(target)//2]}{postposition}:"
    return result

  lengthening = re.sub(r"(б[ߴ°]?б|п[ߴ°]?п|в[ߴ°]?в|м[ߴ°]?м|ф[ߴ°]?ф|ґ[ߴ°]?ґ|к[ߴ°]?к|х[ߴ°]?х|ш[ߴ°]?ш|ч[ߴ°]?ч|(?<!д͡)ж[ߴ°]?ж|г[ߴ°]?г|д['°]?д|т['°]?т|(?<!д͡)з['°]?з|с['°]?с|ц['°]?ц|л['°]?л|н['°]?н|р['°]?р|j°?j|д͡ж[ߴ°]?д͡ж|д͡з['°]?д͡з)([ߴ'°]*)", replace, word)

  if lengthening != word:
    rules_used.append('-Подовження приголосних')

  return lengthening

# Функція додавання знака і-подібної артикуляції
def i_type_articulation(word: str) -> str:
  global rules_used
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

  if regressive != word or progressive != word:
    rules_used.append('-і-подібна артикуляція голосних')

  return progressive

# Функція редукції ненаголошених
def vowels_reduction(word: str) -> str:
  global rules_used
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

  if reduction != word:
    rules_used.append('-Редукція ненаголошених голосних')

  return reduction

# Функція наближення о до у
def o_assimilation(word: str) -> str:
  global rules_used
  def replace(match):
    target = match.group(1)
    postposition = match.group(2)
    result = f"{target}ʸ{postposition}"
    return result

  result = re.sub(r"([оõ])((?:[^аоуеиі]+)(?:[уі]\u0301))", replace, word)

  if result != word:
    rules_used.append('-Гармонійна асиміляція')

  return result

# Функція асиміляції за дзвінкістю
def voice_assimilation(word: str) -> str:
  global rules_used
  def replace_match(match):
    voiceless = match.group(1)
    voiced = match.group(2)
    result = voice_assimilation_map[voiceless] + voiced

    return result
  
  result = re.sub(r"([цкшхпчст])([гзджбґ]|д͡з|д͡ж)", replace_match, word)

  if result != word:
    rules_used.append('-Асиміляція за дзвінкістю')

  return result

# Функція обов'язкової асиміляції за глухістю
def voicelessness_assimilation(word: str) -> str:
  global rules_used
  def replace_match(match):
    voiceless = match.group(2)
    return "с" + voiceless

  def exceptions(match):
    preposition = match.group(1)
    stress = match.group(2)
    postposition = match.group(3)

    return f'{preposition}{stress}х{postposition}'
  
  is_exception = re.sub(r"(ле|в°?о|(?:кߴ|н')і|д'°о)(\u0301?)г(к|т)", exceptions, word)
  obligatory = re.sub(r"^(з)([цкшхфпчст])", replace_match, is_exception)

  if is_exception != word:
    rules_used.append('-Асиміляція за глухістю (слово-виняток)')
  elif obligatory != word:
    rules_used.append('-Асиміляція за глухістю')
  
  return obligatory

# Функція асиміляції за способом творення
def WOP_assimilation(word: str) -> str:
  global rules_used
  def replace_regressive(match):
    target = match.group(1)
    misc = match.group(2)
    assimilator = match.group(3)
    result = WOP_assimilation_map[target] + misc + assimilator
    
    return result
  
  in_verbs = re.sub(r"т'с'а$", "ц':а", word)
  regressive = re.sub(r"([дт])('?)([зсц]|д͡з)", replace_regressive, in_verbs)
  progressive_in_non_verbs = re.sub(r"цс'", "ц'", regressive)

  if in_verbs != word:
    rules_used.append('-Регресивно-прогресивна асиміляція за способом творення без стягнення')
  elif regressive != in_verbs and regressive != word:
    rules_used.append('-Асиміляція за способом творення')
  elif progressive_in_non_verbs != word:
    rules_used.append('-Регресивно-прогресивна асиміляція за способом творення зі стягненням')

  return progressive_in_non_verbs

# Функція асиміляції за місцем та способом творення
def POPWOP_assimilation(word: str) -> str:
  global rules_used
  def replace_match(match):
    target = match.group(1)
    misc = match.group(2)
    assimilator = match.group(3)
    result = POPWOP_assimilation_map[target] + misc + assimilator
    
    return result

  step1 = re.sub(r"([дт])('?)([жшч]|д͡ж)", replace_match, word)
  step2 = re.sub(r"([зсц]|д͡з)('?)([жшч]|д͡ж)", replace_match, step1)
  step3 = re.sub(r"([жшч]|д͡ж)('?)([зсц]|д͡з)", replace_match, step2)

  if step1 != word and step2 != word and step3 != word:
    rules_used.append('-Асиміляція за місцем та способом творення')

  return step3

# Функція асиміляції за м'якістю
def softness_assimilation(word: str) -> str:
  global rules_used
  def replace_match(match):
    target = match.group(1)
    palatalized = match.group(2)
    sign = match.group(3)
    result = f"{target}'{palatalized}{sign}"

    return result

  obligatory = re.sub(r"([дтн])([дтн])(['])", replace_match, word)
  optional = re.sub(r"([зсц]|д͡з)([цкнгґшзхфвпрлджчсмтб]|д͡з|д͡ж)(['ߴ])", replace_match, obligatory)

  if obligatory != word:
    rules_used.append('-Асиміляція за м\'якістю обов\'язкова')
  elif optional != obligatory:
    rules_used.append('-Асиміляція за м\'якістю, факультативна')
  
  return optional

# Функція спрощення приголосних
def consonant_reduction(word: str) -> str:
  global rules_used
  def obligatory_replace(match):
    prev = match.group(1)
    next = match.group(2)
    
    result = f'{prev}{next}'

    return result

  if re.findall(r'запj·а́стн|хвастн', word):
    rules_used.append('-Виняток, редукція приголосних')
    return word
  else:
    reduction = re.sub(r"(с|н)т(ч|ц'|н|д|с)", obligatory_replace, word)
    if reduction != word:
      rules_used.append('-Редукція приголосних')
      contraction = re.sub(r"сс", "с", reduction)
      if contraction != reduction:
        rules_used.append('-Редукція приголосних, стягнення приголосних')

    return reduction

# Функція перевірки правильності введеного слова
def check_input(word: str) -> str:
  word_cleared = ((word.strip()).casefold()).replace("-", "")
  char_check = re.findall(r"[qwertyuiopasdfghjklzxcvbnm,\.;!+=\$№#@\"&]", word_cleared)
  if char_check:
    return "ПОМИЛКА: Виявлено невідомі символи"
  elif " " in word_cleared:
    return "ПОМИЛКА: Було введено більше одного слова"
  for i, char in enumerate(word_cleared):
    if char == "%" and word_cleared[i-1] not in vowels:
      return "ПОМИЛКА: Приголосний позначено як наголошений"
  else:
    return stress(word_cleared)

# Функція транскрибування слова
def phonetic(word: str) -> str:
  global rules_used
  word = check_input(word)
  if word == "":
    return ""
  elif '\u0301' in word:
    transformations = (
      jotted_letters,
      vocalized_consonants,
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
    print('Використані правила:')
    for rule in rules_used:
      print(rule)
    rules_used = []
    return f'[{result}]'
  else:
    return 'ПОМИЛКА: У слові не визначено наголос'
  
def phonematic(word: str) -> str:
  word = check_input(word)
  if word == "":
    return ""
  elif '\u0301' in word:
    transformations = (
      jotted_letters,
      vocalized_consonants,
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
    return f'/{result}/'

  else:
    return 'ПОМИЛКА: У слові не визначено наголос'