import csv
import time
from html.parser import HTMLParser

class Node():
    def __init__(self):
        self.char = None
        self.children = {}
        self.leaf = False
        self.data = {}

class Trie():
    def __init__(self):
        self.root = Node()

    def add(self, word, data):
        current = self.root
        children = self.root.children
        for char in word:
            char = char.lower()
            if char not in children:
                node = Node()
                node.char = char
                children[char] = node
                current = node
                children = node.children
        current.leaf = True
        current.data = data

    def print_word(self, word, node=None):
        node = self.root
        children = node.children
        for char in word:
            if char not in children:
                print('Word: %s is not in the Trie.'%word)
                break
            else:
                node = children[char]
                children = node.children
        else:
            print('Word: %s, Data: %s'%(word, node.data))

class HTMLTextParser(HTMLParser):
    def __init__(self, xhtml):
        HTMLParser.__init__(self)
        self.xhtml = xhtml
        self.trie = Trie()
        self.populate_trie()

    def populate_trie(self):
        file_handle = open('source.csv', 'r')
        reader = csv.DictReader(file_handle)
        for row in reader:
            word = row.get('word')
            if not word:
                continue
            link = row.get('link')
            self.trie.add(word, data={'url': link})

    def get_longest_matching_word_length(self, start_index, data):
        #print('start_index: %s, data:%s'%(start_index, data))
        current = self.trie.root
        children = current.children
        i, longest_match = start_index, None
        while i<len(data):
            if data[i].lower() in children:
                current = current.children[data[i].lower()]
                children = current.children
                i+=1
                if (i == len(data) or (i < len(data) and self.is_word_separator(data[i])) and current.leaf == True):
                    longest_match = i -1
            else:
                break
        return longest_match, current

    @staticmethod
    def is_word_separator(char):
        if char in [' ', '\n', '.', ',', '\t', ':', ';', '?']:
            return True
        return False

    @staticmethod
    def is_valid_char(char):
        return char.isalnum()

    def add_links(self, text):
        i = 0
        #print('text: %s'%text)
        replace_indices = []
        while i < len(text):
            while i< len(text) and self.is_word_separator(text[i]):
                i+=1
            if i<len(text) and self.is_valid_char(text[i]):
                start_index = i
                longest_match, node = self.get_longest_matching_word_length(start_index = start_index, data=text)
                if longest_match:
                    replace_indices.append((start_index, longest_match, node))
                    #print('Longest Match: %s'%longest_match)
                    #print('Found Word: %s with data: %s')
                    i = longest_match+1
                else:
                    while i < len(text) and self.is_valid_char(text[i]):
                        i += 1
            i+=1

        for start_index, longest_match, node in replace_indices:
            url = node.data['url']
            word = text[start_index: longest_match+1]
            #print('Got word: %s'%word)
            text = text[:start_index] + "<a href=%s target='_blank'>"%url + word + "</a>" + text[longest_match+1:]
        return text

    def handle_decl(self, decl):
        self.xhtml += "<!" + decl + ">"

    def unknown_decl(self, data):
        self.xhtml += "<!" + data + ">"

    def handle_starttag(self, tag, attrs):
        self.xhtml += self.get_starttag_text()

    def handle_endtag(self, tag):
        self.xhtml += "</" + tag + ">"

    def handle_startendtag(self, tag, attrs):
        self.xhtml += self.get_starttag_text()

    def handle_data(self, data):
        #print('Got Data: %s'%data)
        self.xhtml+=self.add_links(text=data)

    def handle_comment(self, data):
        self.xhtml += "<!--" + data + "-->"

    def handle_charref(self, name):
        self.xhtml += "&#" + name + ";"

    def handle_entityref(self, name):
        self.xhtml += "&" + name + ";"

    def handle_pi(self, data):
        self.xhtml += "<?" + data + ">"

html_text = """
<!DOCTYPE html>
<html>

<head>
  <title>Our Company</title>
</head>

<body>

  <h1>Welcome to Our Company</h1>
  <h2>Web Site Main Ingredients:</h2>

  <p>Pages (HTML)</p>
  <p>Style Sheets (CSS)</p>
  <p>Computer Code (JavaScript)</p>
  <p>Live Data (Files and Databases)</p>
  <p>Our company is Google which is a search engine giant.</p>
  <p>peta stands for People for the Ethical Treatment to Animals.</p>
  <p>A crypto currency, crypto-currency, or crypto is a digital asset designed to work as a medium of exchange wherein individual coin ownership records are stored in a ledger existing in a form of a computerized database using strong cryptography to secure transaction records, to control the creation of additional coins, and to verify the transfer of coin ownership.</p>
</body>
</html>
"""

html_text_parser = HTMLTextParser(xhtml='')
#print(html_text_parser.xhtml)
start_time = time.time()
html_text_parser.feed(html_text)
end_time = time.time()
print(html_text_parser.xhtml)
print('Time required for forming links: %s seconds.'%(end_time - start_time))