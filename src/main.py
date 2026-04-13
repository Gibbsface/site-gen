from functions import *
from classes import Node
import os, shutil

def main():
    # generate ./public from ./static
    if os.path.exists("./public"):
        shutil.rmtree("./public")
    os.mkdir("./public")
    cp_to_public("./static")

    generate_page("./content/index.md", "./template.html", "./public/index.html")
    
    return 0

main()