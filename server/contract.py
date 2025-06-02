# internal/domain/models/student.py
from pydantic import BaseModel
from typing import List, Optional


class Student(BaseModel):
    id_student: int
    name: str
    ids_discipline_teacher: List[int]

class Discipline(BaseModel):
    id_discipline: int
    name: str
    description: str

class Teacher(BaseModel):
    id_teacher: int
    name: str


# Response /get_all_student
class GetAllStudentResponse(BaseModel):
    student: List[Student]


# Request /get_teachers_and_disciplines_by_id_student
class GetTeachersAndDisciplinesRequest(BaseModel):
    id_student: int

# Response /get_teachers_and_disciplines_by_id_student
class GetTeachersAndDisciplinesResponse(BaseModel):
    disciplines: List[Discipline]
    teachers: List[Teacher]


# Request /add_teacher_rating
class AddTeacherRatingRequest(BaseModel):
    id_student: int
    rating: List[int]


# Request /add_discipline_rating
class AddDisciplineRatingRequest(BaseModel):
    id_student: int
    rating: List[int]


# Response status
class StatusResponse(BaseModel):
    status: bool