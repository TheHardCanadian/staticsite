from textnode import TextNode, TextType
import re   


delimiters = {'bold':["**", "__"],
              "italic": ["*", "_"],
              "code":["`"], 
    }

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    
    #def delimit_string(inside_delimiter, new_nodes)
    if delimiter not in delimiters[text_type.value]:
        raise Exception("Delimiter error: Improper delimiter")

    current_text = ""
    new_nodes = []
    inside_delimiter = False
    i=0
    while i < len(old_nodes):
        if old_nodes[i:].startswith(delimiter):
            if current_text: #this means if the string is not empty
                node_type = text_type if inside_delimiter else TextType.PLAIN_TEXT
                new_nodes.append(TextNode(current_text,node_type))
                current_text = ""
            inside_delimiter = not inside_delimiter
            i += len(delimiter)
        else:
            current_text += old_nodes[i]
            i+=1

    if current_text:
        node_type = text_type if inside_delimiter else TextType.PLAIN_TEXT
        new_nodes.append(TextNode(current_text,node_type))

    return new_nodes    

def regex_find_image(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def regex_find_link(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(text, find_image):
    new_text = text
    new_nodes = []
    matches = find_image(text)
    
    #print(matches)
    i=0
    for i in range(len(matches)):
        split_text = new_text.split(f"![{matches[i][0]}]({matches[i][1]})",1)
        split_text1 = split_text[0]
        new_text = split_text[1]
        new_nodes.append(TextNode(split_text1,TextType.PLAIN_TEXT))
        new_nodes.append(TextNode(matches[i][0],TextType.IMAGE,matches[i][1]))
        i+=1
    
    if new_text:
        new_nodes.append(TextNode(new_text, TextType.PLAIN_TEXT))
    
    return new_nodes
    
def split_nodes_link(text, find_link):
    new_text = text
    
    new_nodes = []
    
    matches = find_link(text)
    
    #print(matches)
    i=0
    for i in range(len(matches)):
        split_text = new_text.split(f"[{matches[i][0]}]({matches[i][1]})",1)
        split_text1 = split_text[0]
        new_text = split_text[1]
        new_nodes.append(TextNode(split_text1,TextType.PLAIN_TEXT))
        new_nodes.append(TextNode(matches[i][0],TextType.LINK,matches[i][1]))
        i+=1
    
    if new_text:
        new_nodes.append(TextNode(new_text, TextType.PLAIN_TEXT))
    
    return new_nodes

def text_to_textnodes(text):

    text_type_map = {
        "bold":TextType.BOLD_TEXT,
        "italic":TextType.ITALIC_TEXT,
        "code":TextType.CODE_TEXT,
        "image":TextType.IMAGE,
        "link": TextType.LINK
    }

    text_node = [TextNode(text,TextType.PLAIN_TEXT)]
    new_node = text_node

    temp_node=[]
    for node in new_node:
        if node.text_type == TextType.PLAIN_TEXT:
            temp_node.extend(split_nodes_image(node.text, regex_find_image))
        else:
            temp_node.append(node)
    new_node = temp_node

    temp_node=[]
    for node in new_node:
        if node.text_type == TextType.PLAIN_TEXT:
            temp_node.extend(split_nodes_link(node.text, regex_find_link))
        else:
            temp_node.append(node)
    new_node = temp_node

    for text_type, delimiter_list in delimiters.items():
        for delimiter in delimiter_list:
            temp_node=[]
            for node in new_node:
                if node.text_type == TextType.PLAIN_TEXT:
                    new_split = split_nodes_delimiter(node.text, delimiter, text_type_map[text_type])
                    temp_node.extend(new_split)
                else:
                    temp_node.append(node) 
            new_node = temp_node                                                                                                                                                                                                                                                             
    #print(f"Delimiter Node Output: {new_node}")

    #loop through new_node and use regex image for each
    

    #print(f"Final Node Output: {new_node}")
    return new_node

#text_to_textnodes("This is **bold text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
#text_to_textnodes("This is **bold text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev) and some more text to top it off")
#text_to_textnodes("This is **bold text** with an _italic_ word and a `code block` and a `second code block` and a `third code block` and a `fourth code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
#text_to_textnodes("This is **bold text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
#result = text_to_textnodes("This is **bold text** with an _italic_ word and another _italic word_ along with a **second bold text** followed by a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a ![Qui-Gon Jinn image] and a [link](https://boot.dev)")
#print(result)

