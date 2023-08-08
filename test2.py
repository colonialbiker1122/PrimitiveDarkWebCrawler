import pandas as pd  
import socks
import socket
import requests
from bs4 import BeautifulSoup
from urllib.error import ContentTooShortError, HTTPError, URLError
import urllib.request

#Direct Trafiic through Tor Browser
socks.set_default_proxy(socks.SOCKS5, "localhost", 9150)
socket.socket = socks.socksocket

def getaddrinfo(*args):
    return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]

socket.getaddrinfo = getaddrinfo
print("SUCCESS: Connection Established via Tor Browser !!")

def majorfunction(linklist):
    #Request the Feeder Links to begin Searching via various Search Engines
    print("Begining to Collect Links...")
    onion = []
    for l in linklist:
        res = requests.get(l)
        soup = BeautifulSoup(res.content, 'html.parser')
        links = [link.get('href') for link in soup.find_all('a')]
        links = list(filter(None, links)) 
        for lshow in links:
            if "onion" in lshow:
                onion.append(lshow)
    print("SUCCESS: {0} Links are Collected".format(len(onion)))

    #Trim the links to proper link format
    for s1 in onion:
        onion = [item.replace(s1, s1[s1.find("http"):]) for item in onion]
    print("SUCCESS: {0} Links are Trimmed".format(len(onion)))

    # Remove Duplicates
    onion = list(set(onion))
    print("SUCCESS: Duplicates are Removed. {0} links are Collected".format(len(onion)))

    #Check if all the links are valid or not
    invalid_count = 0
    linkcount = 0
    validlinks = []
    for x in onion:
        try:
            urllib.request.urlopen(x)
            linkcount +=1
            validlinks.append(x)
        except (HTTPError, URLError, ContentTooShortError) as err:
            invalid_count +=1
            linkcount += 1
            print("{0} is Invalid. No of Links Scanned: {1}".format(x, linkcount))
        else:
            print("{0} is Valid. No of Links Scanned: {1}".format(x, linkcount))

    print("Invalid Links: {0}".format(invalid_count))

    # Update Resulst in .CSV File
    df1 = pd.read_csv("database.csv")
    a = list(df1['0'])
    union = list(set(a + validlinks))
    df3 = pd.DataFrame(union)
    df3.to_csv("database.csv", index=False) # need to change from new_database to database.csv

    #View Status
    print("Total Unique and Valid Number of Dark Web links Collected are: {0}".format(len(df3)))

#Feeder Links for Begining of Search
druglist = ['alcohol','weed','viagra','rollies','molly','lucy','hookah','ganja','cowies','kix','mandy','nopaine','quat','skunk']

linklist = []

for d in druglist:
    linklist.append("http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/search/?q=" + str(d))

klist = ['http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/search/?q=weed', 'http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/search/?q=lsd']
majorfunction(linklist)