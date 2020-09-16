from multiworkers import multiworkers

from extract import pages_generator, extract_bold

save_file = "zhwiki-latest-bold.tsv"
pages = pages_generator("zhwiki-latest-pages-articles-multistream.xml.bz2")


if __name__ == "__main__":
    #func, task_list, save_file, workers=10
    multiworkers(extract_bold, pages, save_file, 50)