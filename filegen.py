import os
import json
from faker import Faker
import mobiledoc as md

fake = Faker()

# Creating required directories if not exist
os.makedirs("testdata/python/basic_text", exist_ok=True)
os.makedirs("testdata/python/formatted_text", exist_ok=True)
os.makedirs("testdata/python/divider", exist_ok=True)
os.makedirs("testdata/python/image", exist_ok=True)
os.makedirs("testdata/python/button", exist_ok=True)
os.makedirs("testdata/python/html", exist_ok=True)
os.makedirs("testdata/python/markdown", exist_ok=True)
os.makedirs("testdata/python/file", exist_ok=True)
os.makedirs("testdata/python/callout", exist_ok=True)
os.makedirs("testdata/python/mixed", exist_ok=True)

os.makedirs("testdata/Json/basic_text", exist_ok=True)
os.makedirs("testdata/Json/formatted_text", exist_ok=True)
os.makedirs("testdata/Json/divider", exist_ok=True)
os.makedirs("testdata/Json/image", exist_ok=True)
os.makedirs("testdata/Json/button", exist_ok=True)
os.makedirs("testdata/Json/html", exist_ok=True)
os.makedirs("testdata/Json/markdown", exist_ok=True)
os.makedirs("testdata/Json/file", exist_ok=True)
os.makedirs("testdata/Json/callout", exist_ok=True)
os.makedirs("testdata/Json/mixed", exist_ok=True)

def generate_files(mobile_doc, test_type, idx):
    py_file_path = f"testdata/python/{test_type}/test_{test_type}_{idx}.py"
    json_path = f"testdata/Json/{test_type}/test_{test_type}_{idx}.json"

    with open(py_file_path, "w") as py_file:
        py_file.write(f"# Auto-generated Python test for {test_type}\n")
        py_file.write("import json\n")
        py_file.write("import mobiledoc as md\n")
        py_file.write(f"with open('{json_path}', 'r') as f:\n")
        py_file.write("    data = json.load(f)\n")
        py_file.write("print(data)\n")

    with open(json_path, "w") as json_file:
        json.dump(mobile_doc.serialize(), json_file, indent=4)

# Methods to generate different tests based on the provided Mobiledoc class methods
def generate_basic_text_case(md_instance, idx):
    md_instance.add_basic_text(fake.text())
    generate_files(md_instance, "basic_text", idx)

def generate_formatted_text_case(md_instance, idx):
    md_instance.add_formatted_text(f"**{fake.word()}** *{fake.word()}* ~~{fake.word()}~~ ^^{fake.word()}^^ ^{fake.word()}^ __{fake.word()}__ `{fake.word()}`")
    generate_files(md_instance, "formatted_text", idx)

def generate_divider_case(md_instance, idx):
    md_instance.add_divider()
    generate_files(md_instance, "divider", idx)

def generate_image_case(md_instance, idx):
    md_instance.add_image(fake.image_url(), fake.sentence())
    generate_files(md_instance, "image", idx)

def generate_button_case(md_instance, idx):
    md_instance.add_button(fake.word(), fake.url())
    generate_files(md_instance, "button", idx)

def generate_html_case(md_instance, idx):
    md_instance.add_HTML("<div>Hello World</div>")
    generate_files(md_instance, "html", idx)

def generate_markdown_case(md_instance, idx):
    md_instance.add_markdown("# " + fake.sentence())
    generate_files(md_instance, "markdown", idx)

def generate_file_case(md_instance, idx):
    md_instance.add_file(fake.file_name(), fake.file_name(), fake.file_name(), fake.random_int())
    generate_files(md_instance, "file", idx)

def generate_callout_case(md_instance, idx):
    md_instance.add_callout(fake.sentence(), fake.emoji())
    generate_files(md_instance, "callout", idx)

def generate_mixed_case(md_instance, idx):
    md_instance.add_basic_text(fake.text())
    md_instance.add_image(fake.image_url(), fake.sentence())
    md_instance.add_button(fake.word(), fake.url())
    md_instance.add_divider()
    md_instance.add_HTML("<div>Mixed Case</div>")
    generate_files(md_instance, "mixed", idx)

def main():
    for i in range(1, 11):
        md_instance = md.Mobiledoc()
        generate_basic_text_case(md_instance, i)

        md_instance = md.Mobiledoc()
        generate_formatted_text_case(md_instance, i)

        md_instance = md.Mobiledoc()
        generate_divider_case(md_instance, i)

        md_instance = md.Mobiledoc()
        generate_image_case(md_instance, i)

        md_instance = md.Mobiledoc()
        generate_button_case(md_instance, i)

        md_instance = md.Mobiledoc()
        generate_html_case(md_instance, i)

        md_instance = md.Mobiledoc()
        generate_markdown_case(md_instance, i)

        md_instance = md.Mobiledoc()
        generate_file_case(md_instance, i)

        md_instance = md.Mobiledoc()
        generate_callout_case(md_instance, i)

        md_instance = md.Mobiledoc()
        generate_mixed_case(md_instance, i)

if __name__ == "__main__":
    main()
