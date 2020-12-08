from difflib import SequenceMatcher
import re


def _remove(word, word_filter):
    for old in word_filter:
        if word.endswith(old):
            word = word.replace(old, '')
    return word


def _is_word_in_sentence(word, sentence):
    return re.compile(r'\b({0})\b'.format(word), flags=re.IGNORECASE).search(
        sentence
    )


def get_best_match(word, items, word_filter=[]):
    if word_filter:
        word = _remove(word, word_filter)
        items = list(map(lambda x: _remove(x, word_filter), items))

    socres = list(get_scores(word, items))
    max_score = max(socres)
    idx_max_score = socres.index(max_score)

    if max_score == 1.0:
        return idx_max_score, max_score

    for idx, item in enumerate(items):
        if _is_word_in_sentence(item, word) or _is_word_in_sentence(
            word, item
        ):
            return idx, 1.0

    return idx_max_score, max_score


def get_scores(word, items):
    return map(
        lambda item: get_score(word, item),
        items,
    )


def get_score(word_a, word_b):
    return SequenceMatcher(None, word_a.lower(), word_b.lower()).ratio()


def get_word_list_diff(words_a, words_b):
    words_a = sorted(words_a)
    words_b = sorted(words_b)

    result = []
    for ida, stock_a in enumerate(words_a):
        _, max_score = get_best_match(stock_a, words_b)
        if max_score > 0.75:
            result.append(ida)
    missing = [value for idx, value in enumerate(words_a) if idx not in result]
    return missing
