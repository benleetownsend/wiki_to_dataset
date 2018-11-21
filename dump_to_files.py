import bz2
from gensim.corpora.wikicorpus import remove_markup, extract_pages
import tqdm
file_base = "wiki/Wikipedia_corpus_{}.txt"
file_num = 1
gen = extract_pages(bz2.BZ2File("enwiki-20180901-pages-articles-multistream.xml.bz2"))
with open("wiki/Wikipedia_titles.txt", "wt")  as titles:
    current_file = open(file_base.format(file_num), "wt")
    for title, page, idx in tqdm.tqdm(gen):
        try:
            start_pos = current_file.tell()
            current_file.write(remove_markup(page).strip())
            end_pos = current_file.tell()
            current_num = file_num
            if end_pos > 50000000:
                file_num += 1
                current_file = open(file_base.format(file_num), "wt")
            titles.write("{} {} {} {}\n".format(current_num, start_pos, end_pos, title))
        except Exception as ex:
            print(ex)

