from flask import Flask, render_template, request
from pathlib import Path

from search.search_back import query_parsers, searching
from search.search_back.html_fillers import GRAM_FEATS, POS_LIST, HELP, SIMPLE_SEARCH, ADVANCED_SEARCH


app = Flask(__name__)

CONLLU_PATH_FROM_PROJECT_ROOT = Path('corpora/parsing/corpus_parsed.conllu')


@app.route('/')
def main_page():
    return render_template('search.html', pos_tags=POS_LIST, features=GRAM_FEATS, instructions=HELP)


@app.route('/results', methods=['GET', 'POST'])
def results():

    if request.method == 'GET':
        exact_forms = request.args.get('exact_form')
        query = query_parsers.string2query(exact_forms)

    elif request.method == 'POST':
        request_dict = request.form
        query = query_parsers.request2query(request_dict)

    abs_conllu_path = Path('../../').resolve().joinpath(CONLLU_PATH_FROM_PROJECT_ROOT)
    result = searching.corpora_search(abs_conllu_path, query)

    result_info = query_parsers.search_info(result)
    query_info = query_parsers.query_info(query[0], query[1])
    return render_template('results.html', results=result, search_meta=result_info, query_meta=query_info)


@app.route('/instructions')
def instructions():
    return render_template('instructions.html', simple=SIMPLE_SEARCH, advanced=ADVANCED_SEARCH)


@app.route('/aboutcorpus')
def aboutcorpus():
    return render_template('stats.html')


if __name__ == '__main__':
    app.run()
