import json

md_file = r'c:\Users\khalil\Documents\courseGenerationWithLangraphAndCrawl4ai\docs\documentation.md'
html_file = r'c:\Users\khalil\Documents\courseGenerationWithLangraphAndCrawl4ai\docs\documentation.html'

with open(md_file, 'r', encoding='utf-8') as f:
    md_content = f.read()

with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

js_string = json.dumps(md_content)

prefix = html_content.split('const md =')[0]
suffix = '\n        c.innerHTML = marked.parse(md);' + html_content.split('c.innerHTML = marked.parse(md);')[1]

new_html = prefix + f'const md = {js_string};\n' + suffix

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(new_html)
print('HTML updated successfully.')
