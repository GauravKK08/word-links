# word-links
Uses a Prefix trie based implementation to reach to the longest possible word in the trie from a parsed HTML text

It requires `source.csv` to populate a trie with words & their respective links.

The HTML text data is traversed tag-by-tag using Python's inbuilt HTMLParser (which works great)

The objective is to find the longest possible word and highlight it.

So consider for a sample HTML input text like below:

```
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
```

We can generate output like below via the program.

```
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
  <p>Our company is <a href=https://www.google.com target='_blank'>Google</a> which is a search engine giant.</p>
  <p><a href=https://www.peta.org target='_blank'>peta</a> stands for People for the Ethical Treatment to Animals.</p>
  <p>A <a href=https://en.wikipedia.org/wiki/Cryptocurrency target='_blank'>crypto currency</a>, crypto-currency, or crypto is a digital asset designed to work as a medium of exchange wherein individual coin ownership records are stored in a ledger existing in a form of a computerized database using strong cryptography to secure transaction records, to control the creation of additional coins, and to verify the transfer of coin ownership.</p>
</body>
</html>
```

