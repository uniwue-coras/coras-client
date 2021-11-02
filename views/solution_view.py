from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTreeWidget, QTreeWidgetItem

from model.exercise import Exercise
from model.solution_entry import SolutionEntry


def __build_tree_item__(solution_entry: SolutionEntry) -> QTreeWidgetItem:
    item = QTreeWidgetItem([solution_entry.text])

    for child in solution_entry.children:
        child_item = __build_tree_item__(child)
        item.addChild(child_item)

    return item


class SolutionView(QWidget):
    def __init__(self, exercise: Exercise, solution: list[SolutionEntry]):
        super().__init__()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title_label = QLabel()
        title_label.setText(f'<h1>{exercise["title"]}</h1>')
        layout.addWidget(title_label)

        tree = QTreeWidget()
        tree.setColumnCount(1)
        tree.setWordWrap(True)

        for solution_entry in solution:
            tree.addTopLevelItem(__build_tree_item__(solution_entry))

        tree.expandAll()

        layout.addWidget(tree)

        self.setLayout(layout)
