import os
import json

from .load_redirect import REDIRECT_TABLE
from .load_bold import BOLD_TABLE


BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DATA_DIR = os.path.join(BASE_DIR, "collect_data")

class anchor_table(object):
    
    def __init__(self, document_count=10**6):
        
        self.document_count = document_count
        self.anchor2count = {}
        self.document_frequency = {}
        self.load_anchor()
        
        
    def load_anchor(self, file="enwiki-latest-anchor.temp", headers=True):
        
        anchor_file = os.path.join(DATA_DIR, file)
        
        with open(anchor_file, errors='replace') as infile:
            
            if headers:
                line = next(infile)
                self.document_count = int(line.strip())
                
            
            for line in infile:
                
                items = line.strip().split("\t", 1)
                if len(items) == 1:
                    continue
                key, value = items
                
                link_count = json.loads(value)
                
                link_count = self._noramlize_redirect(link_count)
                self.document_frequency[key] = sum(link_count.values())
                
                self.anchor2count[key] = link_count
                
    def get_inverse_documnet_frequency(self, text):
        
        return self.document_count / self.document_frequency.get(text, 1)
     
                
    def _normalize_title(self, title):
        
        end_idx = title.find("#")
        if end_idx != -1:
            title = title[:end_idx]
        
        if not title:
            return ""
            
        title = title.replace("_", " ")
        title = title[0].upper() + title[1:]
        return title
    
    def _noramlize_redirect(self, link_count):
        
        new_link_count = {}
        for key, value in link_count.items():
            if key.startswith("http"):
                continue
            
            key = self._normalize_title(key)
            if not key:
                continue
                
            if key in REDIRECT_TABLE.redirect2id:
                wikiid = REDIRECT_TABLE.redirect2id[key]
            else:
                if key in BOLD_TABLE.title2id:
                    wikiid = BOLD_TABLE.title2id[key]
                else:
                    continue
                
            
            count = new_link_count.get(wikiid, 0)
            new_link_count[wikiid] = count+value
        
        return new_link_count
            
        
                

ANCHOR_TABLE = anchor_table()