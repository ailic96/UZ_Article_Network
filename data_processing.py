import os       # file manipulation
import csv      # csv file manipulation
import datetime # date structure  for interval filtering
import nltk     # processing natural language
from collections import Counter # counting dictionary elements
import operator #sorting dict

def delete_if_exists(path):
    """Deletes a file from input path if file exists.
    WARNING: Potentialy destructive action
    Args:
        path ([string]): Path variable or string
    """
    if os.path.exists(path):
        os.remove(path)

def isolate_date_intervals(lower_date, upper_date):
    """ Isolates articles in a wanted interval. Generates a .csv file.

    Args:
        lower_date (date() object):  Object of type (Year(2020), Month(1), Day(26))
        upper_date ([date() object): Object of type (Year(2020), Month(1), Day(26))
    """

    input_path  = 'data/portal_articles.csv'
    output_path = 'data/portal_article-'+ str(upper_date) +'.csv'

    delete_if_exists(output_path)

    with open(input_path, 'r', encoding = 'utf-8') as csv_read, \
         open(output_path, 'a', encoding = 'utf-8') as csv_write:

        csv_reader = csv.reader(csv_read, delimiter = ',')
        csv_writer = csv.writer(csv_write,
            delimiter=',', 
            quotechar='"', 
            quoting = csv.QUOTE_MINIMAL, 
            lineterminator='\n')

        #Add header for new columns
        headers = ['ID', 'Title', 'Subtitle', 'URL', 
        'Section','Article_text', 'Published_time', 'Modified_time',
        'Author', 'Comments', 'Reaction_love',
        'Reaction_laugh', 'Reaction_hug', 'Reaction_ponder',
        'Reaction_sad', 'Reaction_mad', 'Reaction_mind_blown', 'COVID']

        # Skip old header, add new a new one
        next(csv_reader, None)
        csv_writer.writerow(headers)

        # Article filtering by date
        for row in csv_reader:
            date_time_obj = datetime.datetime.strptime(row[6], '%Y-%m-%d')
            article_date = date_time_obj.date()

            if(lower_date <= article_date <= upper_date):
                csv_writer.writerow(row)

        print('Splited article file saved at: ' + output_path)



def file_to_list(input_file):
    """Creates a list from input file by reading .txt file by row.

    Args:
        input_file ([file]): .txt file with '\n' delimiter.

    Returns:
        [list]: A list of elements from .txt.
    """

    list = []
    file = open(input_file, 'r', encoding='utf-8')
    
    for row in file:
        row = row.rstrip()      # Remove \n at the end of row
        list.append(row)
    
    return list


def join_article_text(input_csv, output_txt):
    """ Joins all data containing the article title, 
    subtitle and full article text.

    Args:
        input_csv (csv)
        output_txt (txt)
    """
    input_path = 'data/' + str(input_csv)
    output_path= 'data/' + str(output_txt)

    delete_if_exists(output_path)

    print('Joining article: ' + output_path)
    with open(input_path, 'r', encoding = 'utf-8') as csv_read,\
        open(output_path, 'a', encoding = 'utf-8') as txt_write:
        
        csv_reader = csv.reader(csv_read, delimiter = ',')
        
        next(csv_reader, None)
        whole_text = []

        # Connect rows
        for row in csv_reader:
            article_text_joint = ' '.join([row[1], row[2], row[5]])
            whole_text.append(article_text_joint)
        
        whole_text_joint = ' '.join(whole_text)
        # To lowercase for further cleaning of stopwords
        txt_write.write(whole_text_joint.lower())




def clear_stop_words(input_txt, output_txt):
    """Used for clearing stop words from txt file which are
    predefined in stop_words_merged.txt
        Args:
            input_csv (txt) 
            output_txt (txt)
    """

    input_path = 'data/' + str(input_txt)
    output_path= 'data/' + str(output_txt)

    delete_if_exists(output_path)

    stop_words = set(file_to_list('stopwords/stop_words_merged.txt'))
    
    print('Cleaning file ' + str(input_path) + ' of stop words...')

    with open(input_path, 'r', encoding = 'utf-8') as txt_reader, \
        open(output_path, 'a', encoding = 'utf-8') as txt_writer:

        for row in txt_reader:
            word_tokens = nltk.word_tokenize(row)
            filtered_text = []

            for word in word_tokens:
                if word not in stop_words:
                    filtered_text.append(word)

            filtered_text = (' ').join(filtered_text)        
            txt_writer.write(filtered_text)

    print('Clean file saved at: ' + output_path)
    # Clears files from the previous step
    delete_if_exists(input_path)


