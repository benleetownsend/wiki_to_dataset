import os
import json
import tqdm

class WikiGraph:
    def __init__(self, dir):
        self.dir = dir
        with open(os.path.join(dir, "interlinks.json"), "rt") as fp:
            graph = (l.split("\t", 1) for l in fp)
            self.graph = {k: json.loads(v) for k, v in tqdm.tqdm(graph)}
        with open(os.path.join(dir, "Wikipedia_titles.txt"), "rt") as fp:
            lookup = (l.split(" ", 3) for l in fp)
            self.lookup = {k.strip(): (file, int(start), int(end)) for file, start, end, k in tqdm.tqdm(lookup)}
        
    def text_from_title(self, title):
        file, start, end = self.lookup[title]
        with open(os.path.join(self.dir, "Wikipedia_corpus_{}.txt".format(file)), "rt") as fp:
            fp.seek(start)
            return fp.read(start - end)

    def pages_from(self, base_title, visited=None):
        if visited is None:
            yield base_title
            visited = []

        if base_title not in visited:
            visited.append(base_title)
            for title in self.graph.get(base_title, []):
                if title in visited:
                    continue
                yield title
                
            for title in self.graph.get(base_title, []):
                yield from self.pages_from(title, visited)
    def get_dataset(self, seed, num_chars=10000000):
        page_name_gen = self.pages_from(seed)
        dataset = ""
        for page in page_name_gen:
            dataset += self.text_from_title(page)
            if len(dataset) > num_chars:
                return dataset[:num_chars]
        raise Exception("Not enough data")
    

print(WikiGraph("./wiki").get_dataset("Hammurabi"))
