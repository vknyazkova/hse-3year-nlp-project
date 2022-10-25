!pip3 install setuptools wheel
!pip3 install spacy
!python3 -m spacy download ru_core_news_sm
import spacy

def response2query(response_dict):
    nlp = spacy.load("ru_core_news_sm")
    node_patterns = {}
    constraints = {}
    fields = ['upos', 'features']
    for key1 in response_dict:
        ID = key1.split('_')[0]
        if 'word' in key1 and response_dict[key1] != '':
            if '"' in response_dict[key1]:
                category = {}
                category['form'] = response_dict[key1].strip('"')
                node_patterns[ID] = category
            else:
                category = {}
                for key2 in response_dict:
                    if key2.split('_')[0] == ID and key2.split('_')[1] in fields:
                        clean = response_dict[key1].strip("«»'")
                        lemma = nlp(clean)[0].lemma_
                        category['lemma'] = lemma
                        if key2.split('_')[1] == 'upos' and response_dict[key2] != '':
                            category['upos'] = response_dict[key2]
                        elif key2.split('_')[1] == 'features' and response_dict[key2] != '':
                            for cat in response_dict[key2].split(','):
                                category[cat.strip(' ').split('=')[0]] = cat.strip(' ').split('=')[1]
                        
                node_patterns[ID] = category
                           
        elif 'from' in key1:
            for key2 in response_dict:
                if key2.split('_')[0] == ID and key2.split('_')[1] == 'to':
                    lndst = {}
                    lndst_value = (int(response_dict[key1]), int(response_dict[key2]))
                    lndst['lindist'] = lndst_value
                    constr_key = (str((int(ID)) - 1), ID)
                    constraints[constr_key] = lndst
    return node_patterns, constraints

def query_info(n_p, cs): # n_p - node_patterns; cs - constraints
    result = []
    if '0' in n_p:
        if len(n_p['0']) > 1:
            feats = []
            for key3 in n_p['0']:
                feats.append(n_p['0'][key3])
            feats_str = " & ".join(feats)
            result.append(feats_str)     
        else:
            tag = list(n_p['0'])[0] # определяю какой ключ: lemma или form
            word = n_p['0'][tag]
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
                    tag = list(n_p[key1])[0] # определяю какой ключ: lemma или form
                    word = '"' + n_p[key1][tag] + '"'
                    from_ = cs[key2]['lindist'][0]
                    to = cs[key2]['lindist'][1]
                    result.append(f'{word}, на расстоянии от {from_} до {to} от Слова {key1}')
    return result

