from functools import partial
from typing import Callable

from PyQt5.QtWidgets import QGridLayout, QPushButton, QWidget

from queries import AllExercisesResultExercise

__exercises_per_row: int = 3


def home_view(exercises: list[AllExercisesResultExercise], on_select: Callable[[int], None]) -> QWidget:
    layout = QGridLayout()

    for index, exercise in enumerate(exercises):
        row = 0
        column = index % __exercises_per_row

        button = QPushButton(exercise['title'])
        button.clicked.connect(partial(on_select, exercise['id']))

        layout.addWidget(button, row, column)

    widget = QWidget()
    widget.setLayout(layout)
    return widget
