import re, warnings, os, shutil
from functools import reduce
from classes import *

#DONE
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    md = open(from_path).read()
    template = open(template_path).read()

    # blocks is a list of Block objects
    blocks = markdown_to_blocks(md)
    title = extract_title(md)

    # map blocks as list-of-Blocks into nodes as list-of-nodes
    nodes = list(map(lambda x: Node(x), blocks))
    content = list(map(lambda n: n.get_HTML(), nodes))
    content = "\n".join(content)

    template = template.replace("{{ Content }}", content)
    template = template.replace("{{ Title }}", title)

    if os.path.exists(dest_path):
        os.remove(dest_path)
    f = open(dest_path, "w")
    f.write(template)

#DONE
def extract_title(md):
    match = re.findall(r"^# (.+)", md)
    if not match:
        raise Exception("Error: title not found")
    return match[0]

#DONE
def cp_to_public(top_dir, relative_path=""):
    # this function lists the current directory
    # then copies all non-directories
    # then recursively calls itself on all sub-directories
    curr_dir_path = os.path.join(top_dir, relative_path)
    curr_dir_list = os.listdir(curr_dir_path)
    curr_target_dir = os.path.join("./public", relative_path)
    # print(f"{curr_dir_list}\n{curr_target_dir}")
    for item in curr_dir_list:
        item_path =  os.path.join(curr_dir_path, item)
        if os.path.isfile(item_path):
            # print(f"found file: {item_path}\ncp to {curr_target_dir}")
            shutil.copy(item_path, curr_target_dir)
        else:
            os.mkdir(os.path.join(curr_target_dir, item))
            cp_to_public(top_dir, item)

#DONE
def markdown_to_blocks(md):
    # check if empty
    if md == "":
        raise Exception("Invalid md: md cannot be an empty string")
    
    # scan md and extract code blocks first, that way we do not parse them
    ans = extract_code_blocks(md)
    # ans is now a hybrid list of strings and Block(code)

    ans = extract_quote_blocks(ans)

    # now we scan the strings and split out any images into their own blocks.
    ans = split_image_blocks(ans)

    # now we handle heading blocks
    ans = recognize_heading_blocks(ans)

    # everything else is going to be treated as a paragraph
    ans = list(map(lambda x: x if isinstance(x, Block) else Block(x, BlockType.PARAGRAPH), ans))

    return ans
    

#TODO
def extract_quote_blocks(blocks):
    ans = []
    in_quote_block = False
    curr_str = ""
    for b in blocks:
        if isinstance(b, Block):
            ans.append(b)
            continue
        if len(b) > 0 and b[0] == ">" and not in_quote_block:
            # entering quote block
            in_quote_block = True
            curr_str += b + "\n"
        elif len(b) > 0 and b[0] == ">" and in_quote_block:
            # continuing quote block
            curr_str += b + "\n"
        elif len(b) > 0 and b[0] != ">" and in_quote_block:
            # exiting quote block
            in_quote_block = False
            ans.append(Block(curr_str, BlockType.QUOTE))
            curr_str = ""
            ans.append(b)
        else:
            ans.append(b)
    return ans

#DONE
def extract_code_blocks(md):
    ans = []
    curr_str = ""
    in_code_block = False
    for line in md.split("\n"):
        if not in_code_block and line == "```":
            # entering into code block
            # curr_str = line + "\n" # we don't actually want to store this delimiter
            in_code_block = True
        elif in_code_block and line != "```":
            # continuing code block
            curr_str += line + "\n"
        elif in_code_block and line == "```":
            # exiting code block
            ans.append(Block(curr_str, BlockType.CODE))
            curr_str = ""
            in_code_block = False
        elif line != "":
            # non-empty single-line block
            ans.append(line)
    return ans

#DONE
def split_image_blocks(blocks):
    ans = []
    for b in blocks:
        if isinstance(b, Block):
            # already a block, don't parse this
            ans.append(b)
            continue

        # parse the string for image substrings
        matches = re.findall(r"!\[(.*?)\]\((.*?)\)", b)
        
        # if no img substrings are found, just append this as a string and move on
        if not matches:
            ans.append(b)
            continue

        # otherwise, matches is nonempty. We must scan through each match and perform a split
        string_to_split = b
        while len(matches) > 0:
            m = matches.pop(0)
            m = f"![{m[0]}]({m[1]})"
            # m is the image substr

            # append the nonempty string up until image
            string_until_m = string_to_split.split(m, 1)[0]
            string_to_split = string_to_split.split(m, 1)[1]

            if string_until_m != "":
                warnings.warn(f"Warning: I do not allow images in paragraphs. \npara=\n{b}")
                ans.append(string_until_m)
            
            # append the image block
            ans.append(Block(m, BlockType.IMAGE))

        # append any remaining string after the last image
        if string_to_split != "":
            ans.append(string_to_split)
        
        # after this loop, the entire string should be split into image blocks or substrings
    return ans

#DONE        
def recognize_heading_blocks(blocks):
    ans = []

    for b in blocks:
        #if b is a block just append and continue
        if isinstance(b, Block):
            ans.append(b)
            continue

        #otherwise it's a string. Detect if its a heading block
        is_heading = bool(re.match(r"#{1,6} ", b))
        if is_heading:
            ans.append(Block(b, BlockType.HEADING))
            continue

        # if its not a heading, just append the string
        ans.append(b)


    return ans

