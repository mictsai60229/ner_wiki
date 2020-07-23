import os
from typing import List, Tuple


from load_data import load_bold, load_redirect, load_anchor


def disambiguate_NE(entity: str):
    
    title_result = check_title(entity)
    
    redirect_result = check_redirect(entity)
    
    bold_result = check_bold(entity)
    
    anchor_result = check_anchor(entity)
    
    return {'title': title_result, 'redirect': redirect_result, 'bold': bold_result, 'anchor': anchor_result}
    

    
def check_title(text: str) -> int:
    return load_bold.BOLD_TABLE.title2id.get(text, -1)

def check_redirect(text: str) -> int:
    
    return load_redirect.REDIRECT_TABLE.redirect2id.get(text, -1)

def check_bold(text: str) -> List[int]:
    return load_bold.BOLD_TABLE.bold2id.get(text, [])

def check_anchor(text: str) -> List[Tuple[int, int]]:
    return load_anchor.ANCHOR_TABLE.anchor2count.get(text, [])
    
def _id2title(wikiid: int) -> str:
    return load_bold.BOLD_TABLE.id2title.get(wikiid, "")
    


