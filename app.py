from flask import Flask, render_template, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_bootstrap import Bootstrap
import indexer
import crawler
import queue
import threading
import queryprocessor
import os


""" This script is the main flask app and its responsible for 
running the search page on a local server"""

app = Flask(__name__)

if __name__ == '__main__':
    app.run(use_reloader=False,debug=True)

# initializing the url from user's input
url = "https://www.auth.gr/"
links_list = queue.Queue()  # a queue to save the links that we find to crawl next
url_lock = threading.Lock()  # threading lock
links_list.put(url)  # we put the base url in the links list
crawler_threads = []  # list to save the threads


pages = int(input("Give the number of pages to crawl:"))  # number of pages to iterate
save = 0  # keep last data or delete it (1 = keep, 0 = delete)
num_of_threads = int(input("Give the number of threads:"))  # number of threads
visited = set()  # list of already visited urls
if save == 0:  # if the user requested to restart the crawler and delete all the previous data
    for f in os.listdir(".\\files\\"):  # delete all the txt files
        if not f.endswith(".txt"):
            continue
        os.remove(os.path.join(".\\files\\", f))
if not url.startswith("http"):
    url = "http://" + url

#  for each of the number of threads we call a crawler giving the corresponding data so
#  every next crawler, can find data without crawling the same pages.
for i in range(int(num_of_threads)):
    MyCrawler = crawler.Crawler(url, links_list, visited, pages, url_lock)
    MyCrawler.start()  # start the crawler
    crawler_threads.append(MyCrawler)  # append the crawler to the list wih the threads
for crawler in crawler_threads:
    crawler.join()
print(f"Total Number of pages visited are {len(visited)} using {num_of_threads} threads")

#  calling the indexer and getting a list the total amount of each word in the documents,
#  a list with the number of words that each document has, and a copy of the indexer
df_count, num_of_words_in_docs, indexer_copy = indexer.Indexer()

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

Bootstrap(app)

#  class that represents a search flask form containing a text fiend to enter a query, and a search button.
class SearchForm(FlaskForm):
    query = StringField('query')
    search = SubmitField('search')

#  main route for the flask app. Its the home page that contains the search form.
@app.route("/", methods=["GET", "POST"])  # its methods are POST, and GET since its a from
def search():
    form = SearchForm()  # creating a form class
    if form.is_submitted():  # if the form is submitted
        flash(f'Results for {form.query.data}')  # show a message
        return redirect(url_for('results', query = form.query.data))  # redirect to another route
    return render_template('searchBar.html', title='search', form=form)  # template of the home page

#  results route of the app, runs when a query has been submitted on the form
@app.route("/results/<query>", methods= ["GET", "POST"])  # recieves the query as a parameter
def results(query):
    Q = queryprocessor.queryProcessor()  # process the query to get the top k results
    query_results = Q.process_query(str(query), pages, df_count, num_of_words_in_docs, indexer_copy)
    # query results contains a list of each document name and its score sorted
    websites = column(query_results, 0)
    new_links = []
    for sites in websites:
        new_links.append(sites.replace('.txt', '').replace('www.', '').replace('https','https://www.'))

    form = SearchForm()

    if form.is_submitted():  # if the form is submitted again, run this route again with the new query
        flash(f'Results for {form.query.data}')
        return redirect(url_for('results', query = form.query.data))
    return render_template('results.html', form=form, len = len(new_links), Results=new_links, query=query)
    # redirect to the template of the results page


def column(matrix, i): #return specific column of a matrix
    return [row[i] for row in matrix]
