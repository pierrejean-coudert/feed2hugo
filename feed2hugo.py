import feedparser
import os, sys
from argparse import ArgumentParser
from slugify import slugify
from markdownify import markdownify as md

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
        if 'content' in entry:
            content = entry.content[0].value
        contenttype = DEFAULT_CONTENT_TYPE
        filetitle = "%s.md" % (slugify(entry.title))
        full_dest_path = "%s/%s" % (dest_path, filetitle)

        output = open(full_dest_path, 'w')
        output.write('---\n')
        output.write('date: %s\n' % date)
        output.write('title: "%s"\n' % title.replace('"','\''))
        output.write('author: %s\n' % author)
        output.write('previous_url: %s\n' % link)
        if 'tags' in entry:
            output.write('tags: ["%s"] \n' % '", "'.join(tags))
        if 'updated' in entry:
            output.write('lastmod: %s\n' % lastmod)
        output.write('type: %s\n' % contenttype)
        output.write('---\n')
        output.write(md(content))
        output.close()

    #
    ## RSS Case - to implement ?
    #

if __name__ == '__main__':
    main()
