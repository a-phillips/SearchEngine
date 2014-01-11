import urllib2


def get_links(page):
    try:
        page_source = urllib2.urlopen(page).read()
    except:
        return []
    links = []
    while True:
        start_tag = page_source.find('<a href=')
        start_url = page_source.find('"', start_tag)+1
        end_url = page_source.find('"', start_url)
        url = page_source[start_url:end_url]
        if url:
            if url[:4] == 'http':
                links.append(url)
        else:
            break
        page_source = page_source[end_url:]
    return links

def crawler(start_page):
    crawled = dict()
    to_crawl = [start_page]
    i = 1
    while i < 40:
        for new_link in to_crawl:
            if not crawled.get(new_link):
                page = new_link
                break
        else:
            break
        page_links = get_links(page)
        print 'crawler len %s, page no. %s: %s' % (len(crawled), i, page)
        for link in page_links:
            if crawled.get(link):
                crawled[link] += 1
            elif link not in to_crawl:
                to_crawl.append(link)
        crawled[page] = 1
        try:
            page = to_crawl.pop(0)
        except:
            break
        i += 1
    print 'The crawler has finished!'
    print 'Results:'
    for key, value in crawled.items():
        print key, value

if __name__ == '__main__':
    #crawler('http://www.udacity.com/cs101x/index.html')
    crawler('http://www.xkcd.com')
