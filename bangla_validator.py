import unicodedata

allowed_punctuation = {'।', '৳', '৹', '৷', 'ঃ', ' ', '\n'}

# So -> special other characters
# Cf -> characters for formatting
allowed_categories = ['So', 'Cf']

def is_bangla(text: str) -> bool:
    
    for char in text:
        # Check if the character is in valid Bengali range or allowed punctuation
        if not (
            '\u0980' <= char <= '\u09FF'   # Bengali letters and syllables
            or '\u09F0' <= char <= '\u09F1'  # Bengali digits
            or char in allowed_punctuation  # Common Bengali and general punctuation
            or unicodedata.category(char).startswith('P')
            or unicodedata.category(char) in allowed_categories
        ):
            print(char, " Unicode data: ", unicodedata.category(char))
            return False
    return True