from gql import gql, Client as GraphQLClient

query = gql(
    """\
mutation Login($username: String!, $password: String!) {
    login(loginInput: {username: $username, password: $password}) {
        jwt
    }
}"""
)


def mutate_login(client: GraphQLClient, username: str, password: str) -> str:
    return client.execute(query, {"username": username, "password": password})["login"]["jwt"]
