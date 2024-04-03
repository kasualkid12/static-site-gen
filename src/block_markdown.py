import re
from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(block):
    # find if the start of block matches MD heading
    if re.match(r"^#?#?#?#?#?# \w", block) != None:
        return block_type_heading
    
    # find if start and end of block matched code
    if re.match(r"^```[\s\S]+?```$", block) != None:
        return block_type_code
    
    # split the block for use in finding other block types
    split_block = block.split('\n')

    # loop through the split block checking if all lines start with the quote match
    for i in range(len(split_block)):
        if split_block[i] == '':
            if i+1 == len(split_block):
              return block_type_quote
            continue
        if re.match(r"^>", split_block[i]) == None:
            break
        if i+1 == len(split_block):
            return block_type_quote

    # loop through the split block checking if all lines start with the unordered list matches    
    for i in range(len(split_block)):
        if split_block[i] == '':
            if i+1 == len(split_block):
              return block_type_unordered_list
            continue
        if re.match(r"^\*|-", split_block[i]) == None:
            break
        if i+1 == len(split_block):
            return block_type_unordered_list

    # loop through the split block checking if all lines start with the ordered list match
    for i in range(len(split_block)):
        if split_block[i] == '':
            if i+1 == len(split_block):
              return block_type_ordered_list
            continue
        if re.match(r"^\d+\.", split_block[i]) == None:
            break
        if i+1 == len(split_block):
            return block_type_ordered_list
        
    # default to paragraph block type
    return block_type_paragraph

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def block_to_quote(block):
    split_block = block.split('\n')
    new_lines = []
    for line in split_block:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def block_to_ulist(block):
    split_block = block.split('\n')
    html_items = []
    for line in split_block:
        if line[0] == '*':
            stripped_line = line.lstrip("* ")
        else:
            stripped_line = line.lstrip("- ")
        children = text_to_children(stripped_line)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def block_to_olist(block):
    split_block = block.split('\n')
    html_items = []
    for i in range(len(split_block)):
        stripped_line = split_block[i].lstrip(f"{i+1}. ")
        children = text_to_children(stripped_line)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)

def block_to_code(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])

def block_to_heading(block):
    for i in range(len(block)):
        if i > 6:
            raise Exception("Markdown Error: too many Heading tags")
        if block[i] != '#':
            text = block[i+1:]
            children = text_to_children(text)
            return ParentNode(f"h{i}", children)

def block_to_paragraph(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        type = block_to_block_type(block)
        if type == block_type_quote:
            children.append(block_to_quote(block))
            continue
        elif type == block_type_unordered_list:
            children.append(block_to_ulist(block))
            continue
        elif type == block_type_ordered_list:
            children.append(block_to_olist(block))
            continue
        elif type == block_type_code:
            children.append(block_to_code(block))
            continue
        elif type == block_type_heading:
            children.append(block_to_heading(block))
            continue
        elif type == block_type_paragraph:
            children.append(block_to_paragraph(block))
        else:
            raise ValueError("Invalid block type")
    return ParentNode("div", children, None)