def generate_brigram(input_txt, output_txt):
    """ Generates bigram from a list, clears stopletters.

    Args:
        input_txt (txt file)
        output_txt (txt file)
    """

    input_path = 'data/' + str(input_txt)
    output_path= 'data/' + str(output_txt)


    delete_if_exists(output_path)

    print('Generating bigram: ' + output_path)
    with open(input_path, 'r', encoding = 'utf-8') as txt_read, \
        open(output_path, 'a', encoding = 'utf-8') as txt_write: 

        whole_text = txt_read.read().replace('\n','')
        nltk_tokens = nltk.word_tokenize(whole_text)
        bigram_list = list(nltk.bigrams(nltk_tokens))

        # Short list of stop letters.
        stopletters = ['“', ',', ':', '”', '.', ',', '–', '.', ',', '” ', "''", '``', "''", '..', '...', ',', '.', '’', '„', '" ', '"', '”', '‘', '•', ':', '\\n', '\\t', '“', '–', ';', '-', '_', '!', '~', '"', 'ˇ', '#', '^', '$', '˘', '%', '°', '&', '˛', '/', '`', '(', '˙', ')', '´', '=', '˝', '?', '¨', '¸', '+', '*', '@', '{', '}', '<', '>', '[', ']', 'ł', 'Ł', 'ß', '¤', '\\', '|', '€', '÷', '×']

        for item in bigram_list:
            if item[0] not in stopletters:
                if item[1] not in stopletters:
                    txt_write.write(item[0] + ' ' +  item[1] + '\n')
    
    # Clears files from the previous step
    delete_if_exists(input_path)

                
                

def count_bigrams(input_txt, output_txt):
    """ Turns a list of elements to dictionary, counts sorts
     identical bigrams. Saves the file as .txt

    Args:
        input_txt (txt file)
        output_txt (txt file)
    """
    input_path = 'data/' + str(input_txt)
    output_path= 'data/' + str(output_txt)

    delete_if_exists(output_path)

    print('Counting bigram: ', output_path)
    with open(input_path, 'r', encoding = 'utf-8') as txt_read, \
        open(output_path, 'a', encoding = 'utf-8') as txt_write:

        bigram_list = []
        for row in txt_read:
            bigram_list.append(row)

        bigram_counter = Counter(bigram_list)
        
        bigram_counter = dict( sorted(bigram_counter.items(), key=operator.itemgetter(1),reverse=True))
    
        for k, v in bigram_counter.items():
            txt_write.write(str(k.rstrip('\n')) + ' ' + str(v) + '\n')

    # Clears files from the previous step
    delete_if_exists(input_path)            



# Function calls

isolate_date_intervals(datetime.date(2020, 1, 1), datetime.date(2020,  2, 24))
isolate_date_intervals(datetime.date(2020, 2, 25), datetime.date(2020, 3,13))
isolate_date_intervals(datetime.date(2020, 3, 14), datetime.date(2020, 5,11))
isolate_date_intervals(datetime.date(2020, 5, 12), datetime.date(2020, 8,25))

join_article_text('portal_articles.csv', 'portal_article_all_merged.txt')
join_article_text('portal_article-2020-02-24.csv', 'portal_article-2020-02-24_merged.txt')
join_article_text('portal_article-2020-03-13.csv', 'portal_article-2020-03-13_merged.txt')
join_article_text('portal_article-2020-05-11.csv', 'portal_article-2020-05-11_merged.txt')
join_article_text('portal_article-2020-08-25.csv', 'portal_article-2020-08-25_merged.txt')

clear_stop_words('portal_article_all_merged.txt', 'portal_article_all_clean.txt')
clear_stop_words('portal_article-2020-02-24_merged.txt', 'portal_article-2020-02-24_clean.txt')
clear_stop_words('portal_article-2020-03-13_merged.txt', 'portal_article-2020-03-13_clean.txt')
clear_stop_words('portal_article-2020-05-11_merged.txt', 'portal_article-2020-05-11_clean.txt')
clear_stop_words('portal_article-2020-08-25_merged.txt', 'portal_article-2020-08-25_clean.txt')


generate_brigram('portal_article_all_clean.txt', 'portal_article_all_bigrams.txt')
generate_brigram('portal_article-2020-02-24_clean.txt','portal_article-2020-02-24_bigrams.txt')
generate_brigram('portal_article-2020-03-13_clean.txt','portal_article-2020-03-13_bigrams.txt')
generate_brigram('portal_article-2020-05-11_clean.txt','portal_article-2020-05-11_bigrams.txt')
generate_brigram('portal_article-2020-08-25_clean.txt','portal_article-2020-08-25_bigrams.txt')

count_bigrams('portal_article_all_bigrams.txt', 'portal_article_all_bigrams_counted.txt')
count_bigrams('portal_article-2020-02-24_bigrams.txt', 'portal_article-2020-02-24_bigrams_counted.txt')
count_bigrams('portal_article-2020-03-13_bigrams.txt', 'portal_article-2020-03-13_bigrams_counted.txt')
count_bigrams('portal_article-2020-05-11_bigrams.txt', 'portal_article-2020-05-11_bigrams_counted.txt')
count_bigrams('portal_article-2020-08-25_bigrams.txt', 'portal_article-2020-08-25_bigrams_counted.txt')
