import spacy

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

