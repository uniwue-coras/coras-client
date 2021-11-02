from dataclasses import dataclass, field
from pathlib import Path
from re import Pattern, compile as compile_regex
from typing import Optional, Union
from unittest import TestCase, main as unittest_main

from docx import Document as open_document
from docx.document import Document
from docx.text.paragraph import Paragraph

from model.solution_entry import SolutionEntry

heading_regex: Pattern[str] = compile_regex(r"Heading (\d)")


@dataclass()
class ParsedLine:
    id: int
    level: int
    heading_text: str
    explanation_texts: list[str] = field(default_factory=list)


def __split_parsed_lines__(parsed_lines: list[ParsedLine]) -> list[list[ParsedLine]]:
    minimal_level = min(pl.level for pl in parsed_lines)

    result: list[list[ParsedLine]] = []

    for parsed_line in parsed_lines:
        if parsed_line.level == minimal_level:
            result.append([])

        result[-1].append(parsed_line)

    return result


def __handle_parsed_lines__(parsed_lines: list[ParsedLine]) -> list[SolutionEntry]:
    return [__split_lines_to_solution_entry__(line) for line in __split_parsed_lines__(parsed_lines)]


def __split_lines_to_solution_entry__(lines: list[ParsedLine]) -> SolutionEntry:
    first = lines[0]
    rest = lines[1:]

    children = __handle_parsed_lines__(rest) if len(rest) > 0 else []

    return SolutionEntry(id=first.id, text=first.heading_text, children=children)


def __read_paragraph__(paragraph: Paragraph) -> tuple[Optional[int], str]:
    style_match = heading_regex.match(paragraph.style.name)

    level = int(style_match.group(1)) if style_match is not None else None

    return level, paragraph.text


def open_word_file(filename: Union[str, Path]) -> list[SolutionEntry]:
    document: Document = open_document(filename)

    index = 1
    parsed_lines: list[ParsedLine] = []
    current_parsed_line: Optional[ParsedLine] = None
    for paragraph in document.paragraphs:

        level, text = __read_paragraph__(paragraph)

        if level is not None:
            parsed_line = ParsedLine(index, level, text)
            current_parsed_line = parsed_line
            parsed_lines.append(parsed_line)
        elif current_parsed_line is not None:
            # explanation text found
            current_parsed_line.explanation_texts.append(text)
        else:
            # leading line (author, case, ...)
            pass

    return __handle_parsed_lines__(parsed_lines)


class __OpenWordFileTest(TestCase):
    def test_open_word_file(self):
        parsed = open_word_file(Path.cwd() / "data" / "Marvin_Musterman_Musterloesung_1438940966403.docx")

        self.assertIsNotNone(parsed)

        for line in parsed:
            print(line)


if __name__ == "__main__":
    unittest_main()
