## TODO
- [x] in decoration, the function needs to handle link decoration
- [x] need to handle block quotes
- [x] need to handle unordered lists
- [ ] need to handle ordered lists


# Under the Hood
The parser will read `markdown.md` in the root of this directory. It can only handle the following block types and text decorators:

- Blocks
  - Code (multiline)
  - Paragraph
  - Image
  - Heading (all sizes)

- Text Decorations
  - Code (inline)
  - Link
  - Bold
  - Italic
  - Strikethrough

# Instructions
run with `./main.sh`
test with `./test.sh`

# Future Plans
- [ ] handle all valid markdown text decorations
- [ ] handle unordered lists
- [ ] handle ordered lists
- [ ] handle task lists
- [ ] handle horizontal rules

## Last Updated April 12, 2026