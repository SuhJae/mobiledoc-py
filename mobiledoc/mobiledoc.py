from typing import Union, List

from markdownify import markdownify as md


class Mobiledoc:
    def __init__(self, version: str = "0.3.2"):
        self.version = version
        self.markups = []  # includes formatting information
        self.atoms = []  # includes custom data (e.g., images)
        self.cards = []  # includes custom data (e.g., buttons)
        self.sections = []  # includes the actual text
        self.custom = {}  # user-defined custom data

    def _add_card(self, card):
        """ Helper method to add a card to mobiledoc """
        if card not in self.cards:
            self.cards.append(card)

        # find the index of the card and point to it
        card_idx = self.cards.index(card)
        self.sections.append([10, card_idx])

    def add_basic_text(self, text: Union[str, List[str]]):
        """ Method to add basic text to mobiledoc """
        if isinstance(text, str):
            self.sections.append([1, "p", [[0, [], 0, text]]])
        elif isinstance(text, list):
            for item in text:
                self.sections.append([1, "p", [[0, [], 0, item]]])

    def add_formatted_text(self, text: Union[str, List[str]]):
        """
        Method to convert markdown-like text to a custom format.

        This function takes in text, which can either be a string or a list of strings,
        and processes it to recognize certain markdown-like patterns. Each pattern corresponds
        to a specific tag, and the processed text is stored in the `sections` attribute.

        Parameters:
        - text: The input text, which can either be a single string or a list of strings.

        Usage:
        formatter = MarkdownFormatter()
        formatter.add_formatted_text("**bold** and *italic*")

        Supported Patterns:
        - **: bold
        - *: italic
        - ~~: strikethrough
        - ^^: superscript
        - ^: subscript
        - __: underline
        - `: code
        - [text](link): hyperlink
        """

        def process_text(t: str):
            # Dictionary containing the markdown-like patterns and their corresponding tags.
            patterns = {
                '**': 'b',
                '*': 'i',
                '~~': 's',
                '^^': 'sup',
                '^': 'sub',
                '__': 'u',
                '`': 'code',
                '[': 'a_open',
                ']': 'a_close'
            }

            chunks = []  # To store processed chunks of text.
            stack = []  # To keep track of opened and closed tags.
            buffer = ""  # Temporary buffer to hold characters until a pattern is matched.
            idx = 0  # Index to iterate through the text.

            # Iterate through the text to find patterns and process them.
            while idx < len(t):
                matched = False  # Flag to check if a pattern is matched.

                # Check each pattern to see if it matches the current position in the text.
                for pat, tag in patterns.items():
                    if t[idx:].startswith(pat):
                        # If buffer has content, append it to chunks.
                        if buffer:
                            closed_tags_count = len([m for m in stack if m not in patterns.values()])
                            chunks.append([0, stack.copy(), closed_tags_count, buffer])
                            buffer = ""

                        # Process hyperlink pattern.
                        if tag == 'a_open':
                            link_text_start = idx + len(pat)
                            link_text_end = t.find("]", link_text_start)
                            link_start = t.find("(", link_text_end) + 1
                            link_end = t.find(")", link_start)
                            link = t[link_start:link_end]

                            if ["a", ["href", link]] not in self.markups:
                                self.markups.append(["a", ["href", link]])
                            markup_idx = self.markups.index(["a", ["href", link]])
                            stack.append(markup_idx)
                            buffer += t[link_text_start:link_text_end]
                            idx = link_end + 1
                            closed_tags_count = len([m for m in stack if m not in patterns.values()])
                            chunks.append([0, stack.copy(), closed_tags_count, buffer])
                            buffer = ""
                            stack.pop()
                            continue
                        elif tag == 'a_close':
                            idx += len(pat)
                            continue
                        # Process other patterns.
                        elif tag in ['b', 'i', 's', 'sup', 'sub', 'u', 'code']:
                            if [tag] in self.markups:
                                markup_idx = self.markups.index([tag])
                            else:
                                self.markups.append([tag])
                                markup_idx = len(self.markups) - 1

                            if markup_idx in stack:
                                stack.remove(markup_idx)
                            else:
                                stack.append(markup_idx)

                        idx += len(pat)
                        matched = True
                        break

                # If no pattern is matched, add the character to buffer.
                if not matched:
                    buffer += t[idx]
                    idx += 1

            # If buffer has content at the end, append it to chunks.
            if buffer:
                closed_tags_count = len([m for m in stack if m not in patterns.values()])
                chunks.append([0, stack, closed_tags_count, buffer])

            self.sections.append([1, "p", chunks])

        # Process text based on its type (string or list).
        if isinstance(text, str):
            process_text(text)
        elif isinstance(text, list):
            for item in text:
                process_text(item)

    def add_divider(self):
        """ Method to add a divider to mobiledoc """
        self._add_card(["hr", {}])

    def add_image(self, url: str, caption: str = None):
        """ Method to add an image to mobiledoc """
        card = ["image", {"src": url}]
        if caption:
            card[1]["caption"] = caption

        self._add_card(card)

    def add_button(self, text: str, url: str, alignment: str = "center"):
        """ Method to add a button to mobiledoc """
        self._add_card(["button", {"text": text, "url": url, "alignment": alignment}])

    def add_html(self, html: str):
        """ Method to add HTML  cardto mobiledoc """
        self._add_card(["html", {"html": html}])

    def add_markdown(self, markdown: str):
        """ Method to add markdown card to mobiledoc """
        self._add_card(["markdown", {"markdown": markdown}])

    def add_file(self, url: str, filename: str, filetitle: str, filesize: int, filecaption: str = ""):
        """ Method to add a file to mobiledoc """
        self._add_card(["file", {"src": url, "fileName": filename, "fileTitle": filetitle, "fileCaption": filecaption,
                                 "fileSize": filesize}])

    def add_callout(self, text: str, emoji: str = "", color: str = "accent"):
        self._add_card(["callout", {"calloutEmoji": emoji, "calloutText": text, "backgroundColor": color}])

    def add_markdown_from_html(self, html_string: str):
        """ Method to add markdown from HTML """
        markdown = md(html_string)
        self.add_markdown(markdown)

    def custom_data(self, name: str, value):
        """ Method to add custom data to mobiledoc """
        self.custom[name] = value

    # Utility functions to inspect the current state of the mobiledoc
    def get_markups(self):
        """
        Display the current markups
        :return: list of markups
        """
        return self.markups

    def get_sections(self):
        """
        Display the current sections
        :return: list of sections
        """
        return self.sections

    def get_atoms(self):
        """
        Display the current atoms
        :return: lsit of atoms
        """
        return self.atoms

    def get_cards(self):
        """
        Display the current cards
        :return: list of cards
        """
        return self.cards

    def get_custom(self):
        """
        Display the current custom data
        :return:
        """
        return self.custom

    def serialize(self):
        """ Method to get the serialized mobiledoc """
        return_data = {
            "version": self.version,
            "markups": self.markups,
            "atoms": self.atoms,
            "cards": self.cards,
            "sections": self.sections,
        }
        for key, value in self.custom.items():
            return_data[key] = value
        return return_data


