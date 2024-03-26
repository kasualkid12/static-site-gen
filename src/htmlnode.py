class HTMLNode:
  def __init__(self, tag = None, value = None, children = None, props = None) -> None:
    self.tag = tag
    self.value = value
    self.children = children
    self.props = props

  def to_html(self):
    raise NotImplementedError("to_html method not implemented")
  
  def props_to_html(self):
    if self.props is None:
      return ""
    html = ""
    for key in self.props:
      html += f' {key}="{self.props[key]}"'
    return html
  
  def __repr__(self) -> str:
    return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
  
class LeafNode(HTMLNode):
  def __init__(self, tag, value, props = None) -> None:
    super().__init__(tag, value, None, props)

  def to_html(self):
    if self.value is None:
      raise ValueError("Invalid HTML: no value")
    if self.tag is None:
      return self.value
    return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

  def __repr__(self):
    return f"LeafNode({self.tag}, {self.value}, {self.props})"
  
class ParentNode(HTMLNode):
  def __init__(self, tag, children, props=None) -> None:
    super().__init__(tag, None, children, props)

  def to_html(self):
    if self.tag is None:
      raise ValueError("Invalid HTML: no tag")
    if self.children is None:
      raise ValueError("Invalid HTML: no children")
    
    html = f"<{self.tag}>"

    for child in self.children:
      html += child.to_html()

    return html + f"</{self.tag}>"


  def __repr__(self) -> str:
    return f"ParentNode({self.tag}, {self.children}, {self.props})"