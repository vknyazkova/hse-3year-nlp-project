#!/usr/bin/env python
# coding: utf-8

# In[52]:


get_ipython().system('pip3 install setuptools wheel')
get_ipython().system('pip3 install spacy')
get_ipython().system('python3 -m spacy download ru_core_news_sm')
import spacy


# In[53]:


nlp = spacy.load("ru_core_news_sm")


# # Функция 1

# In[98]:


def response2query(response_dict):
    node_patterns = {}
    constraints = {}
    fields = ['upos', 'features']
    for key1 in response_dict:
        ID = key1.split('_')[0]
        if 'word' in key1:
            if '"' in response_dict[key1]:
                category = {}
                category['form'] = response_dict[key1].strip('"')
                node_patterns[ID] = category
            else:
                category = {}
                for key2 in response_dict:
                    if key2.split('_')[0] == ID and key2.split('_')[1] in fields:
                        lemma = nlp(response_dict[key1])[0].lemma_
                        if response_dict[key1] == lemma:
                            if key2.split('_')[1] == 'upos':
                                category['lemma'] = response_dict[key1]
                                category['upos'] = response_dict[key2]
                            elif key2.split('_')[1] == 'features':
                                category['lemma'] = response_dict[key1]
                                for cat in response_dict[key2].split(','):
                                    category[cat.strip(' ').split('=')[0]] = cat.strip(' ').split('=')[1]
                        else:
                            if key2.split('_')[1] == 'upos':
                                category['lemma'] = lemma
                                category['upos'] = response_dict[key2]
                            elif key2.split('_')[1] == 'features':
                                category['lemma'] = lemma
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


# In[99]:


example_response_dict = {
    '0_word': 'бежать', # лемма -> lemma
    '1_word': 'школу', # словоформа, которую надо привести к лемме -> lemma
    '2_word': '"бегу"',  # словоформа, которую не надо приводить к лемме -> form
    '0_upos': 'VERB', 
    '0_features': 'Tense=Past, Person=1',  
    '1_features': 'Case=Nom',
    '2_from': '0',
    '3_from': '1',
    '2_to': '1',
    '3_to': '2'
}


# In[102]:


print(response2query(example_response_dict))


# # Функция 2

# In[54]:


s = 'промыть курицу и порезать ее'


# In[55]:


def string2query(s):
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


# In[57]:


print(string2query(s))


# # Функция 3

# In[110]:


example_search_result = {
    1: {
        'source': 'https://www.gastronom.ru/recipe/1035', 
        'name': 'Цыпленок карри', 
        'entries': [
            [('Разрубить', 1), ('курицу', 1), ('на', 0), ('небольшие', 0), ('куски', 0), ('.', 0)], 
            [('Перемешать', 1), ('курицу', 1), ('с', 0), ('маринадом', 0), (',', 0), ('оставить', 0), ('на', 0), ('3', 0), ('часа', 0), ('.', 0)]
            ]
        }, 
    2: {
        'source': 'https://www.gastronom.ru/recipe/1127', 
        'name': 'Итальянский пирог с курицей и кабачком', 
        'entries': [
            [('оливкового', 0), ('масла', 0), ('и', 0), ('подрумянить', 1), ('курицу', 1), ('на', 0), ('среднем', 0), ('огне', 0), ('.', 0)], 
            [('Вновь', 0), ('положить', 1), ('курицу', 1), ('в', 0), ('форму', 0), (',', 0), ('добавить', 0), ('чеснок', 0), ('и', 0), ('майоран', 0), (',', 0), ('жарить', 0), ('1', 0), ('мин', 0), ('.', 0)]
            ]
        }, 
    3: {
        'source': 'https://www.gastronom.ru/recipe/1128', 
        'name': 'Запеченная курица с апельсиновым соком', 
        'entries': [
            [('Посыпать', 1), ('курицу', 1), ('луком', 0), (',', 0), ('сверху', 0), ('положить', 0), ('кусочки', 0), ('масла', 0), ('.', 0)], 
            [('Запекать', 1), ('курицу', 1), ('30', 0), ('мин', 0), ('.', 0)], [('Полить', 1), ('курицу', 1), ('соусом', 0), ('и', 0), ('подать', 0), ('.', 0)]
            ]
        }, 
    4: {
        'source': 'https://www.gastronom.ru/recipe/1129', 
        'name': 'Вареная курица с имбирем, луком и кинзой', 
        'entries': [
            [('Снять', 0), ('с', 0), ('огня', 0), ('и', 0), ('дать', 1), ('курице', 1), ('остыть', 0), (',', 0), ('не', 0), ('вынимая', 0), ('ее', 0), ('из', 0), ('бульона', 0), ('.', 0)], 
            [('Вынуть', 1), ('курицу', 1), ('из', 0), ('кастрюли', 0), ('и', 0), ('нарезать', 0), ('небольшими', 0), ('кусочками', 0), ('.', 0)]
            ]
        } 
    }

# i - номер документа ()
# label - флажок для форматирования (можно забить)


# In[109]:


def search_info(search_result):
    search = {}
    n_sentences = len([' '.join([t[0] for t in entry]) for doc in search_result for entry in search_result[doc]['entries']])
    n_documents = len(search_result)
    n_entries = len([entry for doc in search_result for entry in search_result[doc]['entries']])
    search['documents'] = n_documents
    search['sentences'] = n_sentences
    search['entries'] = n_entries
    return search   


# In[111]:


print(search_info(example_search_result))


# # Функция 4

# In[85]:


# n_pp = {
#     '0': {'form': 'промыть'},
#     '1': {'form': 'курицу'},
#     '2': {'form': 'и'},
#     '3': {'form': 'порезать'},
# }
n_pp = {
    '0': {'form': 'в'},
    '1': {'upos': 'ADJ', 'Case': 'Acc'},
    '2': {'upos': 'ADJ', 'Case': 'Acc'},
    '3': {'form': 'страну'},
}


# In[81]:


css = {
    ('0', '1'): {'lindist': (1, 1)},
    ('1', '2'): {'lindist': (1, 1)},
    ('2', '3'): {'lindist': (1, 1)},
}


# In[82]:


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
            word = n_p['0']['form']
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
                    word = n_p[key1]['form']
                    from_ = cs[key2]['lindist'][0]
                    to = cs[key2]['lindist'][1]
                    result.append(f'{word}, на расстоянии от {from_} до {to} от Слова {key1}')
    return result


# In[86]:


print(query_info(n_pp, css))


# In[ ]:




