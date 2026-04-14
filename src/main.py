from functions import *
from classes import Node
import os, shutil

pages = [
    "index.md",
    "blog/glorfindel/index.md",
    "blog/tom/index.md",
    "blog/majesty/index.md",
    "contact/index.md",
]

def main():
    # generate ./public from ./static
    if os.path.exists("./public"):
        shutil.rmtree("./public")
    os.mkdir("./public")
    cp_to_public("./static")

    for p in pages:
        generate_page("./content/" + p, "./template.html", "./public/" + p.replace(".md", ".html"))
    


    return 0

main()