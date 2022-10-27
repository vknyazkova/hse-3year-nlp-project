from flask import Flask, render_template, request
from pathlib import Path
import spacy

from search.search_back import query_parsers, searching
from search.search_back.html_fillers import GRAM_FEATS, POS_LIST, HELP, SIMPLE_SEARCH, ADVANCED_SEARCH, SEARCH_RULES

app = Flask(__name__)

CONLLU_PATH_FROM_PROJECT_ROOT = Path('corpora/parsing/corpus_parsed.conllu')


@app.route('/')
def main_page():
    return render_template('search.html', pos_tags=POS_LIST, features=GRAM_FEATS, instructions=HELP)


@app.route('/results', methods=['GET', 'POST'])
def results():
    nlp = spacy.load("ru_core_news_sm")
    if request.method == 'GET':
        exact_forms = request.args.get('exact_form')
        query = query_parsers.string2query(exact_forms, nlp)

    elif request.method == 'POST':
        request_dict = request.form
        query = query_parsers.request2query(request_dict, nlp)

    # abs_conllu_path = Path('../../').resolve().joinpath(CONLLU_PATH_FROM_PROJECT_ROOT)
    abs_conllu_path = '/home/vknyazkova/hse-3year-nlp-project/corpora/parsing/corpus_parsed.conllu'
    result = searching.corpora_search(abs_conllu_path, query)

    result_info = query_parsers.search_info(result)
    query_info = query_parsers.query_info(query[0], query[1])
    return render_template('results.html', results=result, search_meta=result_info, query_meta=query_info)


@app.route('/instructions')
def instructions():
    return render_template('instructions.html', simple=SIMPLE_SEARCH, advanced=ADVANCED_SEARCH, rules=SEARCH_RULES)


@app.route('/statistics')
def corpus_statistics():
    return render_template('stats.html')


@app.route('/aboutcorpus')
def aboutcorpus():
    return render_template('about.html')


@app.route('/credits')
def our_credits():
    return render_template('credits.html')


if __name__ == '__main__':
    app.run()
