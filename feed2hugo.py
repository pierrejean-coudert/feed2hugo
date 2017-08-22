import feedparser
import os, sys
from argparse import ArgumentParser

def main():
    #
    ## Command line parser
    #

    parser = ArgumentParser(description='Submit dataTasks or dataFlows to Queue')
    parser.add_argument('-f', '--feed',
                        required=True,
                        dest='feed',
                        help='Feed url or path to feed file')
    parser.add_argument('-t', '--target',
                        required=True,
                        dest='target',
                        help='Root path for Hugo project')
    parser.add_argument('-c', '--contenttype',
                        dest='contenttype',
                        default='post',
                        help='project file')
    args = parser.parse_args()

    try:
        HUGO_ROOT_PATH = args.target    
    except ValueError:
        sys.exit("Hugo root path not defined with -t or --target")

    try:
        FEED_URL = args.feed
    except ValueError:
        sys.exit("Feed URL or path to feed not defined with -f or --feed")

    try:
        DEFAULT_CONTENT_TYPE = args.contenttype
    except ValueError:
        sys.exit("Hugo root path not defined with -c or --contenttype")

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

    #
    ## RSS Case - to implement ?
    #

if __name__ == '__main__':
    main()
