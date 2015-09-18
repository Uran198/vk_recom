#/usr/bin/env python

from urllib import parse
from consts import oauth_link
import json

print("Follow oauth_link:")
print(oauth_link)
link = input("Insert here response url after oauth redirection: ")

query = parse.urlparse(link).fragment
x = parse.parse_qs(query)
data = { x['user_id'][0] : { 'access_token' : x['access_token'][0] } }

fd = open("config.json", 'w')
json.dump(data, fd)
fd.close()
print("Successfully rewritten config.json")
