from textnode import TextNode, TextType
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type, closing_delimiter=None):
    
    delimiters = {'bold':["**", "__"],
                  "italic": ["*", "_"],
                  "code":["`"], 
                  "image":["!["], 
                  "link":["["]
    }

    closing_delimiters = {"image": "]",
                          "link": "]"
                          }
    
    #def delimit_string(inside_delimiter, new_nodes)
    if delimiter not in delimiters[text_type.value]:
        raise Exception("Delimiter error: Improper delimiter")
    if closing_delimiter:
        if text_type.value not in closing_delimiters:
            raise KeyError(f"Text type {text_type.value} does not support closing delimiters")
        if closing_delimiter != closing_delimiters[text_type.value]:
            raise Exception("Delimiter error: Improper closing delimiter")
            
    current_text = ""
    new_nodes = []
    inside_delimiter = False
    i=0
    while i < len(old_nodes):
        if closing_delimiter:
            if old_nodes[i:].startswith(closing_delimiter) and not inside_delimiter:
                raise Exception("Delimeter error: Closing delimeter not lead by opening delimeter")
            elif old_nodes[i:].startswith(delimiter) and inside_delimiter:
                raise Exception("Delimeter error: Delimeter not followed by closing delimeter")
            if old_nodes[i:].startswith(delimiter):
                #found delimeter
                if current_text: #this means if the string is not empty
                    node_type = text_type if inside_delimiter else TextType.PLAIN_TEXT
                    new_nodes.append(TextNode(current_text,node_type))
                    current_text = ""
                inside_delimiter = not inside_delimiter
                i += len(delimiter)

            elif old_nodes[i:].startswith(closing_delimiter):
                if current_text: #this means if the string is not empty
                    node_type = text_type if inside_delimiter else TextType.PLAIN_TEXT
                    new_nodes.append(TextNode(current_text,node_type))
                    current_text = ""
                inside_delimiter = not inside_delimiter
                i += len(closing_delimiter)

            else:
                current_text += old_nodes[i]
                i+=1
        elif closing_delimiter == None:
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


#split_nodes_image("This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)", regex_find_image)
#split_nodes_image("This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev) along with some extra text.", regex_find_image)
    
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

#split_nodes_link("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", regex_find_link)
#split_nodes_link("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) along with some extra text.", regex_find_link)



#t4_no_url = regex_find_link("This is a [screenshot] of my screen and also a [profile pic] and the [company logo]")
#result2 = regex_find_link("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
#print(t4_no_url)
#print(result2)
