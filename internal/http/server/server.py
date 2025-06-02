# internal/
#
#
# http/server/router.py
from datetime import datetime

import uvicorn
from fastapi import APIRouter
from internal.http.server.contract import (
    Student, Teacher, Discipline
)
from internal.http.server.contract import (
    GetAllStudentResponse,
    GetTeachersAndDisciplinesRequest, GetTeachersAndDisciplinesResponse,
    AddTeacherRatingRequest,
    AddDisciplineRatingRequest,
    StatusResponse
)
from internal.http.storage.storage import Storage

db = Storage()
db.init_table()

# internal/app/app.py
from fastapi import FastAPI
app = FastAPI(
    title="Student Rating API",
    description="API для управления рейтингами студентов",
    version="1.0.0"
)

router = APIRouter()

@router.get("/get_all_student/", response_model=GetAllStudentResponse)
async def get_all_students():
    await db.connect()
    students = await db.get_all_students()
    await db.disconnect()

    response = list()
    for student in students:
        response.append(Student(
            id_student=student["id_student"],
            name=student["name"],
            ids_discipline_teacher=student["ids_discipline_teacher"],
        ))
    return GetAllStudentResponse(students=response)

@router.post("/get_teachers_and_disciplines_by_id_student",
           response_model=GetTeachersAndDisciplinesResponse)
async def get_teachers_and_disciplines_by_id_student(data: GetTeachersAndDisciplinesRequest):
    await db.connect()
    teachers = await db.get_all_teacher_by_id_student(id_student=data.id_student)
    disciplines = await db.get_all_discipline_by_id_student(id_student=data.id_student)
    await db.disconnect()
    return GetTeachersAndDisciplinesResponse(
        teachers=teachers["teachers"],
        disciplines=disciplines["disciplines"]
    )

@router.post("/add_teacher_rating", response_model=StatusResponse)
async def add_teacher_rating(data: AddTeacherRatingRequest):
    await db.connect()
    await db.add_rating(date=datetime.now(), id_student=data.id_student, rating_list=data.rating, type_="teacher")
    await db.disconnect()
    return StatusResponse(status=True)

@router.post("/add_discipline_rating", response_model=StatusResponse)
async def add_discipline_rating(data: AddDisciplineRatingRequest):
    await db.connect()
    await db.add_rating(date=datetime.now(), id_student=data.id_student, rating_list=data.rating, type_="discipline")
    await db.disconnect()
    return StatusResponse(status=True)

app.include_router(router)