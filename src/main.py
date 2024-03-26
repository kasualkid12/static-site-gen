from textnode import TextNode
from htmlnode import (HTMLNode, LeafNode, ParentNode)

textnode1 = TextNode('This is a text node', 'bold', 'https://www.boot.dev')
textnode2 = TextNode('This is a text node', 'bold', 'https://www.boot.dev')
textnode3 = TextNode('This is text', 'bold')

print(textnode1 == textnode2)
print(textnode1 == textnode3)

print(textnode1)

node = HTMLNode(None, None, None, {"href": "https://www.google.com", "target": "_blank"})

print(HTMLNode.props_to_html(node))
print(repr(node))

node2 = ParentNode(
  "h2",
  [
    LeafNode("b", "Bold text"),
    LeafNode(None, "Normal text"),
    LeafNode("i", "italic text"),
    LeafNode(None, "Normal text"),
  ],
)

print(ParentNode.to_html(node2))