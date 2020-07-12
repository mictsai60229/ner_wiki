#!/bin/sh

wget https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-langlinks.sql.gz
wget https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-redirect.sql.gz
wget https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2

gunzip enwiki-latest-langlinks.sql.gz
gunzip enwiki-latest-redirect.sql.gz

./mysql2sqlite enwiki-latest-langlinks.sql > enwiki-latest-langlinks.sqlite3
./mysql2sqlite enwiki-latest-redirect.sql > enwiki-latest-redirect.sqlite3


python wikiextractor/WikiExtractor.py --process 20 -o enwiki-pages-articles --json -l enwiki-latest-pages-articles.xml.bz2