# Example usage:
if __name__ == "__main__":
    import json

    mobiledoc = Mobiledoc()
    mobiledoc.add_basic_text("This is a basic text, which is not formatted.")
    mobiledoc.add_basic_text(["You may also add a list of strings.", "To add multiple paragraphs."])
    mobiledoc.add_divider()  # add a divider
    mobiledoc.add_formatted_text("Using **markdown-like** syntax, you can *format* the text.")
    mobiledoc.add_formatted_text(["You may also add a `list of strings`.", "To ^add^ ^^multiple^^ paragraphs.",
                                  "You can also add [hyperlinks](https://python.org)."])
    mobiledoc.add_image("https://placehold.co/600x400/EEE/31343C", "You can add images!")
    mobiledoc.add_button("You can also buttons!", "https://python.org")
    mobiledoc.add_html("<ul><li>You can also add HTML</li><li>Like this</li></ul>")
    mobiledoc.add_markdown("You can add **raw markdown** cards! \n1. list item one\n2. list item two")
    mobiledoc.add_file("https://placehold.co/600x400/EEE/31343C", "filename", "filetitle", 1000)
    mobiledoc.add_callout("You can add callouts!", "🔥", "accent")
    mobiledoc.add_markdown_from_html('<b>Hello</b> <a href="http://github.com">GitHub</a>')

    mobiledoc = mobiledoc.serialize()  # This will save the mobiledoc as a dictionary

    with open('doc.json', 'w') as f:
        json.dump(mobiledoc, f, indent=4)  # check out the doc.json file to see the mobiledoc just created!
