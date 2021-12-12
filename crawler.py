import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import threading

# the Crawler class


class Crawler(threading.Thread):

    # initializing the number of pages to be crawled, if the data should be saved,
    # the starting url, the links to crawl, a list that keeps track of
    # the visited urls and the url lock
    def __init__(self, url, links_list, visited, max_pages, url_lock):
        threading.Thread.__init__(self)
        print(f"Web Crawler worker {threading.current_thread()} has Started")
        self.max_pages = max_pages
        self.url = url
        self.links_list = links_list
        self.visited = visited
        self.url_lock = url_lock

    # the run function that's in charge of the process of crawling
    def run(self):

        while True:
            # we create a global lock on our queue of links so that no two threads can access the queue at same time
            self.url_lock.acquire()
            link = self.links_list.get()
            self.url_lock.release()

            # if the link is None the queue is exhausted or the threads are yet, process the links
            if link is None:
                continue

            # if the link is already visited, we break the execution
            if link in self.visited:
                continue

            try:
                # This method constructs a full URL by combining the base url with other url.
                # This uses components of the base URL, the network
                # location and  the path, to provide missing components in the relative URL.
                link = urljoin(self.url, link)

                res = requests.get(link)
                html_page = res.content
                if len(self.visited) >= self.max_pages:
                    break
                # this returns the html representation of the webpage
                soup = BeautifulSoup(html_page, "html.parser")

                # in case we are finding all the links in the page
                for a_tag in soup.find_all('a'):
                    # checking if the link has been visited
                    if (a_tag.get("href") not in self.visited):
                        self.links_list.put(a_tag.get("href"))

                print(f"Adding {link} to the crawled list")
                self.visited.add(link)
                text = soup.get_text()

                title = link  # get the title of the current page.
                title = title.replace("\n", "")  # removing all the unnecessary things from the title
                title = title.replace("\r", "")
                title = title.replace("\t", "")
                title = title.replace("|", "")
                title = title.replace(":", "")
                title = title.replace("/", "")
                title = title.strip(' ')
                print(title)
                # creates a txt file with the name of the page
                file = open(".\\files\\" + title + ".txt", "w", encoding='utf-8')
                file.write(text)
            # ending the crawling task
            finally:
                self.links_list.task_done()
