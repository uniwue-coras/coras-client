from model.solution_entry import BasicSolutionEntry, flatten_entries

solution_example: list[BasicSolutionEntry] = [
    BasicSolutionEntry(
        id=1,
        text='Sachurteilsvoraussetzungen',
        applicability='Applicable',
        children=[
            BasicSolutionEntry(
                id=2,
                text='Eröffnung des Verwaltungsrechtswegs, § 40 I 1 VwGO',
                applicability='Applicable',
                children=[
                    BasicSolutionEntry(
                        id=3,
                        text='aufdrängende Sonderzuweisung',
                        applicability='NotApplicable'
                    ),
                    BasicSolutionEntry(
                        id=4,
                        text='Generalklausel, § 40 I 1',
                        applicability='Applicable'
                    )
                ]
            ),
        ]
    )
]

if __name__ == "__main__":
    print(flatten_entries(solution_example))
