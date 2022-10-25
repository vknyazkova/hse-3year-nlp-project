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
                    elif len(tag) == 1 and tag[0] == 'lemma' :
                        word = n_p[key1][tag[0]]
                        from_ = cs[key2]['lindist'][0]
                        to = cs[key2]['lindist'][1]
                        result.append(f'{word}, на расстоянии от {from_} до {to} от Слова {key1}')
                    else:
                        word = '_'
                        result.append(word)
    return result
