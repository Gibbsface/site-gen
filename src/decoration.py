
decorators = [
    "`",
    "*",
    "**",
    "_",
    "__",
    "~",
    "~~",
]

decorator_to_html = {
    "open": {
        "`": "<code>",
        "*": "<i>",        
        "**": "<b>",
        "_": "<i>",
        "__": "<b>",
        "~": "<s>",
        "~~": "<s>",        
    },
    "close": {
        "`": "</code>",
        "*": "</i>",        
        "**": "</b>",
        "_": "</i>",
        "__": "</b>",
        "~": "</s>",
        "~~": "</s>",        
    },
}
    
#TODO HANDLE LINKS
def convert_links(text):
    return text

def decorated_text_to_html(md):
    ans = convert_delimeters(md)
    ans = convert_links(ans)
    return ans

def convert_delimeters(md):
    # this is a doozy
    ans = ""
    curr_str = ""
    stack = []
    i = -1
    while i < len(md) - 1:
        i += 1
        c = md[i]
        if c not in decorators:
            ans += c
            continue


        # at this point, we know c is a decorator. We need to peek ahead and see if its 1 or 2
        try:
            after_c = md[i + 1]
        except IndexError:
            # this is the last c in the str, so it can only be a single closing tag:
            if len(stack) == 1 and stack[-1] == c:
                # this single closing delimiter closes the stack perfectly
                ans += decorator_to_html["close"][c]
                stack.pop()
                continue

        # print(f"TEST: found delimiter {c}\nans=\"{ans}\" \nafter_c={after_c}")
        
        # at this point we know that c is a decorator, and we know md[i+1] exists, so do some checks
        if after_c in decorators:
            c = c + after_c
            i += 1
            # print(f"TEST {c} is double")

        #at this point c is either the single or double delimiter, now let's check the stack to see open or closed
        if len(stack) > 0 and stack[-1] == c:
            # we are closing this tag
            stack.pop()
            ans += decorator_to_html["close"][c]
            # print(f"TEST: closing tag {c}\nans={ans} and md[i]={md[i]}\n")
        else:
            # we are opening this tag
            stack.append(c)
            ans += decorator_to_html["open"][c]
            # print(f"TEST: opening tag {c}\nans={ans} and md[i]={md[i]}\n")

    # if after the loop, the stack is not empty, then something is wrong
    if len(stack) > 0:
        raise Exception(f"Error: unbalanced decorators in paragraph: \n{md}")

    return ans