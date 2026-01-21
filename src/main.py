from textnode import TextType, TextNode
import os
from shutil import copy, rmtree

def source_to_dest(source, destination):
    #first - delete contents from source.
    if not os.path.exists(source):
        raise ValueError("Source path does not exist")
    
    if not os.path.exists(destination):
        raise ValueError("Destination path does not exist")
    
    print(f"Source path exists: {os.path.exists(source)}")
    print(f"Destination path exists: {os.path.exists(destination)}")



    dest_directory = os.listdir(destination)
    print(f"Destination directory being deleted: {dest_directory}")
    for item in dest_directory:
        item_path = os.path.join(destination, item)
        print(f"Item Path: {item_path}")
        if os.path.isdir(item_path):
            rmtree(item_path)
        else:
            os.remove(item_path)
    
    
    print(f"Destination before: {destination}")

    list_dir = os.listdir(source)
    
    
    print(f"Source: {list_dir}")
    
    for i in list_dir:
        filepath = os.path.join(source, i)
        print(filepath)
        if not os.path.isfile(filepath):
            os.mkdir(os.path.join(destination, i))
            print("Directory Created")
            new_destination = os.path.join(destination,i)
            source_to_dest(filepath, new_destination)
        elif os.path.isfile(filepath):
            copy(filepath, destination)
            print(f"Copied: {i}")

        print(f"Updated Destination:{os.listdir(destination)}")

    print(f"Final Destination:{os.listdir(destination)}")                


def main():
    source_to_dest("static/", "public/") 



if __name__ == "__main__":
    main()
