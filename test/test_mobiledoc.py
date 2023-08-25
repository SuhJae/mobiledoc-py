from pathlib import Path
import unittest
import sys
import subprocess
import json


class TestMobiledocGeneratedFiles(unittest.TestCase):

    def setUp(self):
        self.testdata_python_dir = "testdata/python"
        self.testdata_json_dir = "testdata/Json"

    def execute_and_check_py_file(self, test_type, test_num):
        py_file_path = f"testdata/python/{test_type}/test_{test_type}_{test_num}.py"

        # Update sys.path to include the directory containing mobiledoc
        sys.path.append(str(Path(py_file_path).parent.parent.parent))  # Adjusting path to repository root

        result = subprocess.run([sys.executable, py_file_path], capture_output=True, text=True)

        # Remove the path adjustment (cleanup)
        sys.path.remove(str(Path(py_file_path).parent.parent.parent))

        self.assertEqual(result.returncode, 0, msg=f"Error executing: {py_file_path}\n{result.stderr}")

    def deserialize_and_check_json_file(self, test_type, idx):
        """Helper method to deserialize a given JSON file."""
        json_file_path = f"{self.testdata_json_dir}/{test_type}/test_{test_type}_{idx}.json"
        with open(json_file_path, 'r') as f:
            try:
                json_data = json.load(f)
                self.assertIsNotNone(json_data, msg=f"Error deserializing: {json_file_path}")
            except json.JSONDecodeError:
                self.fail(f"Error deserializing: {json_file_path}")

    def _test_generator(self, test_type):
        for i in range(1, 11):
            self.execute_and_check_py_file(test_type, i)
            self.deserialize_and_check_json_file(test_type, i)

    def test_basic_text(self):
        self._test_generator("basic_text")

    def test_formatted_text(self):
        self._test_generator("formatted_text")

    def test_divider(self):
        self._test_generator("divider")

    def test_image(self):
        self._test_generator("image")

    def test_button(self):
        self._test_generator("button")

    def test_html(self):
        self._test_generator("html")

    def test_markdown(self):
        self._test_generator("markdown")

    def test_file(self):
        self._test_generator("file")

    def test_callout(self):
        self._test_generator("callout")

    def test_mixed(self):
        self._test_generator("mixed")


if __name__ == "__main__":
    unittest.main()
