# mini-project on Chinese NLP

## containerized http service

`docker build -t nlp:v1 . && docker run --rm -it --name nlp-service -p 0.0.0.0:8001:8001 nlp:v1`


## Components

### HTML parsing and database
see `scripts/step1-build_database.ipynb`

### NER on goverment departments
see `step2-train_ner.py`

1. source of labeled data: [CLUENER2020](https://github.com/CLUEbenchmark/CLUENER2020);
2. extract entities with label `gov`;
3. 
