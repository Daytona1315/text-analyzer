import re
import string
import docx
import PyPDF2
import textract


ALLOWED_EXTENSIONS = ['txt', 'doc', 'docx', 'pdf']


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text(file_path, extension):
    match extension:
        case '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        case '.docx':
            doc = docx.Document(file_path)
            return '\n'.join(para.text for para in doc.paragraphs)
        case '.pdf':
            text = ''
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() or ''
            return text
        case '.doc':
            return textract.process(file_path).decode('utf-8')
        case _:
            return ''


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
