import re
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link
)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
  new_nodes = []

  for node in old_nodes:
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

def split_nodes_image(old_nodes):
  new_nodes = []
  for node in old_nodes:
    images = extract_markdown_images(node.text)
    if len(images) == 0:
      new_nodes.append(node)
      continue
    split_text = []
    temp_split = node.text
    for i in range(len(images)):
      temp_split = temp_split.split(f"![{images[i][0]}]({images[i][1]})", 1)
      split_text.extend([temp_split[:-1][0], [images[i][0], images[i][1]]])
      temp_split = temp_split[-1]
    split_text.append(temp_split)
    for i in split_text:
      if i == "":
        continue
      if isinstance(i, str):
        new_nodes.append(TextNode(i, text_type_text))
      else:
        new_nodes.append(TextNode(i[0], text_type_image, i[1]))
    return new_nodes



def split_nodes_link(old_nodes):
  new_nodes = []
  for node in old_nodes:
    links = extract_markdown_links(node.text)
    if len(links) == 0:
      new_nodes.append(node)
      continue
    split_text = []
    temp_split = node.text
    for i in range(len(links)):
      temp_split = temp_split.split(f"[{links[i][0]}]({links[i][1]})", 1)
      split_text.extend([temp_split[:-1][0], [links[i][0], links[i][1]]])
      temp_split = temp_split[-1]
    split_text.append(temp_split)
    for i in split_text:
      if i == "":
        continue
      if isinstance(i, str):
        new_nodes.append(TextNode(i, text_type_text))
      else:
        new_nodes.append(TextNode(i[0], text_type_link, i[1]))
  return new_nodes
  

node = [TextNode(
  "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
  text_type_text,
)]

print(split_nodes_link(node))