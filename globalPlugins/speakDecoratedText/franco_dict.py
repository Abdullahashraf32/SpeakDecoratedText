import re
def smart_franco_to_arabic(text):
  multi_char_patterns = {
    'gh': 'غ',
    'kh': 'خ',
    'sh': 'ش',
    'ch': 'تش',
    'th': 'ث',
    'ph': 'ف',
    'oo': 'و',
    'ou': 'و',
    'ee': 'ي',
    'aw': 'او',
    'ai': 'اي',
    'ay': 'اي',
    'ea': 'يا',
    'io': 'يو',
    'zh': 'ج',
    'ts': 'ص',
    'dz': 'ض',
    'dj': 'ج',
    'aa': 'ا',
    'uu': 'و',
    'ii': 'ي',
    'ey': 'اي',
    'oa': 'وا',
    'tt': 'تّ',
    'ss': 'سّ',
    'll': 'لّ',
  }

  number_replacements = {
    '2': 'أ',
    '3': 'ع',
    '5': 'خ',
    '6': 'ط',
    '7': 'ح',
    '8': 'ق',
    '9': 'ص',
  }

  single_letters = {
    'a': 'ا',
    'b': 'ب',
    'c': 'ك',
    'd': 'د',
    'e': 'ي',
    'f': 'ف',
    'g': 'ج',
    'h': 'ه',
    'i': 'ي',
    'j': 'ج',
    'k': 'ك',
    'l': 'ل',
    'm': 'م',
    'n': 'ن',
    'o': 'و',
    'p': 'ب',
    'q': 'ق',
    'r': 'ر',
    's': 'س',
    't': 'ت',
    'u': 'و',
    'v': 'ف',
    'w': 'و',
    'x': 'كس',
    'y': 'ي',
    'z': 'ز',
  }

  def convert_word(word):
    for key, value in number_replacements.items():
      word = word.replace(key, value)

    for key in sorted(multi_char_patterns, key=len, reverse=True):
      value = multi_char_patterns[key]
      word = re.sub(re.escape(key), value, word, flags=re.IGNORECASE)

    for key, value in single_letters.items():
      word = re.sub(re.escape(key), value, word, flags=re.IGNORECASE)

    return word

  tokens = re.findall(r'\d+|[A-Za-z]+|[^\w\s]', text)
  converted_tokens = []
  for i in tokens:
    if re.match(r'^[A-Za-z0-9]+$', i):
      converted_tokens.append(convert_word(i))
    else:
      converted_tokens.append(i)

  return ''.join(converted_tokens)
