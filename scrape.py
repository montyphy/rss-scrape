#!/usr/bin/env python

from urllib2 import urlopen
import re


#   Regular expressions shouldn't really be used to parse HTML/XML/XHTML:
#   http://stackoverflow.com/questions/1732348/1732454#1732454
#   but they should be ok for this
pat_item = re.compile('<item>(.*?)</item>', re.DOTALL)
pat_link = re.compile('<link>(.*?)</link>', re.DOTALL)
pat_title = re.compile('<title>(.*?)</title>')

#   Will create tuples of the form (<tag name>, <tag attributes>, <tag content>)
pat_item_content = re.compile('<(?P<tagname>\w*)(.*?)>(.*?)</(?P=tagname)>', re.DOTALL)


def get_raw_content(url, timeout=5):
    '''
    Attempts to fetch content pointed to by url.
    '''
    try:
        data = urlopen(url, timeout=timeout).read()
    except:
        print "Cannot open url: " + url
        return None
    return data

def get_links(url, pat_item=pat_item, pat_link=pat_link, pat_title=pat_title):
    '''
    Fetches raw feed from url and returns a dictionary. Dictionary will
    have each item link as a key with that item's title as the value.
    '''
    raw = get_raw_content(url)
    rss_items = re.findall(pat_item, raw)

    output = {}
    for item in rss_items:
        link = re.findall(pat_link, item)[0]
        link = link.split('#')[0]       # get rid of tracker info in the link

        title = re.findall(pat_title, item)[0]

        output[link] = title
    return output

def get_feed(url, pat_item=pat_item, pat_item_content=pat_item_content):
    '''
    Fetches raw feed from url and returns an array of dicts. One entry per
    pat_item match. pat_item_content used to extract item data, ditches
    tag attribute data.
    '''
    raw = get_raw_content(url)
    rss_items = re.findall(pat_item, raw)

    output = []
    for rss_item in rss_items:
        rss_item =  re.findall(pat_item_content, rss_item)

        item_dict = dict()
        for item in rss_item:
            key = item[0]       # tag name
            value = item[2]     # tag content

            item_dict[key] = value

        output.append(item_dict)
    return output


def main():
    '''
    Example usage
    '''

    url = "http://feeds.bbci.co.uk/news/rss.xml"

    links = get_links(url)
    print "RSS Links:"
    print links
    print

    feed = get_feed(url)
    print "Feed:"
    print feed


if __name__ == "__main__":
    main()
