from extract import extract_anchor_frequency, anchor_file_generator
from multiworkers import anchor_multiworkers


save_file = "zhwiki-latest-anchor.tsv"
pages = anchor_file_generator("zhwiki-pages-articles/")



if __name__ == "__main__":
    anchor_multiworkers(extract_anchor_frequency, pages, save_file, 50)