import feedparser
import os
from settings import FEED_URL, HUGO_ROOT_PATH, DEFAULT_CONTENT_TYPE

#
## CHECK DESTINATION PATH EXISTENCE
#

dest_path = "%s/content/%s" % (HUGO_ROOT_PATH, DEFAULT_CONTENT_TYPE)

if os.path.exists(dest_path) is False:
    print("The folder %s does not exist" % dest_path)
    os.makedirs(dest_path)
    print("The folder %s has been created ..." % dest_path)
else:
    pass

#
## PARSE FEED
#

f = feedparser.parse(FEED_URL)

#
## Check if ATOM or RSS ?
#

#
## Atom Case
#

for entry in f.entries:
    title = entry.title
    link = entry.link
    date = entry.published
    if "updated" in entry:
        lastmod = entry.updated
    author = entry.author
    if 'tags' in entry:
        tags = []
        for tag in entry.tags:
            tags.append(tag['term'])
    content = entry.content[0].value
    contenttype = DEFAULT_CONTENT_TYPE
    filetitle = "%s.html" % link.split('/')[-1:][0]
    print(filetitle)
    print('---')
    print('date: %s' % date)
    print('title: %s' % title)
    print('url: %s' % link)
    print('tags: [%s]' % '", "'.join(tags))
    print('lastmod: %s' % lastmod)
    print('type: %s' % contenttype)
    print('---')
    print(content)