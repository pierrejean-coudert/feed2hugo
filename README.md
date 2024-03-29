# Feed2Hugo

Migration tool to migrate from a RSS/Atom Feed to [Hugo](https://gohugo.io/) static site generator.

Used to migrate Dotclear 1.2 and 2 blogs to Hugo.

Forked from https://code.cerenit.fr/nsteinmetz/feed2hugo 

Improvements:
- download all post images
- store each post & related images in a dedicated directory
- adapt images src in posts markdown

## Requirements

* Python 3+ (not tested with Python 2)

```
python3 -m venv .venv 
source ./.venv/bin/activate
pip install -r requirements.txt
```

## Usage

Run :

```
python feed2hugo.py -f <url_or_path_to_feed> -t <hugo_root_path> [-c post]
```

Specify value for `-c` only if your content type is not `post`.

Examples:

```
python feed2hugo.py -f http://www.domain.com/blog/feed -t /home/user/path/to/hugo
```

or:

```
python feed2hugo.py -f http://www.domain.com/blog/feed -t /home/user/path/to/hugo -c blogpost
```

