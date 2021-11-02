from dataclasses import dataclass, field
from typing import TypedDict, Optional, Literal

Applicability = Literal["NotSpecified", "NotApplicable", "Applicable"]


class AnalyzedSubText(TypedDict):
    text: str
    applicability: str


ParagraphType = Literal["German", "Bavarian"]


class ParagraphCitation(TypedDict):
    startIndex: int
    endIndex: int
    paragraphType: ParagraphType
    paragraph: int
    subParagraph: Optional[int]
    sentence: Optional[int]
    lawCode: Optional[str]


class FlatSolutionEntry(TypedDict):
    id: int
    text: str
    applicability: Applicability
    definition: Optional[str]
    # priorityPoints: Optional[int]
    # weight: Optional[int]
    # otherNumber: Optional[int]
    parentId: Optional[int]
    subTexts: list[AnalyzedSubText]
    paragraphCitations: list[ParagraphCitation]


@dataclass()
class SolutionEntry:
    id: int
    text: str
    applicability: Applicability
    definition: Optional[str] = None
    # priority_oints: Optional[int] = None
    # weight: Optional[int] = None
    # other_number: Optional[int] = None
    sub_texts: list[AnalyzedSubText] = field(default_factory=list)
    paragraph_citations: list[ParagraphCitation] = field(default_factory=list)
    children: list["SolutionEntry"] = field(default_factory=list)


# SolutionEntry -> FlatSolutionEntry


def flatten_entry(entry: SolutionEntry, parent_id: Optional[int] = None) -> list[FlatSolutionEntry]:
    first: FlatSolutionEntry = {
        "id": entry.id,
        "text": entry.text,
        "applicability": entry.applicability,
        "definition": entry.definition,
        "parentId": parent_id,
        "subTexts": entry.sub_texts,
        "paragraphCitations": entry.paragraph_citations,
    }

    return [first] + flatten_entries(entry.children, entry.id)


def flatten_entries(entries: list[SolutionEntry], parent_id: Optional[int] = None) -> list[FlatSolutionEntry]:
    flat_entries: list[FlatSolutionEntry] = []

    for entry in entries:
        flat_entries.extend(flatten_entry(entry, parent_id))

    return flat_entries
