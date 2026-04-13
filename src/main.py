from functions import *
from classes import Node
import os, shutil

def main():
    
    # import md
    try:
        path_to_md = "./markdown.md"
        markdown = open(path_to_md).read()
    except:
        raise Exception("Error: could not open or read markdown file")
        
    # blocks is a list of Block objects
    blocks = markdown_to_blocks(markdown)

    # map blocks as list-of-Blocks into nodes as list-of-nodes
    nodes = list(map(lambda x: Node(x), blocks))

    # output html to file
    try:
        path_to_index = "./public/index.html"
        f = open(path_to_index, "w")
        for n in nodes:
            f.write(n.get_HTML() + "\n")
    except:
        raise Exception("Error: could not write to index.html")

    return 0

def main():

    # delete all in public
    shutil.rmtree("./public")
    os.mkdir("./public")

    # copy all from static to public
    cp_to_public("./static")


main()