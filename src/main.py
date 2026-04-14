from functions import *
from classes import Node
import os, shutil

def main():
    # generate ./public from ./static
    if os.path.exists("./public"):
        shutil.rmtree("./public")
    os.mkdir("./public")
    cp_to_public("./static")

    rec_generate_pages("./content", "./template.html", "./public")

    return 0

main()