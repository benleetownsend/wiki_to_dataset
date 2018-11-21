import bz2
from gensim.corpora.wikicorpus import remove_markup, extract_pages, find_interlinks
import tqdm
import json
file_base = "wiki/interlinks.json"
interlinks=dict()
gen = extract_pages(bz2.BZ2File("enwiki-20180901-pages-articles-multistream.xml.bz2"))
with open(file_base, "wt") as fp:
    try:
        for title, text, _ in tqdm.tqdm(gen):
            try:
                fp.write("{}\t{}\n".format(title, json.dumps(list(find_interlinks(text).keys()))))
            except Exception as ex:
                print(ex)
    except Exception as ex:
        print(ex)                

