from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget, QPushButton, QFileDialog

from queries import ExerciseByIdExercise


def open_file():
    filename, _ = QFileDialog.getOpenFileName(parent=None, caption='Open file', directory='.', filter='*.docx')

    if filename:
        print(filename)


def exercise_view(exercise: ExerciseByIdExercise) -> QWidget:
    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignCenter)

    title_label = QLabel()
    title_label.setText(exercise['title'])
    layout.addWidget(title_label)

    for textParagraph in exercise['textParagraphs']:
        text_label = QLabel()
        text_label.setText(textParagraph)
        text_label.setWordWrap(True)
        layout.addWidget(text_label)

    open_file_button = QPushButton()
    open_file_button.setText('Open file')
    open_file_button.clicked.connect(open_file)
    layout.addWidget(open_file_button)

    widget = QWidget()
    widget.setLayout(layout)
    return widget
