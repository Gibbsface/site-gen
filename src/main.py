from functions import *
from classes import *


def main():
    
    # import md
    try:
        path_to_md = "./markdown.md"
        markdown = open(path_to_md).read()
    except:
        raise Exception("Error: could not open or read markdown file")
        
    # blocks is a list of Block objects
    blocks = markdown_to_blocks(markdown)


    # split md into list of blocks
    # block class has a type and content

    # map list of blocks into a list of html strings
    # iter fun will take a block obj and turn it into an htmlParent
    # htmlParent obj will have tag, props, and innerHTML string

    # map list of htmlParents into a list of html strings

    # output html to file


    return 0

main()