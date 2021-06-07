from typing import Callable

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QPushButton, QWidget, QLabel, QVBoxLayout

from model import Exercise


class HomeView(QWidget):
    __exercises_per_row: int = 3

    def __init__(self, exercises: list[Exercise], on_select: Callable[[int], None]):
        super().__init__()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title_label = QLabel()
        title_label.setText('<h1>Exercises</h1>')
        layout.addWidget(title_label)

        exercise_grid = QGridLayout()

        for index, exercise in enumerate(exercises):
            row = 0
            column = index % HomeView.__exercises_per_row

            button = QPushButton(exercise['title'])
            button.clicked.connect(lambda: on_select(exercise['id']))

            exercise_grid.addWidget(button, row, column)

        layout.addLayout(exercise_grid)

        self.setLayout(layout)
