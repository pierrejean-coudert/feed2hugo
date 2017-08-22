# Feed2Hugo

Migration tool to migrate from a RSS/Atom Feed to [Hugo](https://gohugo.io/) static site generator.

## Requirements

* Python 3+ (not tested with Python 2)
* Feedparser

```
pip install feedparser
```

## Usage

Run :

```
python feed2hugo.py -f <url_or_path_to_feed> -t <hugo_root_path> [-c post]
```
Specify value for `-c` only if your content type is not `post`.
