import spacy
from spacy.tokens.token import Token
from spacy.tokens.span import Span
from spacy.tokens.doc import Doc


SUBJ = 'nsubj, nsubj:xsubj, nsubjpass'
OBJ = 'dobj'
MODIFIER = 'amod, appos, nmod, nmod:assmod, nmod:poss, nmod:prep, nmod:range, nmod:tmod, nmod:topic, nummod, acl'


# unzip from `saved_model.zip`
nlp = spacy.load('./saved_model')

def get_segment(sentence: str) -> [str]:
    doc = nlp(sentence)
    return [t.text for t in doc]

def recognize_gov_entities(sentence: str) -> [dict]:
    doc = nlp(sentence)
    entities = []  # example: [{entity: “公安部门”, beginning_position: 0}] 
    for named_entity in doc.ents:
        if named_entity.label_ == 'gov':
            entities.append({
                'entity': named_entity.text,
                'begining_position': named_entity.start_char,
            })
    return entities

def _subtree_boundary(node: spacy.tokens.token.Token, exclude: spacy.tokens.token.Token = None):
    children = list(node.children)
    if exclude and exclude in children:
        children = children[children.index(exclude)+1:]

    if len(children) == 0:
        return None, None

    start_idx = _subtree_boundary(children[0])[0] \
                    if children[0].n_lefts + children[0].n_rights > 0 \
                    else min(node.i, children[0].i)
    end_idx = _subtree_boundary(children[-1])[1] \
                if children[-1].n_lefts + children[-1].n_rights > 0 \
                else max(node.i, children[-1].i)+1

    return start_idx, end_idx

def _dependency_analysis(root: Token, subj_start: int, subj_end: int):
    # print(type(root), root.n_lefts, root.n_rights)
    subj, obj, mod = None, None, None
    for child in root.children:
        if child.dep_ in SUBJ and not subj:
            tree_start, tree_end = _subtree_boundary(child)
            # print('subj', child, tree_start, tree_end)
            if tree_start < subj_end or tree_end > subj_start:
                subj = child
        # print('obj', child.dep_, child.dep_ in OBJ)
        if child.dep_ in OBJ and not obj:
            obj = child
    if (not subj) or (not obj):
        return None, None
    if subj and obj:
        for child in obj.children:
            if child.dep_ in MODIFIER and not mod:
                mod = child
    if not mod:
        return None, None
    return obj, mod

def _extract_components_from_root(root: Token, doc: [Doc]) -> [dict]:
    # an example of components: 
    # [
    #   {action: “打击“, action_position: 6, object: “违法犯罪活动“, object_position: 22,
    #       modifier: “利用黑客手段提供有偿“刷课”服务”, modifier_position: 8},
    # ]
    components = []

    # when root is not an action:
    if root.pos_ != 'VERB':
        return components

    for ent in doc.ents:
        if ent.label_ == 'gov':
            obj, mod = _dependency_analysis(root, ent.start, ent.end)
            if obj and mod:
                obj_start, obj_end = _subtree_boundary(obj, exclude=mod)
                mod_start, mod_end = _subtree_boundary(mod)
                components.append({
                    'action': root.text,
                    'action_position': root.idx,
                    'object': doc[obj_start: obj_end].text,
                    'object_position': doc[obj_start].idx,
                    'modifier': doc[mod_start: mod_end].text,
                    'modifier_position': doc[mod_start].idx,
                })

    return components

def extract_components_from_sentence(sentence: str):
    doc = nlp(sentence)
    root: spacy.tokens.token.Token = [t for t in doc if t.dep_ == 'ROOT'][0]
    components = _extract_components_from_root(root, doc)
    return components
