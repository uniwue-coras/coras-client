from argparse import ArgumentParser
from configparser import ConfigParser
from sys import exit
from typing import Optional

from PyQt5.QtWidgets import QApplication, QMainWindow
from gql import Client as GraphQLClient
from gql.transport.requests import RequestsHTTPTransport
from urllib3 import disable_warnings as urllib3_disable_warnings

from login import mutate_login
from model.exercise import query_all_exercises, Exercise
from model.solution_entry import SolutionEntry
from views.exercise_view import ExerciseView
from views.home_view import HomeView
from views.solution_view import SolutionView

urllib3_disable_warnings()

config = ConfigParser()
config.read("./config.ini")

username: str = config["credentials"]["username"]
password: str = config["credentials"]["password"]

parser = ArgumentParser()
parser.add_argument("--url", default="https://coras.informatik.uni-wuerzburg.de")
args = parser.parse_args()

client: GraphQLClient = GraphQLClient(
    transport=RequestsHTTPTransport(
        url=f"{args.url}/graphql",
        use_json=True,
        headers={"Content-type": "application/json"},
        verify=False,
        retries=3,
    ),
    fetch_schema_from_transport=True,
)

client.transport.headers["Authorization"] = mutate_login(client, username, password)

exercises = query_all_exercises(client)


class CorAsUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CorAs")
        self.setMinimumSize(800, 600)

        self.show_home_view()

    def show_home_view(self):
        new_view = HomeView(exercises, lambda ex_id: self.show_exercise(ex_id))

        self.setCentralWidget(new_view)

    def show_exercise(self, exercise_id: int):
        exercise: Optional[Exercise] = next(ex for ex in exercises if ex["id"] == exercise_id)

        if exercise is None:
            return

        new_view = ExerciseView(exercise, lambda ex_id, solution: self.show_solution(ex_id, solution))

        self.setCentralWidget(new_view)

    def show_solution(self, exercise_id: int, solution: list[SolutionEntry]):
        exercise: Optional[Exercise] = next(ex for ex in exercises if ex["id"] == exercise_id)

        if exercise is None:
            return

        new_view = SolutionView(exercise, solution)

        self.setCentralWidget(new_view)


app = QApplication([])

view = CorAsUI()
view.show()

exit(app.exec())
