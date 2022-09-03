import spacy

nlp = spacy.load('./saved_model')

def get_segment(sentence):
    doc = nlp(sentence)
    return [t.text for t in doc]

    # for t in doc:
    #     print(t.text, '\t', t.pos_, '\t', t.dep_, '\t', t.tag_, '\t', t.idx, '\t', t.i)

    # for named_entity in doc.ents:
    #     print(named_entity, named_entity.label_, named_entity.start, named_entity.end, named_entity.start_char)
    #     print(doc[named_entity.start])
    #     print(doc.text[named_entity.start_char])
    #     # print(doc[named_entity.sent.start_char])

