from typing import TypedDict, Annotated
import operator


class PatientState(TypedDict):

    query: str

    rewritten_query: str

    retrieved_docs: list

    context: str

    routing: dict

    clinical: Annotated[list, operator.add]

    metabolic: Annotated[list, operator.add]

    lifestyle: Annotated[list, operator.add]

    combined: str

    final_report: str