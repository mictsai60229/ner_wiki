import os
import csv


BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DATA_DIR = os.path.join(BASE_DIR, "collect_data")

class redirect_table(object):
    
    def __init__(self):
        self.load_redirect()
        
        
    def load_redirect(self, file="enwiki-latest-redirect.tsv", headers=True):
        
        redirect_file = os.path.join(DATA_DIR, file)
        self.id2redirect = {}
        self.redirect2id = {}
        
        with open(redirect_file, errors='replace') as csvfile:
            
            spamreader = csv.reader(csvfile, delimiter='\t')
            
            if headers:
                next(spamreader, None)
            
            for row in spamreader:
                
                wikiid, _, redirect, _, _ = row
                redirect = self._normalize_title(redirect)
                wikiid = int(wikiid)

                
                if wikiid not in self.id2redirect:
                    self.id2redirect[wikiid] = [redirect]
                else:
                    self.id2redirect[wikiid].append(redirect)
                    
                self.redirect2id[redirect] = wikiid
                
    def _normalize_title(self, title):
        return title.replace("_", " ")
                

REDIRECT_TABLE = redirect_table()