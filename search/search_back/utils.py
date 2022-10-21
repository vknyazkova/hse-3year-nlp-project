def check_query(node_pattern, constraints):
    check_node_pattern(node_pattern)
    check_constraints(constraints)
    constr_nodes = set([n for p in constraints for n in p])
    nodes = set(node_pattern.keys())
    if not constr_nodes <= nodes:
        raise ValueError(f'Not all nodes from the constraints are defined in the node_pattern')
    return True


def check_node_pattern(node_pattern):
    NODES_FIELDS = {'form', 'lemma', 'upos', 'xpos', 'exclude'}
    AVAILABLE_CATEGORIES = {'PronType', 'Gender', 'VerbForm', 'NumType', 'Animacy', 'Mood', 'Poss', 'NounClass',
                            'Tense', 'Reflex', 'Number', 'Aspect', 'Foreign', 'Case', 'Voice', 'Abbr', 'Definite',
                            'Evident', 'Typo', 'Degree', 'Polarity', 'Person', 'Polite', 'Clusivity'}

    for n in node_pattern:
        npattern_fields = set(node_pattern[n].keys())
        if not npattern_fields <= (NODES_FIELDS | AVAILABLE_CATEGORIES):
            raise KeyError(
                f'Node_pattern can only include keys from this set: {NODES_FIELDS} or from the list of available '
                f'grammar categories from here: https://universaldependencies.org/u/feat/index.html')

        exclude_cat = node_pattern[n].get('exclude')
        if exclude_cat:
            if not isinstance(exclude_cat, list):
                raise TypeError('Exclude features should be given in a list')
            if not set(exclude_cat) <= AVAILABLE_CATEGORIES:
                raise ValueError(f'Wrong category name: {set(exclude_cat) - AVAILABLE_CATEGORIES}. Please use the same '
                                 f'names as in the UD: https://universaldependencies.org/u/feat/index.html')
    return True


def check_constraints(constraints):
    AVAILABLE_CATEGORIES = {'PronType', 'Gender', 'VerbForm', 'NumType', 'Animacy', 'Mood', 'Poss', 'NounClass',
                            'Tense', 'Reflex', 'Number', 'Aspect', 'Foreign', 'Case', 'Voice', 'Abbr', 'Definite',
                            'Evident', 'Typo', 'Degree', 'Polarity', 'Person', 'Polite', 'Clusivity'}
    CONSTRAINT_FIELDS = {'deprels', 'fconstraint', 'lindist'}
    FCONSTRAINT_FIELDS = {'disjoint', 'intersec'}

    for np in constraints:
        constr_types = set(constraints[np].keys())
        if not constr_types <= CONSTRAINT_FIELDS:
            raise KeyError(
                f'Wrong constraint type: {constr_types - CONSTRAINT_FIELDS}. Only {CONSTRAINT_FIELDS} can be used as '
                f'keys')

        fconstr = constraints[np].get('fconstraint')
        if fconstr:
            fconst_types = set(fconstr.keys())
            if not fconst_types <= FCONSTRAINT_FIELDS:
                raise KeyError(
                    f'Wrong feature constraint type {fconst_types - FCONSTRAINT_FIELDS}. It can be only: {FCONSTRAINT_FIELDS}')

            for fctype in fconstr:
                if not isinstance(fconstr[fctype], list):
                    raise TypeError(
                        f'{fctype} features should be a list of grammar categories not a {type(fconstr[fctype])}')
                if not set(fconstr[fctype]) <= AVAILABLE_CATEGORIES:
                    raise ValueError(
                        f'Wrong grammar category names: {set(fconstr[fctype]) - AVAILABLE_CATEGORIES}. Please use the '
                        f'same names as in the UD: https://universaldependencies.org/u/feat/index.html')
    return True


