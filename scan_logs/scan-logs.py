# Simple scanner for logs and config files based on default installations
# work in progress

import urllib2
import threading
import Queue
import urllib

print("Simple tool to scan known log and configuration file paths")
print("<----------------------------------------------------->")

target_url = input("Enter the IP address that you want to scan: ")
print("The IP you entered is: ", target_url)
type(target_url)

answer = input("""\nStart scan of default log and configuration file paths (y/n) \n""")
print("You have selected option: ", answer)

threads        = 50
#target_url     = "http://testphp.vulnweb.com"
wordlist_file  = "/tmp/all.txt" # from SVNDigger
resume         = None
#Windows 10-based PC using Edge browser
user_agent     = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"

def build_wordlist(wordlist_file):
# Read in the word list
fd = open(wordlist_file, "rb")
raw_words = fd.readlines()
fd.close()

found_resume = False
words = Queue.Queue()

    for word in raw_words:

    word = word.rstrip()

    if resume is not None:

        if found_resume:
            words.put(word)
        else:
            if word == resume:
                found_resume = True
                print
                "Resuming wordlist from: %s" % resume
    else:
        words.put(word)

return words

def dir_bruter(word_queue,extensions=None):

      while not word_queue.empty():
          attempt = word_queue.get()

          attempt_list = []

          # check to see if there is a file extension; if not,
          # it's a directory path we're bruting
         if "." not in attempt:
              attempt_list.append("/%s/" % attempt)
          else:
              attempt_list.append("/%s" % attempt)

          # if we want to bruteforce extensions
         if extensions:
              for extension in extensions:
                  attempt_list.append("/%s%s" % (attempt,extension))

          # iterate over our list of attempts
          for brute in attempt_list:

              url = "%s%s" % (target_url,urllib.quote(brute))

              try:
                  headers = {}
                 headers["User-Agent"] = user_agent
                  r = urllib2.Request(url,headers=headers)

                  response = urllib2.urlopen(r)

                 if len(response.read()):
                      print "[%d] => %s" % (response.code,url)

              except urllib2.URLError,e:

                  if hasattr(e, 'code') and e.code != 404:
                     print "!!! %d => %s" % (e.code,url)
                     pass

word_queue = build_wordlist(wordlist_file)
extensions = [".php",".bak",".orig",".inc"]

for i in range(threads):
    t = threading.Thread(target=dir_bruter,args=(word_queue,extensions,))
    t.start()
