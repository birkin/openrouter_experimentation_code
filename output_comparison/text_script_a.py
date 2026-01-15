"""
vibe-script to format long string for easier visual comparison.

usage: $ uv run ./text_script_a.py
"""

start_text = '''"\nHere are some suggestions to improve the accessibility of your PDF.\n\n1. **Add a Document Language:** Your PDF doesn\u2019t clearly specify the language it\u2019s written in (like English, Spanish, or French). This is important for screen readers to pronounce words correctly. In Acrobat, you can go to File > Properties > Language and set the appropriate language.\n\n2. **Create a Proper Document Structure (Tags):** The PDF is missing a key element that tells screen readers how the document is organized \u2013 think of it like headings and paragraphs in a word processor. Acrobat has an \u201cAccessibility Check\u201d tool (Tools > Accessibility > Check Accessibility) that can help you identify missing tags and guide you through adding them. Focus on adding tags to headings, paragraphs, lists, and tables.\n\n3. **Mark Content as Artifact or Real Content:** The PDF checker found a lot of content that isn\u2019t clearly identified as either meaningful text/images (real content) or purely decorative elements (artifact content). Screen readers will attempt to read *everything* in the document, so marking decorative elements as \u201cartifact\u201d tells the screen reader to skip them. Again, Acrobat\u2019s Accessibility Check tool can help you find these areas and assign the correct classifications.\n\nAddressing these three areas will likely resolve the majority of the accessibility issues. There may be other, smaller improvements needed, but these are the most impactful to start with.\n\n\n\n"'''


def format_text_as_paragraphs(text: str) -> str:
    """
    Formats the given text by removing extra quotes and preserving paragraph structure.
    """
    # Remove the outer quotes and leading/trailing whitespace
    cleaned_text = text.strip().strip('"')

    # Split by double newlines to identify paragraphs
    paragraphs = cleaned_text.split('\n\n')

    # Join paragraphs with single newlines for proper paragraph formatting
    formatted_paragraphs = []
    for paragraph in paragraphs:
        # Remove any leading/trailing whitespace from each paragraph
        clean_paragraph = paragraph.strip()
        if clean_paragraph:  # Only add non-empty paragraphs
            formatted_paragraphs.append(clean_paragraph)

    return '\n\n'.join(formatted_paragraphs)


def main() -> None:
    """
    Prints the start_text in proper paragraph format.
    """
    formatted_text = format_text_as_paragraphs(start_text)
    print(formatted_text)


if __name__ == '__main__':
    main()
