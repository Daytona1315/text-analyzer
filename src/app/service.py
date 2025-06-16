import re
import string


ALLOWED_EXTENSIONS = ['txt', 'doc', 'docx', 'pdf']


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def count_text(text: str) -> dict:
    """Returns a dictionary with words, punctuation, numbers lists and their counts at the end"""
    splitted = text.split()
    dictionary = {
        'preview': [],
        'symbols': [],
        'words': [],
        'punctuation': [],
        'numbers': []
    }

    # Main cycle
    for word in splitted:
        if not word:
            continue  # skipping blank strings
        if word.isdigit():
            dictionary['numbers'].append(word)
        elif word and re.match(f'[{re.escape(string.punctuation)}]$', word[-1]):
            dictionary['punctuation'].append(word[-1])
            w = word[:-1]
            if w:  # if the part of word remained
                if w.isdigit():
                    dictionary['numbers'].append(w)
                else:
                    dictionary['words'].append(w)
        else:
            dictionary['words'].append(word)

    # Counting symbols
    for symbol in text.strip():
        if symbol == " " or symbol == "/n":
            continue
        else:
            dictionary['symbols'].append(symbol)

    # Adding quantity of each category to the end of every list
    for key in dictionary:
        count = len(dictionary[key])
        dictionary[key].append(count if count > 0 else 0)

    # Counting spaces
    spaces: list = text.count(" ")
    dictionary['spaces'] = [spaces if spaces > 0 else 0]

    # Adding preview string
    preview: str = text[:170]
    dictionary['preview'] = preview

    return dictionary
