from sys import exit
from typing import Optional

from PyQt5.QtWidgets import QApplication, QMainWindow
from gql import Client
from gql.transport.requests import RequestsHTTPTransport

from queries import AllExercisesResult, all_exercises_query, exercise_by_id_query, ExerciseByIdVariables, \
    ExerciseByIdExercise
from views.exercise_view import exercise_view
from views.home_view import home_view

client: Client = Client(
    transport=RequestsHTTPTransport(
        url='http://localhost:7000/graphql',
        use_json=True,
        headers={
            "Content-type": "application/json",
        },
        verify=False,
        retries=3,
    ),
    fetch_schema_from_transport=True
)


class CorAsUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('CorAs')
        self.setFixedSize(800, 600)

        self.show_home_view()

    def show_home_view(self) -> None:
        result: AllExercisesResult = all_exercises_query.execute(client, {})

        new_view = home_view(result['exercises'], lambda ex_id: self.show_exercise(ex_id))

        self.setCentralWidget(new_view)

    def show_exercise(self, exercise_id: int) -> None:
        variables: ExerciseByIdVariables = {'id': exercise_id}
        exercise: Optional[ExerciseByIdExercise] = exercise_by_id_query.execute(client, variables)['exercise']

        if exercise is None:
            return

        new_view = exercise_view(exercise)

        self.setCentralWidget(new_view)


app = QApplication([])
app.setStyle('Fusion')

view = CorAsUI()
view.show()

exit(app.exec())
