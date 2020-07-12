import os
import json
import re

from bz2 import BZ2File
from collections import Counter, defaultdict
from urllib.parse import unquote

def extract_information(paragraph):

    res = {}
    title_match = re.search("<title>([^<]*?)</title>", paragraph)
    if title_match:
        res["title"] = title_match.group(1)
    else:
        res["title"] = ""
    
    id_match = re.search("<id>([^<]*?)</id>", paragraph)
    if id_match:
        res["id"] = id_match.group(1)
    else:
        res["id"] = ""
    
    text_match = re.search("<text[^>]*?>([^<]*?)</text>", paragraph)
    if text_match:
        res["text"] = text_match.group(1)
    else:
        res["text"] = ""
        
    return res
        



def pages_generator(file):
    with BZ2File(file, "r") as f:
        
        in_page = False
        for line in f:
            line = line.decode('utf-8')
            if not in_page:
                if re.search("<page>", line):
                    in_page = True
                    paragraph = line
            
            else:
                if re.search("</page>", line):
                    in_page = False
                    paragraph += line
                    yield extract_information(paragraph)
                else:
                    paragraph += line
            

def extract_first_paragraph(text):
    
    tags = "|".join(["{{", "}}", "\[\[", "]]"])
    
    for match in re.finditer("(.*\n)*?\n", text):
        
        value = match.group(0)
        stack = []
        res = ""
        start = 0
        
        
        for match in re.finditer(tags, value):
            if not stack:
                res += value[start:match.start()]
                start = match.end()
            else:
                start = match.end()
            
            if match.group(0) in ("{{", "[["):
                stack.append(match.group(0))
            elif stack:
                stack.pop()
        res += value[start:]
        
        res = res.strip()
        if res:
            return res   
    return ""
            
def search_bold(text):
    
    regex = "|".join(["'''(.*?)'''", '"""(.*?)"""'])
    
    res = set()
    for match in re.finditer(regex, text):
        res.add(match.group(1))
    
    return res


def extract_bold(filepath):
    
    page_ids = []
    page_bolds = []
    for page in pages_generator(filepath):
        pages_ids.append(, page['title'])
        
        first_paragraph = extract_first_paragraph(page['text'])
        bold_data = search_bold(first_paragraph)
            
        page_bolds[page['id']] = 
            
        print(page["id"], page["title"], json.dumps(list(bold_data), ensure_ascii=False), sep="\t", file=f)
    
    return page_bolds ,page_ids

def extract_redirects(filepath):
    pass

def extract_language_link(language="zh"):
    pass
    
def extract_anchor_frequency(datapath):
    
    tasks = (os.path.join(root, name) for root, dirs, files in os.walk(datapath, topdown=False) for name in files)
    wiki_paragraphs = (json.loads(line) for file in tasks for line in open(file))
    
    
    anchor_count = defaultdict(Counter)
    regex = '<a href="([^"]*?)">([^<]*?)</a>'
    
    count = 0
    for wiki_paragraph in wiki_paragraphs:
        
        
        
        content = wiki_paragraph ['text']
        used_title = set()
        for match in re.finditer(regex, content):
            link = unquote(match.group(1))
            anchor = match.group(2)

            if link in used_title:
                continue

            used_title.add(link)
            anchor_count[anchor][link] += 1
       
        count += 1
        if count % 10000 == 0:
            print("Preprocess {} wiki pages".format(count))
    
    return anchor_count

def output_page_id(page_ids, filepath="enwiki-pageid.tsv"):
    
    with open(filepath, "w") as f:
        wikipages = list(page_ids.items())
        wikipages.sort(key=lambda x: x[0])
        
        for page_id, title in wikipages:
            print(page_id, title, sep="\t", file=f)
            



if __name__ == "__main__":
    
    
    anchor_count, page_ids = extract_anchor_frequency("enwiki-pages-articles")
    output_page_id(page_ids)
    
    redirects = extract_redirects("enwiki-latest-redirect.tsv", page_ids)
    
    
    