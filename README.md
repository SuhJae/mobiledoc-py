# **Mobiledoc**

A Python package aimed to simplify the processing of the mobiledoc format.

## **Features**

- **Simple API**: Intuitive methods to easily add text, formatted text, dividers, and custom data.
- **Markdown-like Formatting**: Write using familiar markdown-like syntax, and let the package do the heavy lifting.
- **Serialization**: Serialize the mobiledoc object into a JSON-friendly format.

## **Installation**

coming soon to pypi

## **Example**

```python
from mobiledoc import Mobiledoc
import json

mobiledoc = Mobiledoc()
mobiledoc.add_basic_text("This is a basic text, which is not formatted.")
mobiledoc.add_basic_text(["You may also add a list of strings.", "To add multiple paragraphs."])
mobiledoc.add_divider()  # add a divider
mobiledoc.add_formatted_text("Using **markdown-like** syntax, you can *format* the text.")
mobiledoc.add_formatted_text(["You may also add a `list of strings`.", "To ^add^ ^^multiple^^ paragraphs.",
                              "You can also add [hyperlinks](https://python.org)."])

mobiledoc = mobiledoc.serialize()  # This will save the mobiledoc as a dictionary

with open('doc.json', 'w') as f:
    json.dump(mobiledoc, f, indent=4)  # check out the doc.json file to see the mobiledoc just created!

```
This will create redy-to-use mobiledoc like below. (click expand to see the mobiledoc)
<details>
<summary>Full mobiledoc</summary>
<pre><code>
{
    "version": "0.3.2",
    "markups": [
        ["b"],
        ["i"],
        ["code"],
        ["sub"],
        ["sup"],
        ["a", ["href", "https://python.org"]]
    ],
    "atoms": [],
    "cards": [
        ["hr", {}]
    ],
    "sections": [
        [1, "p", [
            [0, [], 0, "This is a basic text, which is not formatted."]
        ]],
        [1, "p", [
            [0, [], 0, "You may also add a list of strings."]
        ]],
        [1, "p", [
            [0, [], 0, "To add multiple paragraphs."]
        ]],
        [10, 0],
        [1, "p", [
            [0, [], 0, "Using "],
            [0, [0], 1, "markdown-like"],
            [0, [], 0, " syntax, you can "],
            [0, [1], 1, "format"],
            [0, [], 0, " the text."]
        ]],
        [1, "p", [
            [0, [], 0, "You may also add a "],
            [0, [2], 1, "list of strings"],
            [0, [], 0, "."]
        ]],
        [1, "p", [
            [0, [], 0, "To "],
            [0, [3], 1, "add"],
            [0, [], 0, " "],
            [0, [4], 1, "multiple"],
            [0, [], 0, " paragraphs."]
        ]],
        [1, "p", [
            [0, [], 0, "You can also add "],
            [0, [5], 1, "hyperlinks"],
            [0, [], 0, "."]
        ]]
    ]
}
</code></pre>

</details>

## **API**

### **Mobiledoc Methods**

- **`add_basic_text(text: Union[str, List[str]])`**: Adds basic text to mobiledoc.
- **`add_formatted_text(text: Union[str, List[str]])`**: Adds markdown-like formatted text to mobiledoc.
  - **Supported Markdown-like Patterns:**
    ```
    **: bold
    *: italic
    ~~: strikethrough
    ^^: superscript
    ^: subscript
    __: underline
    `: code
    [text](link): hyperlink
    ```
- **`custom_data(name: str, value)`**: Adds custom data to mobiledoc.
- **`get_markups()`**: Returns the current markups.
- **`get_sections()`**: Returns the current sections.
- **`get_atoms()`**: Returns the current atoms.
- **`get_cards()`**: Returns the current cards.
- **`get_custom()`**: Returns the current custom data.
- **`serialize()`**: Returns the serialized mobiledoc.

## **Contributing**

Contributions are welcome! Please submit a pull request or open an issue on GitHub.

---

I hope this README provides a clear overview of the **`mobiledoc`** package. You can further customize it as per your needs!
