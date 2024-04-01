import re

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
        if re.match(r"^\d\.", split_block[i]) == None:
            break
        if i+1 == len(split_block):
            return block_type_ordered_list
        
    # default to paragraph block type
    return block_type_paragraph

print(block_to_block_type("""
1. This is a heading
2. This is a paragraph of text. It has some **bold** and *italic* words inside of it.
3. This is a list item
4. This is another list item
"""))