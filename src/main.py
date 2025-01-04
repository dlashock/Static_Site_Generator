import os
from pathlib import Path
import shutil
from copystatic import copy_all, generate_pages_recursively
from block_markdown import extract_title

public_dir_path = "./public"
static_dir_path = "./static"
source_path = "./content/"
template_path = "./template.html"
destination_path = "./public"

def del_all(dir):
    print(f"Deleting Directory and all contents: {dir}")
    if os.path.exists(dir):
        shutil.rmtree(dir)

def main():
    if os.path.exists(public_dir_path):
        del_all(public_dir_path)
    copy_all(static_dir_path, public_dir_path)
    generate_pages_recursively(source_path, template_path, destination_path)

main()