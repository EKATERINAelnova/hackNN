from pydantic import BaseModel


class Student(BaseModel):
    id_student: int
    name: str
    ids_discipline_teacher: list[int]

class Discipline(BaseModel):
    id_discipline: int
    name: str
    description: str

class Teacher(BaseModel):
    id_teacher: int
    name: str


# Response /get_all_student
class GetAllStudentResponse(BaseModel):
    students: list[Student]


# Request /get_teachers_and_disciplines_by_id_student
class GetTeachersAndDisciplinesRequest(BaseModel):
    id_student: int

# Response /get_teachers_and_disciplines_by_id_student
class GetTeachersAndDisciplinesResponse(BaseModel):
    disciplines: list[Discipline]
    teachers: list[Teacher]


# Request /add_teacher_rating
class AddTeacherRatingRequest(BaseModel):
    id_student: int
    rating: list[int]


# Request /add_discipline_rating
class AddDisciplineRatingRequest(BaseModel):
    id_student: int
    rating: list[int]


# Response /get_feedback
class GetFeedbackResponse(BaseModel):
    id_student: int
    name: str
    summary: str
    keywords: list[str]


# Response status
class StatusResponse(BaseModel):
    status: bool