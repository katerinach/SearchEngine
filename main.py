
import indexer
import crawler
import queue
import threading
import os
import queryprocessor


# os.mkdir(".\\files")
url = "https://www.auth.gr/" # url
links_to_crawl = queue.Queue()
url_lock = threading.Lock()
links_to_crawl.put(url)
crawler_threads = []
pages = int(input("Give the number of pages to crawl:"))  # number of pages to iterate
save = 0  # keep last data or delete it (1 = keep, 0 = delete)
num_of_threads = int(input("Give the number of threads:"))# number of threads
visited = set()
if save == 0:  # if the user requested to restart the crawler and delete all the previous data
    for f in os.listdir(".\\files\\"):  # delete all the txt files
        if not f.endswith(".txt"):
            continue
        os.remove(os.path.join(".\\files\\", f))
if not url.startswith("http"):
    url = "http://" + url
for i in range(int(num_of_threads)):
    MyCrawler = crawler.Crawler(url, links_to_crawl, visited, pages, save, url_lock)
    MyCrawler.start()
    crawler_threads.append(MyCrawler)
for crawler in crawler_threads:
    crawler.join()
print(f"Total Number of pages visited are {len(visited)} using {num_of_threads} threads")
df_count, num_of_words_in_docs, indexer_copy = indexer.Indexer()
query = queryprocessor.queryProcessor()
query_results = query.process_query("νησίδες α.π.θ.", pages, df_count, num_of_words_in_docs, indexer_copy)
#query results contains a list of each document name and its score sorted

