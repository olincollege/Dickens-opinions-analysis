import requests
r = requests.get('https://gutenberg.org/files/786/786-0.txt')
r.text
print(r.text)