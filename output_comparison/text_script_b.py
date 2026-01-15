import argparse
import difflib

a_string = """        "content": "\nHere are some suggestions to improve the accessibility of your PDF.\n\n1. **Add a Document Language:** Your PDF doesn\u2019t clearly specify the language it\u2019s written in (like English, Spanish, or French). This is important for screen readers to pronounce words correctly. In Acrobat, you can usually find this setting under \u201cFile\u201d -> \u201cProperties\u201d -> \u201cLanguage\u201d. Select the appropriate language from the dropdown menu.\n\n2. **Create a Proper Document Structure (Tags):** The PDF lacks a well-defined reading order and logical structure. Think of this like headings and paragraphs in a word processor. Screen readers use this structure to help people navigate the document. Acrobat has an \u201cAccessibility\u201d tool that can help you add tags, or automatically detect the reading order. You may need to review and correct the automatically generated tags to ensure they are accurate.\n\n3. **Mark Content as Artifact or Real Content:** The accessibility checker found a lot of content that isn\u2019t clearly identified as either meaningful text/images (real content) or purely decorative elements (artifact content). Screen readers will attempt to read *everything* in the document, including things that shouldn\u2019t be read aloud. In Acrobat, when you are in the tagging mode, you can set content to be marked as an artifact. This tells screen readers to ignore it. \n\nThese three steps will likely address the majority of the accessibility issues. There may be other, less critical things to improve, but focusing on these will make the biggest difference for people using assistive technology.\n\n\n\n",
"""

b_string = """        "content": "\nHere are some suggestions to improve the accessibility of your PDF.\n\n1. **Add a Document Language:** Your PDF doesn\u2019t clearly specify the language it\u2019s written in (like English, Spanish, or French). This is important for screen readers to pronounce words correctly. In Acrobat, you can go to File > Properties > Language and set the appropriate language.\n\n2. **Create a Proper Document Structure (Tags):** The PDF is missing a key element that tells screen readers how the document is organized \u2013 think of it like headings and paragraphs in a word processor. Acrobat has an \u201cAccessibility Check\u201d tool (Tools > Accessibility > Check Accessibility) that can help you identify missing tags and guide you through adding them. Focus on adding tags to headings, paragraphs, lists, and tables.\n\n3. **Mark Content as Artifact or Real Content:** The PDF checker found a lot of content that isn\u2019t clearly identified as either meaningful text/images (real content) or purely decorative elements (artifact content). Screen readers will attempt to read *everything* in the document, so marking decorative elements as \u201cartifact\u201d tells the screen reader to skip them. Again, Acrobat\u2019s Accessibility Check tool can help you find these areas and assign the correct classifications.\n\nAddressing these three areas will likely resolve the majority of the accessibility issues. There may be other, smaller improvements needed, but these are the most impactful to start with.\n\n\n\n","""


def compare_strings(str1: str, str2: str, show_whitespace: bool = True) -> None:
    """
    Compare two strings and show their differences.

    Args:
        str1: First string to compare
        str2: Second string to compare
        show_whitespace: Whether to highlight whitespace differences
    """
    print('=== STRING COMPARISON ===')
    print(f'String 1 length: {len(str1)} characters')
    print(f'String 2 length: {len(str2)} characters')
    print(f'Strings are identical: {str1 == str2}')
    print()

    if str1 == str2:
        print('No differences found.')
        return

    # Split into lines for line-by-line comparison
    lines1 = str1.splitlines(keepends=True)
    lines2 = str2.splitlines(keepends=True)

    print('=== LINE-BY-LINE DIFFERENCES ===')
    diff = difflib.unified_diff(lines1, lines2, fromfile='string_a', tofile='string_b', lineterm='')

    diff_output = list(diff)
    if diff_output:
        for line in diff_output:
            print(line)
    else:
        print('No line-by-line differences found.')

    print()

    # Character-level comparison for whitespace differences
    if show_whitespace:
        print('=== CHARACTER-LEVEL DIFFERENCES (INCLUDING WHITESPACE) ===')

        # Show character-by-character diff for the first differing line
        for i, (line1, line2) in enumerate(zip(lines1, lines2)):
            if line1 != line2:
                print(f'First difference found at line {i + 1}:')
                print(f'String A line {i + 1}: {repr(line1)}')
                print(f'String B line {i + 1}: {repr(line2)}')
                print()

                # Show character-level diff for this line
                char_diff = difflib.unified_diff(
                    list(line1), list(line2), fromfile='string_a_char', tofile='string_b_char', lineterm=''
                )

                print('Character-level differences:')
                for char_line in char_diff:
                    print(char_line.rstrip())
                break

        # Check if one string has more lines
        if len(lines1) != len(lines2):
            print(f'Line count difference: String A has {len(lines1)} lines, String B has {len(lines2)} lines')
            if len(lines1) > len(lines2):
                print('Extra lines in String A:')
                for i, line in enumerate(lines1[len(lines2) :], start=len(lines2) + 1):
                    print(f'  Line {i}: {repr(line)}')
            else:
                print('Extra lines in String B:')
                for i, line in enumerate(lines2[len(lines1) :], start=len(lines1) + 1):
                    print(f'  Line {i}: {repr(line)}')


def main() -> None:
    """
    Main function to run the string comparison.
    """
    parser = argparse.ArgumentParser(description='Compare two strings and show differences')
    parser.add_argument('--no-whitespace', action='store_true', help='Hide whitespace-only differences')
    args = parser.parse_args()

    show_whitespace = not args.no_whitespace
    compare_strings(a_string, b_string, show_whitespace)


if __name__ == '__main__':
    main()
