import os
import csv


BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DATA_DIR = os.path.join(BASE_DIR, "collect_data")

class langlinks_table(object):
    
    def __init__(self, tgt_lang="zh"):
        self.load_langlinks(tgt_lang)
        
        
    def load_langlinks(self, tgt_lang, file="enwiki-latest-langlinks.tsv", headers=True):
        
        langlinks_file = os.path.join(DATA_DIR, file)
        self.id2title = {}
        self.title2id = {}
        
        with open(langlinks_file, errors='replace') as csvfile:
            
            spamreader = csv.reader(csvfile, delimiter='\t')
            
            if headers:
                next(spamreader, None)
            
            for row in spamreader:
                
                wikiid, lang, title = row
                title = self._strip_title(title)
                wikiid = int(wikiid)
                
                if lang != tgt_lang:
                    continue
                
                self.id2title[wikiid] = title
                self.title2id[title] = wikiid
                
    def _strip_title(self, title):
        return title.strip("\"")
                

LANGLINKS_TABLE = langlinks_table('zh')