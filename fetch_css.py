import scrapy
import pdfkit
import requests
import urllib2
from urlparse import urlparse
from bs4 import BeautifulSoup

def fetch_css(url):

    try:
        response = urllib2.urlopen(url)
        html_data = response.read()
        response.close()

        soup = BeautifulSoup(''.join(html_data), "lxml")

        # Find all external style sheet references
        ext_styles = soup.findAll('link', rel="stylesheet")

        # Find all internal styles
        int_styles = soup.findAll('style', type="text/css")

        # TODO: Find styles defined inline?
        # Might not be useful... which <p style> is which?
 
        # Loop through all the found int styles, extract style text, store in text
        # first, check to see if there are any results within int_styles.
        int_css_data = ''
        int_found = 1
        if len(int_styles) != 0:
            for i in int_styles:
                if(str(i.find(text=True))!='None'):
                    print "Found Internal"
                    int_css_data += str(i.find(text=True))
        else:
            int_found = 0
            print("No internal stylesheets found")
 
        # Loop through all the found ext stylesheet, extract the relative URL,
        # append the base URL, and fetch all content in that URL
        # first, check to see if there are any results within ext_styles.
        ext_css_data = ''
        ext_found = 1
        if len(ext_styles) != 0:
            for i in ext_styles:
                # Check to see if the href to css style is absolute or relative
                o = urlparse(i['href'])
                if o.scheme == "":
                    css_url = url + '/' + i['href']  # added "/" just in case
                    print "Found external stylesheet: " + css_url
                else:
                    css_url = i['href']
                    print "Found external stylesheet: " + css_url
 
                response = urllib2.urlopen(css_url)
                ext_css_data += response.read()
                response.close()
        else:
            ext_found = 0
            print "No external stylesheets found"
 
        # Combine all internal and external styles into one stylesheet (must convert
        # string to unicode and ignore errors!
        # FIXME: Having problems picking up JP characters:
        # I already tried ext_css_data.encode('utf-8'), but this didn't work
        all_css_data = int_css_data + unicode(ext_css_data, errors='ignore')
 
        return all_css_data, int_found, ext_found
    except:
        return "",0,0

out, int_found, ext_found = fetch_css('http://www.geeksforgeeks.org/sort-linked-list-already-sorted-absolute-values/')
if ext_found == 1 or int_found == 1:
    filename = './compiled_css.css'
    f = open( filename, 'w')
    f.write(out)
    css_include_statement = '<link rel="stylesheet" type="text/css" href="compiled_css.css">'
    filename = "./geeks.html"
    with open(filename, 'w') as f:
        f.write(css_include_statement)
else:
    print "not found anything"