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

  for old_node in old_nodes:
      if old_node.text_type != text_type_text:
          new_nodes.append(old_node)
          continue
      split_nodes = []
      sections = old_node.text.split(delimiter)
      if len(sections) % 2 == 0:
          raise ValueError("Invalid markdown, formatted section not closed")
      for i in range(len(sections)):
          if sections[i] == "":
            continue
          if i % 2 == 0:
            split_nodes.append(TextNode(sections[i], text_type_text))
          else:
            split_nodes.append(TextNode(sections[i], text_type))
      new_nodes.extend(split_nodes)
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
    if node.text_type != text_type_text:
      new_nodes.append(node)
      continue
    images = extract_markdown_images(node.text)
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
    if node.text_type != text_type_text:
      new_nodes.append(node)
      continue
    links = extract_markdown_links(node.text)
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
  
def text_to_textnodes(text):
  # splits a string of text to and array of text nodes broken up between bold, italic, code, image and link
  nodes = [TextNode(text, text_type_text)]
  nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
  nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
  nodes = split_nodes_delimiter(nodes, "`", text_type_code)
  nodes = split_nodes_image(nodes)
  nodes = split_nodes_link(nodes)
  return nodes