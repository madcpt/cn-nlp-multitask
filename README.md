# mini-project on Chinese NLP

## containerized http service

`docker build -t nlp:v1 . && docker run --rm -it --name nlp-service -p 0.0.0.0:8001:8001 nlp:v1`


## Components

### HTML parsing and database
see `scripts/step1-build_database.ipynb`


### Word Segmentation
Word segmentation is directed built from [spacy's `zh_core_web_md` model](https://spacy.io/models/zh#zh_core_web_md).


### NER on goverment departments
train code pls refer to `step2-train_ner.py`

1. source of labeled data: [CLUENER2020](https://github.com/CLUEbenchmark/CLUENER2020);
2. extract entities with label `gov`;
3. train NER pipeline based on [spacy's `zh_core_web_md` model](https://spacy.io/models/zh#zh_core_web_md);

To avoid training upon each deployment, I have trained and dumpped the model in `saved_model.zip` (tracked and managed by git-lfs).



