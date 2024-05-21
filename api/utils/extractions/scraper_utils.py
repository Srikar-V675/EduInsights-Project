from pydantic_schemas.mark import Mark, MarkCreate


# Conversion function
def convert_mark_create_to_orm(mark_create: MarkCreate) -> Mark:
    return Mark(
        stud_id=mark_create.stud_id,
        subject_id=mark_create.subject_id,
        section_id=mark_create.section_id,
        internal=mark_create.internal,
        external=mark_create.external,
        total=mark_create.total,
        result=mark_create.result,
        grade=mark_create.grade,
    )  # type: ignore
