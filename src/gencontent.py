import os
from blocks import markdown_to_html, extract_markdown

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    markdown_file = open(from_path)
    markdown_content = markdown_file.read()
    markdown_file.close()

    markdown_file_template = open(template_path)
    markdown_content_template = markdown_file_template.read()
    markdown_file_template.close()

    title = extract_markdown(markdown_content)
    print(f"Title: {title}")

    node = markdown_to_html(markdown_content)
    node_html = node.to_html()
    print(f"Node HTML: {node_html}")

    final_html = markdown_content_template.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", node_html)
    final_html = final_html.replace('href="/',f'href="{basepath}')
    final_html = final_html.replace('src="/',f'src="{basepath}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, 'w') as dest_file:
        dest_file.write(final_html)
    
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    print("Generating pages...")
    dest_dir_path_file = os.path.join(dest_dir_path, "index.html")
    directory = os.listdir(dir_path_content)
    print(f"Directory: {directory}")
    for i in directory:
        print(f"I is {i}")
        joined = os.path.join(dir_path_content, i)
        print(f"Joined directory/file path {joined}")
        if os.path.isfile(joined):
            if joined.endswith(".md"):
                generate_page(joined, template_path, dest_dir_path_file, basepath)
                
        else:
            print(f"Need to make a new path for next directory")
            new_dest_path_directory = os.path.join(dest_dir_path,i)
            print(f"New joined destination path folder: {new_dest_path_directory}")
            if not os.path.exists:
                print(f"Path {new_dest_path_directory} doesn't exit, making new path before")
                new_dest_path_directory = os.mkdir(new_dest_path_directory)
            generate_pages_recursive(joined, template_path, new_dest_path_directory, basepath)



    """"
    In generate_page, after you replace the {{ Title }} and {{ Content }}, replace any instances of:
href="/ with href="{basepath}
src="/ with src="{basepath}
    
    Create a generate_pages_recursive(dir_path_content, template_path, dest_dir_path) function. It should:
Crawl every entry in the content directory

For each markdown file found, generate a new .html file using the same template.html. 
The generated pages should be written to the public directory in the same directory structure.
Change your main function to use generate_pages_recursive instead of generate_page. 
You should generate a page for every markdown file in the content directory and write the results to the public directory.

Run the new program and ensure that both pages on the site are generated correctly and you can navigate between them."""



