import os
from block_markdown import ( 
  markdown_to_blocks,
  markdown_to_html_node
)


def extract_title(markdown):
  blocks = markdown_to_blocks(markdown)
  for block in blocks:
    if block.startswith('# '):
      return block[2:]
  raise Exception("Markdown has no h1, all pages require a h1 header")

def generate_page(from_path, template_path, dest_path):
  print(f"Generating page from {from_path} to {dest_path} using {template_path}")

  html = None

  # get html template
  with open(template_path) as template:
    read_data = template.read()
    html = read_data

  # get md content and convert it to html
  with open(from_path) as md_content:
    read_data = md_content.read()
    title = extract_title(read_data)
    md_as_html = markdown_to_html_node(read_data).to_html()

    # replace placeholder title and content with new title and html content respectively
    html = html.replace("{{ Title }}", title).replace("{{ Content }}", md_as_html)

  if not os.path.exists(os.path.dirname(dest_path)):
    print(f"Creating path to {dest_path}...")
    os.makedirs(os.path.dirname(dest_path))

  print(f"Creating new file {dest_path}...")
  with open(dest_path, 'w') as new_file:
    new_file.write(html)