# SPDX-FileCopyrightText: 2025 German Aerospace Center (DLR)
# SPDX-License-Identifier: Apache-2.0
#
"""Multiline Table extension for Python Markdown."""

from logging import getLogger
import re
from typing import Any
import xml.etree.ElementTree as etree

from markdown import Markdown
from markdown.blockparser import BlockParser
from markdown.extensions.tables import PIPE_LEFT, PIPE_NONE, PIPE_RIGHT, TableExtension, TableProcessor


class MultilineTableProcessor(TableProcessor):
    """Multiline Table Python Markdown extension markdown code block processor."""

    RE_END_BORDER = re.compile(r"(?<!\\)(?:\\\\)*(\|\+?|:)$")

    def __init__(self, parser: BlockParser, config: dict[str, Any]) -> None:
        """
        Initialize new instance of the multiline table python extension markdown block processor.

        Args:
            parser (BlockParser): block parser
            config (dict[str, Any]): all configuration options
        """
        super().__init__(parser, config)
        self._logger = getLogger("MARKDOWN")

    def test(self, parent: etree.Element, block: str) -> bool:
        """
        Ensure that the first few rows contains a valid table head (column header and separator row).

        This method does exactly the same like its super() version except that the separator row
        does not have to be in the second row to support multiline headers.
        See variable `format_row`.

        Args:
            parent (etree.Element): parent html element
            block (str): markdown code

        Returns:
            bool: whether markdown code is a table or not
        """
        is_table = False
        rows = [row.strip(" ") for row in block.split("\n")]
        if len(rows) > 1:
            header0 = rows[0]
            self.border = PIPE_NONE  # type: ignore[assignment]
            if header0.startswith("|"):
                self.border |= PIPE_LEFT  # type: ignore[assignment]
            if self.RE_END_BORDER.search(header0) is not None:
                self.border |= PIPE_RIGHT  # type: ignore[assignment]
            row = self._split_row(header0)  # type: ignore[attr-defined]
            row0_len = len(row)
            is_table = row0_len > 1

            # Each row in a single column table needs at least one pipe.
            if not is_table and row0_len == 1 and self.border:
                for index in range(1, len(rows)):
                    is_table = rows[index].startswith("|")
                    if not is_table:
                        is_table = self.RE_END_BORDER.search(rows[index]) is not None
                    if not is_table:
                        break

            if is_table:
                format_row = next((row for idx, row in enumerate(rows) if idx > 0 and row.endswith("|")))
                row = self._split_row(format_row)  # type: ignore[attr-defined]
                is_table = (len(row) == row0_len) and set("".join(row)) <= set("|:- ")
                if is_table:
                    self.separator = row

        return is_table

    def run(self, parent: etree.Element, blocks: list[str]) -> bool | None:
        """
        Transform multiline table to standard markdown table.

        Args:
            parent (etree.Element): parent html element
            blocks (list[str]): markdown code blocks

        Returns:
            bool | None: success state
        """
        lines = blocks.pop(0).split("\n")

        # sanity check which should never fail due to self.test(...)
        if len(lines) < 2:
            self._logger.warning("Broken table with less then 2 lines detected.")
            return False
        column_count = len(re.split(r"(?<!\\)(?:\\\\)*\|", lines[0])) - 2
        if column_count < 1:
            self._logger.warning("Broken table with less then 1 column detected.")
            return False

        # convert multiline table to default markdown table format
        blocks.insert(0, self._convert_table(lines, column_count))
        return super().run(parent, blocks)

    def _convert_table(self, lines: list[str], column_count: int) -> str:
        line_idx = 1
        while line_idx < len(lines):
            line = lines[line_idx]
            if line.strip()[0] != ":" and not line.strip().endswith("|+"):
                line_idx += 1
                continue

            re_split_pattern = r"(?<!\\)(?:\\\\)*:" if not line.strip().endswith("|+") else r"(?<!\\)(?:\\\\)*\|"
            columns = re.split(re_split_pattern, line)[1:-1]
            if len(columns) != column_count:
                self._logger.warning(
                    "Table column count mismatch. "
                    f"Row has {len(columns)} instead of the expected {column_count} columns."
                )

            columns_previous = re.split(r"(?<!\\)(?:\\\\)*\|", lines[line_idx - 1])[1:-1]
            lines[line_idx - 1] = (
                "| "
                + " | ".join(
                    map(
                        lambda column_parts: " ".join(map(lambda part: part.strip(), column_parts)).strip(),
                        zip(columns_previous, columns, strict=False),
                    )
                )
                + " |"
            )
            lines.pop(line_idx)

        return "\n".join(lines)


class MultilineTableExtension(TableExtension):
    """Multiline Table Python Markdown extension."""

    def extendMarkdown(self, md: Markdown) -> None:
        """
        Extend markdown instance with multiline table extension.

        Args:
            md (Markdown): markdown instance to extend
        """
        if "|" not in md.ESCAPED_CHARS:
            md.ESCAPED_CHARS.append("|")
        if ":" not in md.ESCAPED_CHARS:
            md.ESCAPED_CHARS.append(":")
        processor = MultilineTableProcessor(md.parser, self.getConfigs())
        md.parser.blockprocessors.register(processor, "md-multiline-table", 106)


def make_extension(*args, **kwargs) -> MultilineTableExtension:
    """
    Make a new instance of `MultilineTableExtension`.

    Returns:
        MultilineTableExtension: new instance of MultilineTableExtension
    """
    return MultilineTableExtension(*args, **kwargs)
