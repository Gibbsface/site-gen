from functions import *
import os, shutil, sys

def main():
    # get dynamic basepath
    basepath = "/" if len(sys.argv) == 1 else sys.argv[1]
    build_dir = "docs"

    # generate ./public from ./static
    if os.path.exists("./" + build_dir):
        shutil.rmtree("./" + build_dir)
    os.mkdir("./" + build_dir)
    cp_to_public("./static", build_dir)

    rec_generate_pages("./content", "./template.html", "./" + build_dir, basepath)

    return 0

main()