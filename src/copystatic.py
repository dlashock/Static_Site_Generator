import os, shutil
from block_markdown import markdown_to_html_node, extract_title
from htmlnode import HTMLNode, LeafNode, ParentNode

def copy_all(source, destination):
    src_items = os.listdir(source)
    print(f"Printing all files from top level of source directory: {source}")
    for item in src_items:
        print(os.path.join(source, item))
    if not os.path.exists(destination):
        print(f"Creating destination directory: {destination}")
        os.mkdir(f"{destination}")
    for item in src_items:
        if os.path.isdir(os.path.join(source, item)):
            print(f"Directory found. Creating {os.path.join(source, item)}")
            copy_all(os.path.join(source, item), os.path.join(destination, item))
        elif os.path.isfile(os.path.join(source, item)):
            print(f"File found. Copying file from source to destination: {os.path.join(source, item)}")
            shutil.copy(os.path.join(source, item), os.path.join(destination, item))

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}...")
    
    # Open and read contents from the source file
    with open(from_path, "r") as file:
        from_contents = file.read()

    # Open and read contents from the template file
    with open(template_path, "r") as file:
        template_contents = file.read()

    # Convert markdown file to an HTML string and extract the title
    content = markdown_to_html_node(from_contents)
    content_string = content.to_html()
    title = extract_title(from_contents)
    
    # Replace {{ Title }} and {{ Content }} in the template file with the title and content from source file
    template_contents = template_contents.replace("{{ Content }}", content_string)
    template_contents = template_contents.replace("{{ Title }}", title)
    
    print(f"Creating {dest_path} with updated {template_path} file...")
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as file:
        file.write(template_contents)

def generate_pages_recursively(dir_path_content, template_path, dest_dir_path):
    pass