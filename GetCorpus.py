import urllib2
import nltk
import string


def get_page_info(page):
    #See if the page exists. Get html if it does.
    try:
        page_html = urllib2.urlopen(page).read()
    except:
        return [], []

    #Get the page text and the links
    links = get_links(page_html)
    words = get_words(page_html)

    return links, words


def get_words(page_html):
    words = []
    raw_text = nltk.clean_html(page_html)
    for line in raw_text.splitlines():
        for word in line.split():
            word = word.lower()
            word = word.strip(string.punctuation)
            word = word.strip(string.whitespace)
            words.append(word)
    return words


def get_links(page_html):
    links = []
    
    #Loop through page, looking for link tags
    #TODO: use regular expressions instead
    while True:
        start_tag = page_html.find('<a href=')
        start_url = page_html.find('"', start_tag)+1
        end_url = page_html.find('"', start_url)
        url = page_html[start_url:end_url]
        
        #Only take the url if it has http
        if url:
            if url[:4] == 'http':
                links.append(url)
        else:
            break

        #Remove processed html
        page_html = page_html[end_url:]
        
    return links

def crawler(start_page, url_rank, corpus, print_detail=False):
    to_crawl = [start_page]
    counter = 1
    while True:
        if counter%100 == 0:
            answer = raw_input('100 pages added. Continue? (y/n):\n')
            if answer == 'n':
                break
    
        #Only go to page if it hasn't been crawled.
        #Remove links that were already crawled
        for new_link in to_crawl:
            if not url_rank.get(new_link):
                page = new_link
                to_crawl = to_crawl[to_crawl.index(page)+1:]
                break
        else:
            break

        #Get page information
        links, words = get_page_info(page)
        
        #Process the links. Prevent repeats.
        for link in links:
            if url_rank.get(link):
                url_rank[link] += 1
            elif link not in to_crawl:
                to_crawl.append(link)

        #Process the words. Prevent repeats.
        for word in words:
            if not corpus.get(word):
                corpus[word] = [page]
            elif page not in corpus[word]:
                corpus[word].append(page)

        #Indicate that the page has been crawled
        url_rank[page] = 1

        #Check progress...
        if print_detail:
            print 'page: %s' % counter
            print 'len corpus: %s' % len(corpus)
            print 'len to_crawl: %s' % len(to_crawl)
            print ''

        #Increase counter
        counter += 1

    return url_rank, corpus

def update_corpus(seed, url_rank, corpus):
    
    #Generate corpus
    url_rank, corpus = crawler(seed, url_rank, corpus, print_detail=True)
    print 'Corpus generated'

    print 'Sorting corpus...'
    #Rank urls from url_rank
    ranked = [(score, url) for url, score in url_rank.items()]
    ranked.sort(reverse=True)
    ranked = [item[1] for item in ranked]

    print 'Sorting urls for keys...'    
    #Sort urls for each key
    for key in corpus.keys():
        corpus[key] = [url for url in ranked if url in corpus[key]]

    print 'Finished sorting!'
    return url_rank, corpus


def open_corpus():
    url_rank = dict()
    corpus = dict()
    
    #Open files
    with open('Corpus/Corpus.txt','r') as raw_corp, \
         open('Corpus/PageRank.txt','r') as raw_rank:

        #First value is keyword, all others are urls
        for line in raw_corp.read().splitlines():
            if line:
                line_split = line.split(',')
                corpus[line_split[0]] = line_split[1:]

        #First value is url, second is count
        for line in raw_rank.read().splitlines():
            if line:
                line_split = line.split(',')
                url_rank[line_split[0]] = int(line_split[1])
    return url_rank, corpus


def write_file(url_rank, corpus):
    #Open files for writing
    with open('Corpus/Corpus.txt','w') as corpus_file, \
         open('Corpus/PageRank.txt','w') as rank_file:

        #Write to corpus
        for key_results in corpus.items():
            url_csv = ','.join(key_results[1])
            line_csv = '%s,%s\n' % (key_results[0],url_csv)
            corpus_file.write(line_csv)

        #Write to PageRank
        for url_score in url_rank.items():
            rank_file.write('%s,%s\n' % (url_score[0],url_score[1]))


def run(seed):
    print 'Opening url rank and corpus...'
    url_rank, corpus = open_corpus()
    
    #Check if seed is legit, and hasn't been used
    while True:
        try:
            check = urllib2.urlopen(seed)
        except:
            print 'You entered an invalid seeding website'
            seed = raw_input('Enter another website:\n')
        else:
            if url_rank.get(seed):
                seed = raw_input('Seed already in corpus, enter a new one:\n')
            else:
                break

    print 'Updating corpus...'
    url_rank, corpus = update_corpus(seed, url_rank, corpus)

    print 'Writing to file...'
    write_file(url_rank, corpus)

    print 'Done!'
    
    

if __name__ == '__main__':
    run('http://www.xkcd.com')
    
