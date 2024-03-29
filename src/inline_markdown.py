import re
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
  new_nodes = []

  for node in old_nodes:
    print(node)
    if not isinstance(node, TextNode):
      new_nodes.append(node)
    else:
      split_text = node.text.split(delimiter)
      if len(split_text) % 2 == 0:
        raise Exception("Invalid Markdown: no starting/ending text type")
      counter = 0
      for i in split_text:
        if i == "":
          continue
        if counter % 2 == 0:
          new_nodes.append(TextNode(i, text_type_text))
          counter += 1
        else:
          new_nodes.append(TextNode(i, text_type))
          counter += 1

  return new_nodes

def extract_markdown_images(text):
  r_string = r"!\[(.*?)\]\((.*?)\)"
  matches = re.findall(r_string, text)
  return matches

def extract_markdown_links(text):
  r_string = r"\[(.*?)\]\((.*?)\)"
  matches = re.findall(r_string, text)
  return matches