import markdown
import os
import re
import argparse
from jinja2 import Template

md = markdown.Markdown(extensions=['fenced_code','meta'])

template = Template("""<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    {% for css in stylesheets %}
    <link rel="stylesheet" href="{{ css }}">
    {% endfor %}
    <script src="/mermaid.min.js"></script>
    <title>{{ title }}</title>
</head>
<body>
<header>
  <a href="/index.html">Homepage</a><br>
</header>
<h1>{{title}}</h1>
{{ content }}
</body>
<hr>
</html>
""")

def convert2html(page_path):
    doc = None
    with open(page_path, "r", encoding="utf-8") as f:
        doc = md.convert(f.read())
    
    doc = doc.replace('<p>-&gt; <a ', '<p class="diverge"><a ')


    doc = re.sub(
        r'<pre><code class="language-mermaid">(.*?)</code></pre>',
        r'<pre class="mermaid">\1</pre>',
        doc,
        flags=re.DOTALL
    )

    title = md.Meta.get('title', ['BLANK'])[0]

    html = template.render(title=title, stylesheets=["/style.css"], content=doc)
    return (html,title)


def parse_args():
    parser = argparse.ArgumentParser(description='Convert Markdown to HTML')
    parser.add_argument('-f', '--file', help='path to file')
    return parser.parse_args()

def main():

    args = parse_args()
    page = args.file
    output_path="pages"
    html,title = convert2html(page)
    name = os.path.join(output_path,f"{title.lower().replace(' ', '-')}.html")
    with open(name, "w") as w:
        w.write(html)
    print(f"Wrote {name}")
if __name__ == "__main__":
    main()
    
    


    
