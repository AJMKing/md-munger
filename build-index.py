import markdown
import os
import argparse
import re
from dataclasses import dataclass
from jinja2 import Template

md = markdown.Markdown(extensions=['fenced_code','meta'])

template = Template("""<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    {% for css in stylesheets %}
    <link rel="stylesheet" href="{{ css }}">
    {% endfor %}    
    <title>{{ title }}</title>
</head>
<body>
<header>
  <a href="/index.html">Homepage</a><br>
</header>
<h1>{{title}}</h1>
<p class="diverge"><a href="bio.html">Bio</a></p>
<p class="diverge"><a href="https://github.com/ajmking">Github</a></p>
<p class="diverge"><a href="https://linkedin.com/in/ajmking.com">Linkedin</a></p>
<h2>Pages</h2>
{% for page in pages %}
<p class="diverge"><a href=/{{ page.path }}>{{page.name}}</a></p>
{% endfor %}
<h2>Programs</h2>
See <a href="https://github.com/ajmking">Github</a> for now.</br>
</body>
</html>
""")

@dataclass
class Page():
    name: str = ""
    path: str = ""


def get_title(page):
    with open(page) as f:
        match = re.search(r'<title>(.*?)</title>', f.read())
    return match.group(1) if match else None

def get_pages(page_path):
    if page_path == None or page_path == "":
        page_path = "pages"

    pages = []
    for f in sorted(os.listdir(page_path)):
        path = os.path.join(page_path,f)
        pages.append(Page(name=get_title(path),path=path))
    return pages


def parse_args():
    parser = argparse.ArgumentParser(description='Convert Markdown to HTML')
    parser.add_argument('-f', '--file', help='path to files')
    return parser.parse_args()

def main():

    args = parse_args()
    page_path = args.file
    pages = get_pages(page_path)
    html = template.render(title="A. J. M. King", pages=pages, stylesheets=["/style.css"])
    with open("index.html", "w") as w:
        w.write(html)

if __name__ == "__main__":
    main()
    
    


    
