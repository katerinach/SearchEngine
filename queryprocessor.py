import os
import csv
import numpy
import math
from numpy import dot
from numpy.linalg import norm

#the query processor class
class queryProcessor:

    def __init__(self):
        pass

    #the function that calculates the idf values
    def calculate_idf(self,count, N):
        idf_values = [] #key is each word and the value is the idf value
        for token in count:
            idf_values.append([token[0], math.log(N/token[1])]) #IDF Formula

        return idf_values

    #the function that calculates the query idf value. Does the same as calucalte_idf but adds the query
    def calculate_query_idf(self,query_count,count,N):
        idf_values = [] #key is each word and the value is the idf value
        for query in query_count:
            for token in count:
                if token[0] == query[0]:
                    idf_values.append([token[0], math.log(N/token[1]+query[1])])

        return idf_values

    #the function that calculates the number of a word in a specific document
    def calculate_count_of_word_in_doc(self,word,doc,indexer_copy):
        for row in indexer_copy:
        #reading each row of the indexer
            if row[0] == word: #if it finds the word then must check for the specific doc
                for d in row[2]:
                    if d[0] == doc:
                        return d[1] #d[1] is the count of appearance
        return 0

    #function that processes the query
    def process_query(self,query,N,count,num_of_words_in_docs,indexer_copy):

        #calculate TF-IDF
        idf = self.calculate_idf(count, N)
        tfidf_documents = []
        for doc in num_of_words_in_docs: #for each document
            doc_tfidf = []
            for word in idf: #for each word
                tf = self.calculate_count_of_word_in_doc(word[0],doc[0],indexer_copy)/doc[1] #TF Formula
                doc_tfidf.append([word[0],doc[0], tf * word[1]]) #TF-IDF Formula
            tfidf_documents.append(doc_tfidf)

        #turn the query into list of words and number of appearance
        query = query.lower() #make lowercase
        query_list = list(query.split(" "))
        query_list.sort(key=get_word) #sort
        query_count = []
        frequency = 0
        previous_word = query_list[0]
        for word in query_list: #for all words in query, find frequency of appearance inside the query
            current_word = word
            if current_word == previous_word:
                frequency = frequency + 1
                previous_word = current_word
            else:
                query_count.append([previous_word, frequency])
                frequency = 1
                previous_word = current_word
        query_count.append([previous_word, frequency])

        #calculate tf-idf for the query
        query_idf = self.calculate_query_idf(query_count,count,N)
        query_tfidf = []
        i = 0
        for word in query_idf:
            query_tf = query_count[i][1]/len(query_list) #TF Formula
            query_tfidf.append([word[0],"query", query_tf * word[1]]) #TF-IDF Formula
            i = i+1

        cosine_sim = self.cosine_similarity(query_tfidf,tfidf_documents,N,num_of_words_in_docs) #find cosine similarity
        cosine_sim.sort(key=lambda x: x[1]) #sort the results by the cosine similarity score
        print("final results: ",cosine_sim)
        return cosine_sim

    #function that calculates the cosine similarity
    def cosine_similarity(self, query_vector,doc_vectors,N,num_of_words_in_docs):

        v1 = 0 #query vector
        result=[]
        for i in range(len(query_vector)):
            v1= v1 + query_vector[i][2] #sum of individual vectors
        cosine = 0
        for i in range(0,N): #find scoring for each document
            v2 = 0
            for word in doc_vectors[i]:
                v2 = v2 + word[2] #sum of individual vectors
            cosine = dot(v1, v2) / (norm(v1)*norm(v2))
            result.append([num_of_words_in_docs[i][0], cosine]) #Cosine similarity Formula
            #print("dot: ",dot(v1, v2),", norm v1: ",norm(v1),", norm v2: ",norm(v2))

        return result


def column(matrix, i): #return specific column of a matrix
    return [row[i] for row in matrix]



def get_word(array):
    return array[0]