from markdown_to_html_node import markdown_to_html_node
from markdown_blocks import extract_title
import os

def generate_page(from_path:str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as f:
        template = f.read()
    
    HTML_string = markdown_to_html_node(markdown).to_html()
    page_title = extract_title(markdown)
    template = template.replace("{{ Title }}", page_title)
    template = template.replace("{{ Content }}", HTML_string)

    # Create output directory and write result to it
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template)