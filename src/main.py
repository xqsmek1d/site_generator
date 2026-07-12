from textnode import TextNode, TextType
from copystatic import copystatic
from generate_page import generate_page
from generate_pages_recursive import generate_pages_recursive

def main():
    copystatic()
    #generate_page("content/index.md","template.html","public/index.html")
    generate_pages_recursive("./content","template.html","./public")
main()