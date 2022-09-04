# mini-project on Chinese NLP

## containerized http service

`docker build -t nlp:v1 . && docker run --rm -it --name nlp-service -p 0.0.0.0:8001:8001 nlp:v1`


## Components

### HTML parsing and database
see `scripts/step1-build_database.ipynb`

- simply load the excel file, then use `BeautifulSoup` to parse html text;
- use `sqlite3` as embedded db, dump db file as `data/data.db`;
- store parsed `title`, `published_date` and `content` into db;


### Word Segmentation
Word segmentation is directed built from [spacy's `zh_core_web_md` model](https://spacy.io/models/zh#zh_core_web_md).

- use `spacy` because it is an efficient multitask NLP framework;
  - note that I chose version `2.3.0` over `3.x` because the latest version reports unkown bug in NER fine-tuning;
- there are four chinese models available, chose [`zh_core_web_md`](https://github.com/explosion/spacy-models/releases/tag/zh_core_web_md-2.3.0) because it achieves a balance between model size and performance;
- model `zh_core_web_md==2.3.0` uses [`jieba`](https://github.com/fxsjy/jieba) as segmentor;

#### Error Analysis and Ideas
an example for imperfect word segmentation:
```
Input: 国务院关税税则委员会按程序决定，对相关商品延长排除期限。
output:  ['国务院', '关税税', '则', '委员会', '按', '程序', '决定', '，', '对', '相关', '商品', '延长', '排除', '期限', '。']
```

Since `jieba` was intruduced many years ago, I further tested the same input on [`pkuseg`](https://github.com/lancopku/pkuseg-python), a more recent segmentor:

```
pkuseg output: ['国务院', '关税税', '则', '委员会', '按', '程序', '决定', '，', '对', '相关', '商品', '延长', '排除', '期限']
```

which did not really seem better...


### NER on goverment departments
train code pls refer to `step2-train_ner.py`

1. source of labeled data: [CLUENER2020](https://github.com/CLUEbenchmark/CLUENER2020);
2. extract entities with label `gov`;
3. train NER pipeline based on [spacy's `zh_core_web_md` model](https://spacy.io/models/zh#zh_core_web_md);

To avoid training upon each deployment, I have trained and dumpped the model in `saved_model.zip` (tracked and managed by git-lfs).

After 10 iterations of training, the pipeline was able to recognize '公安部门' and even complex entity like '省级住房和城乡建设、水利、财政部门'.

#### Error Analysis and Ideas
Segmentation error can leads to NER error. use the same example as in Task 1:
```
Input: 国务院关税税则委员会按程序决定，对相关商品延长排除期限。
TASK1: SEG {'segment': ['国务院', '关税税', '则', '委员会', '按', '程序', '决定', '，', '对', '相关', '商品', '延长', '排除', '期限', '。']}
TASK2: NER {'entities': [{'entity': '国务院', 'beginning_position': 0}, {'entity': '委员会', 'beginning_position': 7}]}
```
where gold prediction should be '国务院关税税则委员会'. NER could possibly perform better on this sample with a better segmentor.


### Identify action, the object of the action, and the modifier of the object given the subject is a department.

After reading materials on [dependency parsing](https://web.stanford.edu/~jurafsky/slp3/14.pdf), I decided to build a rule-based dependency parser.

Everything related is packed and well-annotated in `model/finetune_ner.py`. Key functions:
- `_subtree_boundary`;
- `_dependency_analysis`;
- `extract_components_from_root`;

## Error Analysis
In the following example, SEG and NER looks fine, but failed to find action, object and modifer:
```
Input: 公安部门依法打击利用黑客手段提供有偿“刷课”服务违法犯罪活动
TASK1: SEG {'segment': ['公安', '部门', '依法', '打击', '利用', '黑客', '手段', '提供', '有偿', '“', '刷课', '”', '服务', '违法', '犯罪', '活动']}
TASK2: NER {'entities': [{'entity': '公安部门', 'beginning_position': 0}]}
TASK3: DEP {'components': []}
```

It could be that the object and modifer are too long and ambiguous. After replacing '提供有偿“刷课”服务' with '的', the sentence seems to make more sense, and the parser managed to give a better result:
```
Input: 公安部门依法打击利用黑客手段的违法犯罪活动
TASK1: SEG {'segment': ['公安', '部门', '依法', '打击', '利用', '黑客', '手段', '的', '违法', '犯罪', '活动']}
TASK2: NER {'entities': [{'entity': '公安部门', 'beginning_position': 0}]}
TASK3: DEP {'components': [{'action': '打击', 'action_position': 6, 'object': '违法犯罪活动', 'object_position': 15, 'modifier': '利用黑客手段的', 'modifier_position': 8}]}
```

The dependency tree looks like:

[dep](./img/dep.svg)