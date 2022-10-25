import spacy
from collections import defaultdict

def parse_word(word_string):
    new_pattern = defaultdict(dict)
    quotes = ["'", "«", "»", '"']
    l = []
    for quote in quotes:
        if quote in word_string:
            l.append(1)
            clean = word_string.strip(quote)
            word_string = clean
            new_pattern.update(form=clean)
        else:
            l.append(0)
    if sum(l) == 0:
        nlp = spacy.load("ru_core_news_sm")
        lemma = nlp(word_string)[0].lemma_
        new_pattern['lemma'] = lemma
    return dict(new_pattern)

def find_missing_nodes(node_patterns, constraints): 
    constraint_nodes = set([n for pair in constraints for n in pair])
    return {missing_node: {} for missing_node in constraint_nodes - set(node_patterns.keys())}

def request2query(response_dict): 
    node_patterns = defaultdict(dict)
    constraints = {}
    range2indexes = {'from': 0, 'to': 1}
    for field in response_dict: 
        if response_dict[field]: 
            field_name = field.split('_')[1]
            token_id = field.split('_')[0]
            if field_name == 'features':
                new_pattern = {f.split('=')[0].strip(): f.split('=')[1].strip() for f in response_dict[field].split(',')}
            elif field_name == 'word':
                new_pattern = parse_word(response_dict[field])
            elif field_name == 'from' or field_name == 'to':
                new_pattern = {}
                pair = (str(int(token_id)- 1), token_id)
                if not constraints.get(pair):
                    constraints[pair] = {'lindist': [1, 1]}
                constraints[pair]['lindist'][range2indexes[field_name]] = int(response_dict[field])
            else:
                new_pattern = {(field_name, response_dict[field])}
            node_patterns[token_id].update(new_pattern)
    
    node_patterns.update(find_missing_nodes(node_patterns, constraints))
    return dict(node_patterns), constraints

def string2query(s):
    nlp = spacy.load("ru_core_news_sm")
    doc = nlp(s)
    node_patterns = {}
    for sent in doc.sents:
        for token in sent:
            value = {}
            value['form'] = token.text
            node_patterns[str(token.i - sent.start)] = value
    constraints = {}
    if len(doc) > 1:
        for key in node_patterns:
            if int(key) > 0:
                lndst = {}
                lndst['lindist'] = (1, 1)
                constraints[str(int(key) - 1), key] = lndst            
    return node_patterns, constraints

def search_info(search_result):
    search = {}
    n_sentences = len(set([' '.join([t[0] for t in entry]) for doc in search_result for entry in search_result[doc]['entries']]))
    n_documents = len(search_result)
    n_entries = len([entry for doc in search_result for entry in search_result[doc]['entries']])
    search['documents'] = n_documents
    search['sentences'] = n_sentences
    search['entries'] = n_entries
    return search

def query_info(n_p, cs):
    result = []
    if '0' in n_p:
        if len(n_p['0']) > 1:
            feats = []
            for key3 in n_p['0']:
                feats.append(n_p['0'][key3])
            feats_str = " & ".join(feats)
            result.append(feats_str)     
        else:
            tag = list(n_p['0'])
            if len(tag) == 1 and tag[0] == 'form' :
                word = '"' + n_p['0'][tag[0]] + '"'
                result.append(word)
            elif len(tag) == 1 and tag[0] != 'form' :
                word = n_p['0'][tag[0]]
                result.append(word)
            else:
                word = '_'
                result.append(word)
    for key1 in n_p:
        for key2 in cs:
            if key1 == key2[1]:
                if len(n_p[key1]) > 1:
                    feats = []
                    for key3 in n_p[key1]:
                        feats.append(n_p[key1][key3])
                    feats_str = " & ".join(feats)
                    from_ = cs[key2]['lindist'][0]
                    to = cs[key2]['lindist'][1]
                    result.append(f'{feats_str}, на расстоянии от {from_} до {to} от Слова {key1}')
                else:
                    tag = list(n_p[key1])
                    if len(tag) == 1 and tag[0] == 'form' :
                        word = '"' + n_p[key1][tag[0]] + '"'
                        from_ = cs[key2]['lindist'][0]
                        to = cs[key2]['lindist'][1]
                        result.append(f'{word}, на расстоянии от {from_} до {to} от Слова {key1}')
                    elif len(tag) == 1 and tag[0] != 'form' :
                        word = n_p[key1][tag[0]]
                        from_ = cs[key2]['lindist'][0]
                        to = cs[key2]['lindist'][1]
                        result.append(f'{word}, на расстоянии от {from_} до {to} от Слова {key1}')
                    else:
                        word = '_'
                        result.append(word)
    return result
