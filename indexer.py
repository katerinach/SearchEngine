import os
import csv
import numpy
import copy

#the Indexer function
def Indexer():

    list = [] #list that contains the words crawled
    num_of_words_in_doc = [] #tracks the total number of words in each document

    #getting each word from each file and creating a csv file to save the data


    for file in os.listdir(".\\files\\"):  # for each txt file created by crawler
        words_count = 0
        if not file.endswith(".txt"):
            continue
            #reading each line
        with open(".\\files\\" + file, 'r',  encoding='utf-8') as f:
            for line in f:
                #reading each word
                for word in line.split():
                    punc = '''!()|-[]{};:'", <>./?@#$%^&*_~©®™¨¨«»'''
                    if word in punc: #ignore punctuation marks
                        continue
                    words_count = words_count+1
                    flag = 0
                    for index, array in enumerate(list):
                        if word in array[0] and str(file) == str(array[1]): #for same words in the same document
                            list[index][2] = int(list[index][2]) + 1
                            flag = 1
                    if flag == 0:
                        word = word.lower() #make all words lowercase to avoid same words appearing in the indexer multiple times
                        list.append(numpy.array([str(word), str(file), 1])) #add the word,document name to the list
                    else:
                        continue
        num_of_words_in_doc.append([file, words_count]) #add the file and word count
    #sorting the csv in alphabetic order by the 'word' value
    list.sort(key=get_word)

    #calculating the number of documents that each word appears in (so that the same word doesn't repeat)
    count = []
    frequency = 0
    previous_word = list[0][0] #set the first word as the previous word
    for array in list: #for each word in the list
        current_word = array[0] #set each word as current
        if current_word == previous_word: #if it's the same as the previous one
            frequency = frequency + 1 #add frequency count
        else:
            count.append([previous_word, frequency]) #else means the repeated word has ended and we can add it and frequency count to the list
            frequency = 1 #resetting frequency count

        previous_word = current_word #set current as previous

    #creating a csv file to save the data
    indexer_copy = []
    with open('.\\indexer\\indexer.csv', 'w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['word', 'documents', 'data']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        temp = []
        for data in count:
            temp.clear()
            for array in list:
                if array[0] == data[0]:
                    temp.append([str(array[1]), int(array[2])])
            temp2 = copy.deepcopy(temp)
            indexer_copy.append([data[0], data[1], temp2]) #make a list copy of the indexer to use later
            writer.writerow({'word': data[0], 'documents': data[1], 'data': temp})

    return count, num_of_words_in_doc, indexer_copy #return count of each word, number of words in each doc and indexer


def get_word(array):
    return array[0]
