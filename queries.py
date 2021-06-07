from typing import TypedDict, Optional, TypeVar, Generic

from gql import gql, Client
from graphql import DocumentNode

T = TypeVar('T')
V = TypeVar('V')


class Query(Generic[T, V]):
    query: DocumentNode

    def __init__(self, query: str):
        self.query = gql(query)

    def execute(self, client: Client, args: V) -> T:
        return client.execute(self.query, args)


class AllExercisesResultExercise(TypedDict):
    id: int
    title: str


class AllExercisesResult(TypedDict):
    exercises: list[AllExercisesResultExercise]


class AllExercisesVariables(TypedDict):
    pass


all_exercises_query = Query[AllExercisesResult, AllExercisesVariables](
    """\
    query AllExercises {
      exercises {
        id
        title
      }
    }
    """
)


class ExerciseByIdExercise(TypedDict):
    id: int
    title: str
    textParagraphs: list[str]


class ExerciseByIdResult(TypedDict):
    exercise: Optional[ExerciseByIdExercise]


class ExerciseByIdVariables(TypedDict):
    id: int


exercise_by_id_query = Query[ExerciseByIdResult, ExerciseByIdVariables](
    """\
    query ExerciseById($id: Int!) {
        exercise(id: $id) {
            id
            title
            textParagraphs
        }
    }
    """
)
