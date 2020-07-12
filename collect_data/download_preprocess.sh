#!/bin/sh

wget https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-langlinks.sql.gz
wget https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-redirect.sql.gz
wget https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2

gunzip enwiki-latest-langlinks.sql.gz
gunzip enwiki-latest-redirect.sql.gz


./mysql2sqlite enwiki-latest-langlinks.sql | (cat && echo "select * from langlinks;") | sqlite3 -header -csv -separator $'\t' | sed -e '1,2d' > enwiki-latest-langlinks.tsv
./mysql2sqlite enwiki-latest-redirect.sql | (cat && echo "select * from redirect;") | sqlite3 -header -csv -separator $'\t' | sed -e '1,2d' > enwiki-latest-redirect.tsv


python wikiextractor/WikiExtractor.py --process 20 -o enwiki-pages-articles --json -l enwiki-latest-pages-articles.xml.bz2