import string

corpus = dict()
with open('Corpus/Corpus.txt','r') as raw_corp:
    #First value is keyword, all others are urls
    print 'Loading corpus...'
    for line in raw_corp.read().splitlines():
        if line:
            line_split = line.split(',')
            corpus[line_split[0]] = line_split[1:]
    print 'Corpus loaded.'
    print ''
    
def run():
    query = raw_input('Please enter your search term:\n')
    query = query.lower()
    query = query.strip(string.punctuation)
    query = query.strip(string.whitespace)
    results = corpus.get(query)
    if results:
        print 'Your results for "%s":' % query
        print '\n'.join(results)          
    
    

if __name__ == '__main__':
    search = 'y'
    print 'Welcome to the search engine!'
    while search == 'y':        
        run()
        search = raw_input('Search again?\n')
        
