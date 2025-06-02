from collections import defaultdict

from fastapi import APIRouter

from internal.http.server.contract import (
    Student, Teacher, Discipline
)
from internal.http.server.contract import (
    GetAllStudentResponse,
    GetTeachersAndDisciplinesRequest, GetTeachersAndDisciplinesResponse,
    AddTeacherRatingRequest,
    AddDisciplineRatingRequest,
    GetStatisticRequest, GetStatisticResponse,
    StatusResponse
)

from internal.storage.storage import Storage
from datetime import datetime, timedelta

router = APIRouter()
db = Storage()

@router.get("/get_all_student", response_model=GetAllStudentResponse)
async def get_all_students():
    db.drop_table()
    db.init_table()
    await db.mock_data()

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
    return StatusResponse(status=True)s

@router.post("/get_statistic", response_model=GetStatisticResponse) # GetStatisticResponse
async def add_discipline_rating(data: GetStatisticRequest):
    def rating(data: list[list[int]]) -> dict:
        # Храним суммы рейтингов и количество появлений
        _scores = defaultdict(float)
        _counts = defaultdict(int)

        for arr in data:
            n = len(arr)
            for position, _id in enumerate(arr):
                rating = 1 - position / n
                _scores[_id] += rating
                _counts[_id] += 1

        # Считаем средний рейтинг
        average_ratings = {
            _id: _scores[_id] / _counts[_id]
            for _id in _scores
        }
        return average_ratings

    await db.connect()
    data_teacher_rating = list()
    teacher = await db.get_last_rating_on_diapason(start_date=data.date_start, end_date=data.date_end, _type="teacher")
    for row in teacher:
        data_teacher_rating.append(row["rating"])

    data_discipline_rating = list()
    discipline = await db.get_last_rating_on_diapason(start_date=data.date_start, end_date=data.date_end, _type="discipline")
    for row in discipline:
        data_discipline_rating.append(row["rating"])
    await db.disconnect()

    return StatusResponse(status=True)