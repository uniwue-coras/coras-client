from typing import Callable

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget, QPushButton, QFileDialog

from model.exercise import Exercise
from model.solution_entry import SolutionEntry
from word_parser import open_word_file


class ExerciseView(QWidget):
    def __init__(self, exercise: Exercise, show_solution: Callable[[int, list[SolutionEntry]], None]):
        super().__init__()

        self.show_solution = show_solution

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title_label = QLabel()
        title_label.setText(f'<h1>{exercise["title"]}</h1>')
        layout.addWidget(title_label)

        for textParagraph in exercise["text"].split("\n"):
            text_label = QLabel()
            text_label.setText(textParagraph)
            text_label.setWordWrap(True)
            layout.addWidget(text_label)

        open_file_button = QPushButton()
        open_file_button.setText("Open file")
        open_file_button.clicked.connect(lambda: self.__open_file__(exercise["id"]))
        layout.addWidget(open_file_button)

        self.setLayout(layout)

    def __open_file__(self, exercise_id: int):
        filename, _ = QFileDialog.getOpenFileName(parent=None, caption="Open file", directory=".", filter="*.docx")

        if filename is None or len(filename) == 0:
            return

        parsed_lines = open_word_file(filename)

        self.show_solution(exercise_id, parsed_lines)
