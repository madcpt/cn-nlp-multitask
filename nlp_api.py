from model.finetune_ner import parse_str, extract_components_from_root

# API: entry for word segmentation
def get_segment(sentence: str) -> [str]:
    doc = parse_str(sentence)
    return [t.text for t in doc]

# API: entry for goverment department NER
def recognize_gov_entities(sentence: str) -> [dict]:
    doc = parse_str(sentence)
    entities = []  # example: [{entity: “公安部门”, beginning_position: 0}] 
    for named_entity in doc.ents:
        if named_entity.label_ == 'gov':
            entities.append({
                'entity': named_entity.text,
                'beginning_position': named_entity.start_char,
            })
    return entities

# API: entry to parse and extract action, objective and modifier
def extract_components_from_sentence(sentence: str):
    doc = parse_str(sentence)
    root: Token = [t for t in doc if t.dep_ == 'ROOT'][0]
    components = extract_components_from_root(root, doc)
    return components
