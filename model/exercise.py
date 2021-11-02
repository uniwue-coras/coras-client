from typing import TypedDict

from gql import gql, Client

from model.solution_entry import FlatSolutionEntry


class Exercise(TypedDict):
    id: int
    title: str
    text: str
    sampleSolution: list[FlatSolutionEntry]


# GraphQL


class AllExercisesResult(TypedDict):
    exercises: list[Exercise]


query = gql(
    """\
query AllExercises {
  exercises {
    id
    title
    text
    sampleSolution {
        __typename
    }
  }
}"""
)


def query_all_exercises(client: Client) -> list[Exercise]:
    return client.execute(query)["exercises"]
