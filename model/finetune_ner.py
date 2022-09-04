import spacy
from spacy.tokens.token import Token
from spacy.tokens.span import Span
from spacy.tokens.doc import Doc
from typing import Optional


SUBJ = 'nsubj, nsubj:xsubj, nsubjpass'
OBJ = 'dobj'
MODIFIER = 'amod, appos, nmod, nmod:assmod, nmod:poss, nmod:prep, nmod:range, nmod:tmod, nmod:topic, nummod, acl'


# unzip from `saved_model.zip`
nlp = spacy.load('./saved_model')

def parse_str(sentence: str) -> Doc:
    return nlp(sentence)

def _subtree_boundary(node: Token, exclude: Optional[Token] = None) \
        -> (Optional[int], Optional[int]):
    ### this function returns the left and right boundary (word index) of all leaves under node
    # input:
    #   - node:
    #   - exclude: only count leaves on the right of this node
    # output: 
    #   - start_idx: left boundary of all leaves
    #   - end_idx: right boundary of all leaves
    ###

    # get children and only keep right side of `exclude` node
    children = list(node.children)
    if exclude and exclude in children:
        children = children[children.index(exclude)+1:]

    if len(children) == 0:
        return None, None

    # if node has children -> recursively find start_idx of first child
    # otherwise -> return index of first child
    # need to take min with node itself in case all nodes are on the right side
    start_idx = min(node.i,
                    _subtree_boundary(children[0])[0]
                        if children[0].n_lefts + children[0].n_rights > 0
                        else children[0].i
                    )
    # same for end_idx
    end_idx = max(node.i + 1,
                      _subtree_boundary(children[-1])[1] \
                          if children[-1].n_lefts + children[-1].n_rights > 0 \
                          else children[-1].i + 1
                     )
    return start_idx, end_idx

def _dependency_analysis(root: Token, subj_start: int, subj_end: int) \
        -> (Optional[Token], Optional[Token]):
    ### this function returns the root node (action) of object and object-modifier
    # input:
    #   - root: root node of dependency tree, regarded as action
    #   - subj_start: left boundary of subject subtree
    #   - subj_end: right boundary of subject subtree
    # output: 
    #   - obj: object node
    #   - mod: object-modifier node
    ###

    subj, obj, mod = None, None, None

    # find subj and obj node
    for child in root.children:
        # find subj with predefined depenency types
        if child.dep_ in SUBJ and not subj:
            # consider as subj node only if the boundary
            # of `child` overlapes with [subj_start, subj_end]
            tree_start, tree_end = _subtree_boundary(child)
            if tree_start < subj_end or tree_end > subj_start:
                subj = child
        # find obj with predefined depenency types
        if child.dep_ in OBJ and not obj:
            obj = child

    # continue to find `mod` only if both subj and obj are valid
    if (not subj) or (not obj):
        return None, None

    # find modifer node amond `obj.children`, also based on predefined depenency types
    for child in obj.children:
        if child.dep_ in MODIFIER and not mod:
            mod = child

    ## only return obj when mod is also valid
    # if not mod:
    #     return None, None

    return obj, mod

def extract_components_from_root(root: Token, doc: Doc) -> [dict]:
    ### this function returns the components given root node and spacy doc
    #
    # input:
    #   - root: root node of dependency tree
    #   - doc: sentence in form of spacy doc
    # output: 
    #   - components:
    #       an example of components: 
    #       ```
    #       [
    #         {
    #            action: "打击",
    #            action_position: 6,
    #            object: "违法犯罪活动",
    #            object_position: 22,
    #            modifier: "利用黑客手段提供有偿“刷课”服务",
    #            modifier_position: 8
    #         },
    #       ]
    #       ```
    ###

    components = []

    # check that root is an action node:
    if root.pos_ != 'VERB':
        return components

    # 1. traverse through all named entities, find entities with label `gov`;
    # 2. treat entity as potential subject, find obj and mod with `_dependency_analysis()`;
    # 3. if obj is found, add corresponding info into `components`;
    # note that `mod` can be None, since it does not always exists;
    for ent in doc.ents:
        if ent.label_ != 'gov':
            continue

        obj, mod = _dependency_analysis(root, ent.start, ent.end)
        if not obj:  # not valid
            continue

        obj_start, obj_end = _subtree_boundary(obj, exclude=mod)
        if mod:
            mod_start, mod_end = _subtree_boundary(mod)
        components.append({
            'action': root.text,
            'action_position': root.idx,
            'object': doc[obj_start: obj_end].text,
            'object_position': doc[obj_start].idx,
            'modifier': doc[mod_start: mod_end].text if mod else None,
            'modifier_position': doc[mod_start].idx if mod else None,
        })

    return components
