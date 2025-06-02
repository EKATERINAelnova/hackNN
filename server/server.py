# internal/
#
#
# http/server/router.py
import uvicorn
from fastapi import APIRouter
from internal.http.server.contract import (
    GetAllStudentResponse,
    GetTeachersAndDisciplinesRequest, GetTeachersAndDisciplinesResponse,
    AddTeacherRatingRequest,
    AddDisciplineRatingRequest,
    StatusResponse
)
from internal.http.storage.storage import Storage
db = Storage()

# internal/app/app.py
from fastapi import FastAPI
app = FastAPI(
    title="Student Rating API",
    description="API для управления рейтингами студентов",
    version="1.0.0"
)

router = APIRouter(prefix="/api/v1", tags=["students"])
app.include_router(router)

@router.get("/get_all_student/", response_model=GetAllStudentResponse)
async def get_all_students():
    student = db.get_all_students()
    print(student)
    return GetAllStudentResponse

@router.post("/get_teachers_and_disciplines_by_id_student",
           response_model=GetTeachersAndDisciplinesResponse)
async def get_teachers_and_disciplines_by_id_student(data: GetTeachersAndDisciplinesRequest):
    """
    Получить всех преподавателей и дисциплин для студента
    """
    return GetTeachersAndDisciplinesResponse

@router.post("/add_teacher_rating", response_model=StatusResponse)
async def add_teacher_rating(data: AddTeacherRatingRequest):
    """
    Добавить рейтинг преподавателей от студента
    Рейтинг передаётся как список id_teacher от худшего к лучшему
    """
    # Валидация что студент существует
    # Сохранение рейтинга
    return StatusResponse

@router.post("/add_discipline_rating", response_model=StatusResponse)
async def add_discipline_rating(data: AddDisciplineRatingRequest):
    """
    Добавить рейтинг дисциплин от студента
    Рейтинг передаётся как список id_discipline от худшего к лучшему
    """
    # Валидация что студент существует
    # Сохранение рейтинга
    return StatusResponse

uvicorn.run("server:app", host="0.0.0.0", port=8080, reload=True)