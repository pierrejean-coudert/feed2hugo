import os, sys, re
from argparse import ArgumentParser
import feedparser
import shutil
from slugify import slugify
from markdownify import markdownify as md
from bs4 import BeautifulSoup as bs
import requests


def download_image(url, image_path):
    try:
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(image_path, "wb") as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
        else:
            print(r.status_code, "error loading", url)
    except Exception as e:
        print(e, url)


def dump_images(html, dest):
    """
    Downloads images referenced by html to dest path
    returns a dict {"image_src_url_in_html": "image_filename"}
    """
    soup = bs(html, features="html.parser")

    links = dict()
    for image in soup.findAll("img"):
        url = image["src"]
        filename = url.split("/")[-1].replace(" ", "_")
        image_path = os.path.join(dest, filename)
        links[url] = filename
        if not os.path.exists(image_path):
            download_image(url, image_path)

    return links


def feed_to_hugo(feed_url, hugo_root_path, content_type):
    f = feedparser.parse(feed_url)
    p = re.compile("https?:\/\/[a-z.]+")
    for entry in f.entries:
        title = entry.title

        baseUrl = p.match(entry.link).group(0)
        link = entry.link[len(baseUrl) :]

        if "updated" in entry:
            lastmod = entry.updated

        if "published" in entry:
            date = entry.published
        elif "updated" in entry:
            date = entry.updated

        author = entry.author
        tags = [t["term"] for t in entry.tags]

        content = None
        if "content" in entry:
            content = entry.content[0].value

        dest_path = os.path.join(
            hugo_root_path, "content", content_type, slugify(entry.title)
        )
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)

        with open(os.path.join(dest_path, "index.md"), "w") as f:
            # front matter
            f.write("---\n")
            f.write(f"date: {date}\n")
            f.write('title: "%s"\n' % title.replace('"', "'"))
            f.write(f"author: {author}\n")
            f.write(f'alias: ["{link}"]\n')
            if tags:
                f.write('tags: ["%s"] \n' % '", "'.join(tags))
            if "updated" in entry:
                f.write(f"lastmod: {lastmod}\n")
            f.write(f"type: {content_type}\n")
            f.write("---\n")

            # build markdown content
            if content:
                links = dump_images(content, dest_path)
                md_content = md(content)
                # replace images sources with local images references
                for link, filename in links.items():
                    md_content = md_content.replace(link, filename)
                f.write(md_content)


if __name__ == "__main__":
    parser = ArgumentParser(description="Parse RSS/ATOM feed to generate Hugo blog")
    parser.add_argument(
        "-f", "--feed", required=True, dest="feed", help="Feed url or path to feed file"
    )
    parser.add_argument(
        "-t",
        "--target",
        required=True,
        dest="target",
        help="Root path for Hugo project",
    )
    parser.add_argument(
        "-c", "--contenttype", dest="content_type", default="post", help="project file"
    )
    args = parser.parse_args()

    feed_to_hugo(args.feed, args.target, args.content_type)
