from dataclasses import dataclass
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
    children: list["SolutionEntry"]
