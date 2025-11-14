#!/usr/bin/env python3
#
# SPDX-FileCopyrightText: 2025 German Aerospace Center (DLR)
# SPDX-License-Identifier: Apache-2.0
#
import os
import unittest

from markdown import markdown

from md_multiline_table import make_extension


def convert_and_compare(md_file: str, *extensions: str) -> None:
    solution_file = os.path.join(os.path.dirname(__file__), "resources", "solution.html")
    md_file = os.path.join(os.path.dirname(__file__), "resources", md_file)

    with open(md_file) as file:
        md = file.read()
    with open(solution_file) as file:
        solution = file.read()

    html = markdown(md, extensions=extensions)
    assert solution == html


class MdConverterTestCase(unittest.TestCase):
    def test_standard_markdown_table(self):
        # https://python-markdown.github.io/extensions/tables
        convert_and_compare("default_markdown.md", "tables")

    def test_standard_markdown_table_with_extension(self):
        convert_and_compare("default_markdown.md", make_extension())

    def test_colon_table(self):
        convert_and_compare("colon_example_1.md", make_extension())

    def test_colon_table_with_empty_lines(self):
        convert_and_compare("colon_example_2.md", make_extension())

    def test_colon_table_with_context_on_different_rows(self):
        convert_and_compare("colon_example_3.md", make_extension())

    def test_colon_table_with_escape_char(self):
        md = "|A|\n|-|\n||\n:\\:\\|:\n:\\:\\|:"
        solution = (
            "<table>\n<thead>\n<tr>\n<th>A</th>\n</tr>\n</thead>\n"
            "<tbody>\n<tr>\n<td>:| :|</td>\n</tr>\n</tbody>\n</table>"
        )
        html = markdown(md, extensions=[make_extension()])
        assert solution == html

    def test_plus_sign_table(self):
        convert_and_compare("plus_sign_example_1.md", make_extension())

    def test_plus_sign_table_with_empty_lines(self):
        convert_and_compare("plus_sign_example_2.md", make_extension())

    def test_plus_sign_table_with_context_on_different_rows(self):
        convert_and_compare("plus_sign_example_3.md", make_extension())

    def test_plus_sign_table_with_escape_char(self):
        md = "|A|\n|-|\n||\n|:\\||+\n|:\\||+"
        solution = (
            "<table>\n<thead>\n<tr>\n<th>A</th>\n</tr>\n</thead>\n"
            "<tbody>\n<tr>\n<td>:| :|</td>\n</tr>\n</tbody>\n</table>"
        )
        html = markdown(md, extensions=[make_extension()])
        assert solution == html


if __name__ == "__main__":
    unittest.main()
