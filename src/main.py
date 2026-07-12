from textnode import TextNode, TextType
from copystatic import copystatic
from generate_page import generate_page
from generate_pages_recursive import generate_pages_recursive
import sys

def main():
    if len(sys.argv) == 1:
        basepath = "/"
    elif len(sys.argv) == 2:
        basepath = sys.argv[1]
    else:
        raise Exception("Error: invalid argument entered")
    copystatic()
    #generate_page("content/index.md","template.html","public/index.html",basepath)
    generate_pages_recursive("./content","template.html","./docs",basepath)
main()