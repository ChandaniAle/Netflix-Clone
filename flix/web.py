import requests
from bs4 import BeautifulSoup

url = 'https://www.daraz.com.np/bath-body/?spm=a2a0e.11779170.cate_2.1.287d2d2b4U0Ojg'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

# Get the content
response = requests.get(url, headers=headers)
html_content = response.text

# Parsing the html content
soup = BeautifulSoup(html_content, 'html.parser')
print(soup)

# Print out a portion of the parsed HTML to identify the correct class
# print(soup.prettify()[:2000])  # Printing the first 2000 characters of the HTML

# Assuming you identified the correct class, we will find the titles again
titles = soup.find_all('div',id="id-title")
print(titles)

# Extract and print the text of each title
for title in titles:
    print(title.get_text(strip=True))
