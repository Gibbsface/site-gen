import re

from classes import *

###########################

#DONE
def markdown_to_blocks(md):
    # check if empty
    if md == "":
        raise Exception("Invalid md: md cannot be an empty string")
    
    # scan md and extract code blocks first, that way we do not parse them
    ans = extract_code_blocks(md)
    # ans is now a hybrid list of strings and Block(code)

    # now we scan the strings and split out any images into their own blocks.
    ans = split_image_blocks(ans)

    # now we handle heading blocks
    ans = recognize_heading_blocks(ans)

    # everything else is going to be treated as a paragraph
    ans = list(map(lambda x: x if isinstance(x, Block) else Block(x, BlockType.PARAGRAPH), ans))

    return ans
    
#DONE
def extract_code_blocks(md):
    ans = []
    curr_str = ""
    in_code_block = False
    for line in md.split("\n"):
        if not in_code_block and line == "```":
            # entering into code block
            curr_str = line + "\n"
            in_code_block = True
        elif in_code_block and line != "```":
            # continuing code block
            curr_str += line + "\n"
        elif in_code_block and line == "```":
            # exiting code block
            ans.append(Block(curr_str + line, BlockType.CODE))
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

