import urllib.request
import zipfile
import json
import spacy
import random


### download labeled data from CLUENER2020
filehandle, _ = urllib.request.urlretrieve('https://storage.googleapis.com/cluebenchmark/tasks/cluener_public.zip')
zip_file_object = zipfile.ZipFile(filehandle, 'r')

### extract entities with label `gov`
TRAIN_DATA = []
for filename in ['train.json', 'dev.json']:
    file = zip_file_object.open(filename)
    for line in file.readlines():
        data = json.loads(line)
        if 'government' in data['label']:
            # example of data:
            # {'text': '会议批准了中国与欧盟海军、多国海上力量和北约等就在“国际推荐通行走廊”', 'label': {'government': {'中国与欧盟海军': [[5, 11]], '北约': [[20, 21]]}}}
            entities = []
            for _, ind in data['label']['government'].items():
                for start, end in ind:
                    entities.append((start, end+1, 'gov'))
            TRAIN_DATA.append((data['text'], {'entities': entities}))

## example of TRAIN_DATA:
# TRAIN_DATA =  [
#     ("公安部门依法打击利用黑客手段提供有偿“刷课”服务违法犯罪活动", {'entities': [(0, 4, 'gov')]}),
# ]
print('length of TRAIN_DATA:', len(TRAIN_DATA))


# need to download at the first time, use the following command:
# `python3 -m spacy download zh_core_web_md`
nlp = spacy.load('zh_core_web_md')

# add new label `gov` to NER pipeline
nlp.get_pipe('ner').add_label('gov')

# disable other pipes during training
other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
with nlp.disable_pipes(*other_pipes):  # only train NER
    optimizer = nlp.begin_training()
    for itn in range(10):
        print("Statring iteration " + str(itn))
        random.shuffle(TRAIN_DATA)
        losses = {}
        for text, annotations in TRAIN_DATA:
            nlp.update(
                [text],  # batch of texts
                [annotations],  # batch of annotations
                drop=0.2,  # dropout - make it harder to memorise data
                sgd=optimizer,  # callable to update weights
                losses=losses)
        print('loss', losses)

# save model to directory `saved_model`
nlp.to_disk('./saved_model')
