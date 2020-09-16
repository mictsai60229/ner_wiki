# Chinese_Wikipedia_data

This project is used to preprocess Wikipedia data for named entity disambiguation.
I also created a simple disambiguate method in ```disambigaute_named_entity.py```.

## Required packages or tools

Before start on this project, you need to make sure that you have these packages or tools.

* [sqlite3](https://www.sqlite.org/download.html)
* [WikiExtractor](https://github.com/attardi/wikiextractor)
* [mysql2sqlite](https://github.com/dumblob/mysql2sqlite)

## Download and preprocess data

1. Download Wikipedia data
```shell
wget https://dumps.wikimedia.org/zhwiki/latest/zhwiki-latest-redirect.sql.gz
wget https://dumps.wikimedia.org/zhwiki/latest/zhwiki-latest-pages-articles.xml.bz2
```

2. Generate Wikipedia redirect file 

```shell
gunzip enwiki-latest-redirect.sql.gz
./mysql2sqlite enwiki-latest-redirect.sql > enwiki-latest-redirect.sqlite3 | (cat && echo "select * from redirect;") | sqlite3 -header -separator $'\t' | sed -e '1,2d' > zhwiki-latest-redirect.tsv
```
The output **zhwiki-latest-redirect.tsv** should be a file like:

| rd_from        | rd_namespace           | rd_title  | rd_interwiki | rd_fragment |
| ------ |:--------:| -----:|  -----:| -----:|
| 173 | 0 | "Linux内核" | "" | "" |
| 175 | 0 | Linux | "" | "" |
| 233 | 2 | Mountain | "" | "" |


3. Generate Wikipedia anchor data

First, preprocess Wikipedia data by **WikiExtractor**.
```
python wikiextractor/WikiExtractor.py --process 20 -o zhwiki-pages-articles --json -l zhwiki-latest-pages-articles.xml.bz2
```
It will then generate **zhwiki-pages-articles** directory with preprocess Wikipedia data.

4. Generate bold data
Go to **collect_data** directory, then execute

```
python gen_bold.py
```
It will generate file **zhwiki-latest-bold.tsv**.

5. Generate anchor data
In **collect_data** directory, then execute, then execute
```
python gen_anchor.py
```
It will then generate file **zhwiki-latest-anchor.tsv**.






