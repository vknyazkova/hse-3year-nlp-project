from conllu import models, parse_incr
from search.search_back.sentence_filter import SentenceFilter
from collections import defaultdict


def highlighted_tokens(all_suitable_tokens: dict, sentence: models.TokenList) -> list:
    """Возвращает список из кортежей (токен, лейбл), где лейбл=1, если токен из запроса, =0 - если не из запроса """

    token_format = []
    for token in sentence:
        format_label = 0
        if isinstance(token['id'], int):
            if token['id'] - 1 in all_suitable_tokens:
                format_label = 1
        token_format.append((token['form'], format_label))
    return token_format


def corpora_search(conllu_path, query):
    result = defaultdict(list)
    conlluf = open(conllu_path, 'r', encoding='utf-8')
    for sentence in parse_incr(conlluf):

        sf = SentenceFilter(sentence)
        sf.filter_sentence(query[0], query[1])
        if sf.entries:
            for entry in sf.entries:
                result[(sentence.metadata['source'], sentence.metadata['name'])].append(highlighted_tokens(entry, sentence))
    conlluf.close()
    result = {i + 1: {'source': doc[0], 'name': doc[1], 'entries': result[doc]} for i, doc in enumerate(result)}
    return result
