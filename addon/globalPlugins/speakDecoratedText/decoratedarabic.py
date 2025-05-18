import re
import unicodedata

# This dictionary maps various decorated or alternative forms of Arabic and Latin letters
# to their normalized Arabic equivalents. It is used to replace stylized, unicode variants,
# or similar-looking characters with standard Arabic ones to improve readability and compatibility.
replacements = {
    '𝔄': 'ا', '𝔞': 'ا', '𝓐': 'ا', '𝒜': 'ا', '𝒶': 'ا',
    '𝐀': 'ا', '𝐚': 'ا', '𝕬': 'ا', '𝖆': 'ا', '𝙰': 'ا', '𝚊': 'ا',
    '𝔄̇': 'ا', '𝔄̈': 'ا',
    '𝔅': 'ب', '𝔟': 'ب', '𝓑': 'ب', '𝒷': 'ب', '𝐁': 'ب', '𝐛': 'ب',
    '𝕭': 'ب', '𝖇': 'ب', '𝙱': 'ب', '𝚋': 'ب', 'ٮ': 'ب', 'پ': 'ب',
    '𝔗': 'ت', '𝔱': 'ت', '𝓣': 'ت', '𝓉': 'ت', '𝐓': 'ت', '𝐭': 'ت',
    '𝕋': 'ت', '𝖙': 'ت', '𝚃': 'ت', '𝚝': 'ت',
    'ة': 'ة', '𝓉̇': 'ة', '𝔱̇': 'ة', '𝓉̈': 'ة', '𝔱̈': 'ة',
    '𝕥̈': 'ة', '𝕥̇': 'ة', '𝓽̇': 'ة', 'ۀ': 'ة',
    'ث': 'ث', '𝔗̱': 'ث', '𝔱̱': 'ث',
    '𝔍': 'ج', '𝔧': 'ج', '𝓙': 'ج', '𝒿': 'ج', '𝐉': 'ج', '𝐣': 'ج',
    '𝕁': 'ج', '𝖏': 'ج', '𝙹': 'ج', '𝚓': 'ج', 'چ': 'ج',
    'ح': 'ح', '𝔥': 'ح', '𝓗': 'ح', '𝒽': 'ح', '𝐇': 'ح', '𝐡': 'ح',
    'خ': 'خ', '𝔨': 'خ', '𝓚': 'خ', '𝓀': 'خ', '𝐊': 'خ', '𝐤': 'خ',
    'د': 'د', '𝔇': 'د', '𝔡': 'د', '𝓓': 'د', '𝒹': 'د', '𝐃': 'د', '𝐝': 'د',
    'ذ': 'ذ', '𝔇̱': 'ذ', '𝔡̱': 'ذ',
    'ر': 'ر', '𝔕': 'ر', '𝔯': 'ر', '𝓡': 'ر', '𝓇': 'ر', '𝐑': 'ر', '𝐫': 'ر',
    'ز': 'ز', '𝔃': 'ز', '𝓩': 'ز', '𝓏': 'ز', '𝐙': 'ز', '𝐳': 'ز', 'ژ': 'ز',
    'س': 'س', '𝔖': 'س', '𝔰': 'س', '𝓢': 'س', '𝓈': 'س', '𝐒': 'س', '𝐬': 'س',
    'ش': 'ش', '𝔖̱': 'ش', '𝔰̱': 'ش',
    'ص': 'ص', '𝔠': 'ص', '𝓒': 'ص', '𝒸': 'ص', '𝐂': 'ص', '𝐜': 'ص',
    'ض': 'ض', '𝔡̱': 'ض',
    'ط': 'ط', '𝔱̱': 'ط',
    'ظ': 'ظ', '𝔱̤': 'ظ',
    'ع': 'ع', '𝔞̱': 'ع', '𝔄̱': 'ع', 'ػ': 'ع',
    'غ': 'غ', '𝔤': 'غ', '𝓖': 'غ', '𝑔': 'غ', 'ؼ': 'غ',
    'ف': 'ف', '𝔣': 'ف', '𝓕': 'ف', '𝒻': 'ف', 'ڤ': 'ف', 'ؽ': 'ف',
    'ق': 'ق', '𝔮': 'ق', '𝓠': 'ق', '𝓆': 'ق', 'ڨ': 'ق', 'ؾ': 'ق',
    'ك': 'ك', '𝔨': 'ك', '𝓚': 'ك', '𝓀': 'ك', 'ؿ': 'ك', 'گ': 'ك', 'ک': 'ك',
    'ل': 'ل', '𝔩': 'ل', '𝓛': 'ل', '𝓁': 'ل',
    'م': 'م', '𝔪': 'م', '𝓜': 'م', '𝓂': 'م',
    'ن': 'ن', '𝔫': 'ن', '𝓝': 'ن', '𝓃': 'ن', 'ں': 'ن',
    'ه': 'ه', '𝔥': 'ه', '𝓗': 'ه', '𝒽': 'ه', 'ھ': 'ه',
    'و': 'و', '𝔴': 'و', '𝓦': 'و', '𝓌': 'و', 'ۊ': 'و',
    'ي': 'ي', '𝔶': 'ي', '𝓨': 'ي', '𝓎': 'ي', 'ې': 'ي', 'ۑ': 'ي', 'ې': 'ي', 'ۍ': 'ي',
    'ى': 'ى', '𝔶̱': 'ى', '𝓨̱': 'ى', '𝓎̱': 'ى',
    'ٱ': 'ا',
    'أ': 'أ', 'إ': 'إ', 'آ': 'آ', 'ء': 'ء',
    'ؤ': 'ؤ', 'ئ': 'ئ',
    'ہ': 'ه',
    '𝓂̇': 'م', '𝓃̇': 'ن',
    'A': 'ا', 'a': 'ا',
    'B': 'ب', 'b': 'ب',
    'T': 'ت', 't': 'ت',
    'J': 'ج', 'j': 'ج',
    'H': 'ح', 'h': 'ح',
    'K': 'ك', 'k': 'ك',
    'S': 'س', 's': 'س',
    'D': 'د', 'd': 'د',
    'R': 'ر', 'r': 'ر',
    'Z': 'ز', 'z': 'ز',
    'M': 'م', 'm': 'م',
    'N': 'ن', 'n': 'ن',
    'W': 'و', 'w': 'و',
    'Y': 'ي', 'y': 'ي',
    'F': 'ف', 'f': 'ف',
    'Q': 'ق', 'q': 'ق',
    'G': 'غ', 'g': 'غ',
    '𝟎': '0', '𝟏': '1', '𝟐': '2', '𝟑': '3', '𝟒': '4',
    '𝟓': '5', '𝟔': '6', '𝟕': '7', '𝟖': '8', '𝟗': '9',
    '𝟘': '0', '𝟙': '1', '𝟚': '2', '𝟛': '3', '𝟜': '4',
    '𝟝': '5', '𝟞': '6', '𝟟': '7', '𝟠': '8', '𝟡': '9',
    '𝟬': '0', '𝟭': '1', '𝟮': '2', '𝟯': '3', '𝟰': '4',
    '𝟱': '5', '𝟲': '6', '𝟳': '7', '𝟴': '8', '𝟵': '9',
    '𝟢': '0', '𝟣': '1', '𝟤': '2', '𝟥': '3', '𝟦': '4',
    '𝟧': '5', '𝟨': '6', '𝟩': '7', '𝟪': '8', '𝟫': '9',
    '۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4',
    '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9',
}

def normalize_text(text):
  """
  Normalize stylized or decorated Arabic text by replacing characters
  with their standard forms and removing unnecessary diacritics.

  Steps:
  1. Replace characters using the 'replacements' dictionary.
  2. Normalize unicode characters using NFKD form to decompose them.
  3. Remove Tatweel (Kashida) and most diacritics except Hamza Above and Below.
  4. Recompose the cleaned string using NFC form.

  Args:
    text (str): The input string to normalize.

  Returns:
    str: The normalized text.
  """
  # Replace all decorated characters based on the replacements dictionary
  for key, value in replacements.items():
    text = re.sub(re.escape(key), value, text)

  # Decompose characters to separate base letters from diacritics
  text = unicodedata.normalize("NFKD", text)
  cleaned = ''
  for i in text:
    # Skip Tatweel (Kashida) character
    if i == 'ـ':
      continue
    # Skip most diacritic marks except Hamza Above (U+0654) and Hamza Below (U+0655)
    if unicodedata.category(i) == 'Mn' and i not in ['\u0654', '\u0655']:
      continue
    cleaned += i

  # Recompose characters into their canonical form
  return unicodedata.normalize("NFC", cleaned)
