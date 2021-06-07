from dataclasses import dataclass
from typing import TypedDict

from gql import gql, Client


class FlatSolutionEntry(TypedDict):
    __typename: str


class Exercise(TypedDict):
    id: int
    title: str
    textParagraphs: list[str]
    sampleSolution: list[FlatSolutionEntry]


@dataclass()
class SolutionEntry:
    id: int
    text: str
    children: list['SolutionEntry']


# GraphQL

class AllExercisesResult(TypedDict):
    exercises: list[Exercise]


query = gql(
    """\
    query AllExercises {
      exercises {
        id
        title
        textParagraphs
        sampleSolution {
            __typename
        }
      }
    }
    """
)


def query_all_exercises(client: Client) -> list[Exercise]:
    return client.execute(query)['exercises']
