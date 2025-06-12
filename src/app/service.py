import re
import string


def count_text(text: str) -> dict:
    """Returns a dictionary with words, punctuation, numbers lists and their counts at the end"""
    splitted = text.split()
    dictionary = {
        'words': [],
        'punctuation': [],
        'numbers': []
    }

    for word in splitted:
        if not word:
            continue  # пропустить пустые строки, например из-за двойных пробелов
        if word.isdigit():
            dictionary['numbers'].append(word)
        elif word and re.match(f'[{re.escape(string.punctuation)}]$', word[-1]):
            dictionary['punctuation'].append(word[-1])
            w = word[:-1]
            if w:  # если осталась часть слова
                if w.isdigit():
                    dictionary['numbers'].append(w)
                else:
                    dictionary['words'].append(w)
        else:
            dictionary['words'].append(word)

    # Добавляем количество элементов в конец каждого списка
    for key in dictionary:
        count = len(dictionary[key])
        dictionary[key].append(count if count > 0 else 0)
    # Подсчёт пробелов
    spaces = text.count(" ")
    dictionary['spaces'] = [spaces if spaces > 0 else 0]

    return dictionary
