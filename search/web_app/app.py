from flask import Flask, render_template, request
from search.search_back import query_parsers, search

app = Flask(__name__)


CONLLU_PATH = 'corpora/recipe_corpora.conllu'
POS_LIST = ['ADJ', 'ADP', 'ADV', 'AUX', 'CCONJ', 'DET', 'INTJ', 'NOUN', 'NUM', 'PART',
            'PRON', 'PROPN', 'PUNCT', 'SCONJ', 'SYM', 'VERB', 'X']
GRAM_FEATS = {
    'Abbr': ['Yes'],
    'Animacy': ['Anim', 'Inan'],
    'Aspect': ['Imp', 'Perf'],
    'Case': ['Acc', 'Dat', 'Gen', 'Ins', 'Loc', 'Nom', 'Par', 'Voc'],
    'Degree': ['Cmp', 'Pos', 'Sup'],
    'Foreign': ['Yes'],
    'Gender': ['Fem', 'Masc', 'Neut'],
    'Mood': ['Cnd', 'Imp', 'Ind'],
    'Number': ['Plur', 'Sing'],
    'NumType': ['Card'],
    'Person': ['1', '2', '3'],
    'Polarity': ['Neg'],
    'Poss': ['Yes'],
    'PronType': ['Dem', 'Ind', 'Int', 'Neg', 'Prs', 'Rel', 'Tot'],
    'Reflex': ['Yes'],
    'Tense': ['Fut', 'Past', 'Pres'],
    'Typo': ['Yes'],
    'Variant': ['Short'],
    'VerbForm': ['Conv', 'Fin', 'Inf', 'Part'],
    'Voice': ['Act', 'Mid', 'Pass']
}
INSTRUCTIONS = {
    'word': 'Используйте кавычки для поиска точных форм (напр. "курицу"). Если слово будет не в начальной форме и '
            'без кавычек, то слово будет лемматизировано и поиск будет произведен по лемме. ',
    'features': 'Каждый признак имеет вид: ГрамКатегория=Значение и отделяется друг от друга запятой. Для списка '
                'тегов смотрите '
}


@app.route('/')
def main_page():
    return render_template('search.html', pos_tags=POS_LIST, features=GRAM_FEATS, instructions=INSTRUCTIONS)


@app.route('/results', methods=['GET', 'POST'])
def results():

    if request.method == 'GET':
        exact_forms = request.args.get('exact_form')
        query = query_parsers.string2query(exact_forms)

    elif request.method == 'POST':
        result = request.form
        print(result)
        query = query_parsers.response2query(result)


    query = [
        {
            '0': {'upos': 'VERB'},
            '1': {'lemma': 'курица'}
        },
        {
            ('0', '1'): {'lindist': (1, 1)}
        }
    ]

    result = search.corpora_search(CONLLU_PATH, query)
    info = query_parsers.search_info(result)

    result_info = {
        'documents': 100,
        'sentences': 100,
        'entries': 100
    }
    query_info = [
        'VERB',
        'курица, на расстоянии от 1 до 1 от Слова 0'
    ]

    return render_template('results.html', results=result, search_meta=result_info, query_meta=query_info)


if __name__ == '__main__':
    app.run()
