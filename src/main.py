from copystatic import copy_files_recursive
from generate_html import generate_pages_recursively

static_path = './static'
public_path = './public'
content_path = './content'
template_path = './template.html'
new_html_dest_path = './public'

def main():
  print('Copying static files to public directory...')
  copy_files_recursive(static_path, public_path)

  generate_pages_recursively(content_path, template_path, new_html_dest_path)

main()