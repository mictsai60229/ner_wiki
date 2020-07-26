import os
import csv


BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DATA_DIR = os.path.join(BASE_DIR, "collect_data")

class bold_table(object):
    
    def __init__(self):
        
        self.id2title = {}
        self.title2id = {}
        
        self.disambiguate_pages = set()
        
        self.id2bold = {}
        self.bold2id = {}
        
        self.load_bold()
        
        
    def load_bold(self, file="enwiki-latest-bold.tsv", headers=False):
        
        bold_file = os.path.join(DATA_DIR, file)
        
        
        with open(bold_file, errors='replace') as csvfile:
            
            spamreader = csv.reader(csvfile, delimiter='\t')
            
            if headers:
                next(spamreader, None)
            
            for row in spamreader:
                
                wikiid, title, is_disambiguate, bold = row
                
                if ":" in title:
                    continue
                
                wikiid = int(wikiid)
                if is_disambiguate == "True" or '(disambiguation)' in title:
                    self.disambiguate_pages.add(wikiid)
                title = self._normalize_title(title)
                
                wikiid = int(wikiid)
                
                self.id2title[wikiid] = title
                self.id2bold[wikiid] = bold
                
                self.title2id[title] = wikiid
                    
                    
                self.id2bold[wikiid] = bold
                for text in bold:
                    if not text:
                        continue
                    
                    if text not in self.bold2id:
                        self.bold2id[text] = [wikiid]
                    else:
                        self.bold2id[text].append(wikiid)
                #self.title2id[title] = wikiid
                
    def _normalize_title(self, title):
        return title.replace("_", " ")
    
    def _remove_class(self, title):
        ridx = title.rfind("(")
        return title if ridx == -1 else title[:ridx-1]
                

BOLD_TABLE = bold_table()