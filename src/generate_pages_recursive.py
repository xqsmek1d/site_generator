from markdown_to_html_node import markdown_to_html_node
from markdown_blocks import extract_title
import os

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str) -> None:
    #print(f"Generating pages from {dir_path_content} to {dest_dir_path} using {template_path}")
    for entry in os.listdir(dir_path_content):
        content_fpath = os.path.join(dir_path_content,entry)
        #print(content_fpath)
        if entry == "index.md":
            dest_fpath = os.path.join(dest_dir_path,"index.html")

            print(f"Copy {content_fpath} to {dest_fpath}")
            with open(content_fpath) as f:
                markdown = f.read()
            with open(template_path) as f:
                template = f.read()

            HTML_string = markdown_to_html_node(markdown).to_html()
            page_title = extract_title(markdown)
            template = template.replace("{{ Title }}", page_title)
            template = template.replace("{{ Content }}", HTML_string)
            template = template.replace('href="/',f'href="{basepath}')
            template = template.replace('src="/',f'src="{basepath}')

            os.makedirs(os.path.dirname(dest_fpath), exist_ok=True)
            with open(dest_fpath, "w") as f:
                f.write(template)

        elif os.path.isdir(content_fpath):
            dest_fpath = os.path.join(dest_dir_path,entry)
            generate_pages_recursive(content_fpath, template_path, dest_fpath, basepath)
        else:
            raise Exception("Error: something unexpected occured while generating HTML pages recursively")