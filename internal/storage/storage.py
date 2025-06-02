from datetime import datetime, timedelta

from databases import Database
from sqlalchemy import select, func, and_
from sqlalchemy import create_engine
from internal.storage.metadata import metadata, student, teacher, feedback, rating, discipline_teacher, discipline
from typing import Optional

# Класс-обёртка (Singleton)
class Storage:
    _instance: Optional["Storage"] = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Storage, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._db_path = "postgresql://hack:hackathon@localhost:5432/hack_db"
        self._db = Database(self._db_path)


    async def connect(self):
        if not self._db.is_connected:
            await self._db.connect()

    async def disconnect(self):
        if self._db.is_connected:
            await self._db.disconnect()

    def init_table(self):
        engine = create_engine(self._db_path)
        metadata.create_all(engine)

    def drop_table(self):
        engine = create_engine(self._db_path)
        metadata.drop_all(engine)


    async def get_all_students(self):
        query = student.select()
        return await self._db.fetch_all(query)

    async def get_teacher_by_id(self, id_teacher: int):
        query = teacher.select().where(teacher.c.id_teacher == id_teacher)
        return await self._db.fetch_one(query)

    async def get_discipline_by_id(self, id_discipline: int):
        query = discipline.select().where(discipline.c.id_discipline == id_discipline)
        return await self._db.fetch_one(query)

    async def get_discipline_teacher_by_id(self, id_discipline_teacher: int):
        query = discipline_teacher.select().where(discipline_teacher.c.id_discipline_teacher == id_discipline_teacher)
        return await self._db.fetch_one(query)

    async def get_all_teacher_by_id_student(self, id_student: int):
        query = student.select().where(student.c.id_student == id_student)
        data_student = await self._db.fetch_one(query)

        data_teachers = list()
        for ids_discipline_teacher in data_student["ids_discipline_teacher"]:
            data_discipline_teacher = await self.get_discipline_teacher_by_id(ids_discipline_teacher)
            data_teacher = await self.get_teacher_by_id(data_discipline_teacher["id_teacher"])
            data_teachers.append({
                'id_teacher': data_teacher["id_teacher"],
                'name': data_teacher["name"]
            })

        # Используем словарь для уникальных записей
        union_data_teachers = {item['id_teacher']: item for item in data_teachers}.values()
        # Преобразуем обратно в список
        union_data_teachers = list(union_data_teachers)
        return {'teachers': union_data_teachers}

    async def get_all_discipline_by_id_student(self, id_student: int):
        query = student.select().where(student.c.id_student == id_student)
        data_student = await self._db.fetch_one(query)

        data_disciplines = list()
        for ids_discipline_teacher in data_student["ids_discipline_teacher"]:
            data_discipline_teacher = await self.get_discipline_teacher_by_id(ids_discipline_teacher)
            data_discipline = await self.get_discipline_by_id(data_discipline_teacher["id_discipline"])
            data_disciplines.append({
                'id_discipline': data_discipline["id_discipline"],
                'name': data_discipline["name"],
                'description': data_discipline["description"]
            })

        # Используем словарь для уникальных записей
        union_data_disciplines = {item['id_discipline']: item for item in data_disciplines}.values()
        # Преобразуем обратно в список
        union_data_disciplines = list(union_data_disciplines)
        return {'disciplines': union_data_disciplines}

    async def add_rating(self, date, id_student: int, rating_list: list[int], type_: str):
        query = rating.insert().values(date=date, id_student=id_student, rating=rating_list, type=type_)
        return await self._db.execute(query)


    async def get_last_rating_on_diapason(self, start_date: datetime, end_date: datetime, _type: str):
        subq = select(
            rating.c.id_rating,
            rating.c.date,
            rating.c.id_student,
            rating.c.rating,
            rating.c.type,
            func.row_number().over(
                partition_by=rating.c.id_student,
                order_by=rating.c.date.desc()
            ).label("rn")
        ).where(
            and_(
                rating.c.date.between(start_date, end_date),
                rating.c.type.in_([_type])
            )
        ).subquery()

        # основной запрос: берем только строки с rn = 1 (т.е. последние по дате для каждого id_student)
        query = select(
            subq.c.id_rating,
            subq.c.date,
            subq.c.id_student,
            subq.c.rating,
            subq.c.type
        ).where(subq.c.rn == 1)
        result = await self._db.fetch_all(query)
        return result

    # Добавление
    async def add_student(self, name: str, data: list[int]):
        query = student.insert().values(name=name, ids_discipline_teacher=data)
        return await self._db.execute(query)

    async def add_teacher(self, name: str):
        query = teacher.insert().values(name=name)
        return await self._db.execute(query)

    async def add_discipline(self, name: str, description: str):
        query = discipline.insert().values(name=name, description=description)
        return await self._db.execute(query)

    async def add_discipline_teacher(self, id_teacher: str, id_discipline: str):
        query = discipline_teacher.insert().values(id_teacher=id_teacher, id_discipline=id_discipline)
        return await self._db.execute(query)

    # 👇 Метод добавления моковых данных
    async def mock_data(self):
        await self.connect()

        # Преподаватели
        teacher_id_1 = await self.add_teacher("Тальяна Ковалёва")
        teacher_id_2 = await self.add_teacher("Сергей Матвеев")
        teacher_id_3 = await self.add_teacher("Лилия Бражник")
        teacher_id_4 = await self.add_teacher("Самарина Татьяна")
        teacher_id_5 = await self.add_teacher("Родин Самсон")
        teacher_id_6 = await self.add_teacher("Согатин Николай")


        # Дисциплины
        discipline_id_1 = await self.add_discipline(name="Веб-программирование", description="")
        discipline_id_2 = await self.add_discipline(name="ООП", description="")
        discipline_id_3 = await self.add_discipline(name="Базы данных", description="")
        discipline_id_4 = await self.add_discipline(name="Криптография", description="")
        discipline_id_5 = await self.add_discipline(name="Алгоритмы", description="")
        discipline_id_6 = await self.add_discipline(name="Теория вероятностей", description="")

        # Связь преподаватель-дисциплина
        dt_id_1 = await self.add_discipline_teacher(id_teacher=teacher_id_1, id_discipline=discipline_id_1)
        dt_id_2 = await self.add_discipline_teacher(id_teacher=teacher_id_1, id_discipline=discipline_id_2)
        dt_id_3 = await self.add_discipline_teacher(id_teacher=teacher_id_1, id_discipline=discipline_id_3)
        dt_id_4 = await self.add_discipline_teacher(id_teacher=teacher_id_1, id_discipline=discipline_id_4)

        dt_id_5 = await self.add_discipline_teacher(id_teacher=teacher_id_2, id_discipline=discipline_id_1)
        dt_id_6 = await self.add_discipline_teacher(id_teacher=teacher_id_2, id_discipline=discipline_id_2)
        dt_id_7 = await self.add_discipline_teacher(id_teacher=teacher_id_2, id_discipline=discipline_id_5)
        dt_id_8 = await self.add_discipline_teacher(id_teacher=teacher_id_2, id_discipline=discipline_id_6)

        dt_id_9 = await self.add_discipline_teacher(id_teacher=teacher_id_3, id_discipline=discipline_id_2)
        dt_id_10 = await self.add_discipline_teacher(id_teacher=teacher_id_3, id_discipline=discipline_id_3)
        dt_id_11 = await self.add_discipline_teacher(id_teacher=teacher_id_3, id_discipline=discipline_id_5)
        dt_id_12 = await self.add_discipline_teacher(id_teacher=teacher_id_3, id_discipline=discipline_id_6)

        dt_id_13 = await self.add_discipline_teacher(id_teacher=teacher_id_4, id_discipline=discipline_id_3)
        dt_id_14 = await self.add_discipline_teacher(id_teacher=teacher_id_4, id_discipline=discipline_id_5)

        dt_id_15 = await self.add_discipline_teacher(id_teacher=teacher_id_5, id_discipline=discipline_id_1)
        dt_id_16 = await self.add_discipline_teacher(id_teacher=teacher_id_5, id_discipline=discipline_id_6)

        dt_id_17 = await self.add_discipline_teacher(id_teacher=teacher_id_6, id_discipline=discipline_id_1)
        dt_id_18 = await self.add_discipline_teacher(id_teacher=teacher_id_6, id_discipline=discipline_id_2)
        dt_id_19 = await self.add_discipline_teacher(id_teacher=teacher_id_6, id_discipline=discipline_id_3)
        dt_id_20 = await self.add_discipline_teacher(id_teacher=teacher_id_6, id_discipline=discipline_id_6)

        # Студенты
        student_id_1 = await self.add_student(name="Алексей Смирнов Иванович",data=[1,2,3])
        student_id_1 = await self.add_student(name="Алексей Смирнов Иванович", data=[dt_id_1, dt_id_2, dt_id_3, dt_id_4, dt_id_5, dt_id_6, dt_id_7, dt_id_8, dt_id_13, dt_id_14])
        student_id_2 = await self.add_student(name="Кузнецова Елена Александровна", data=[dt_id_17, dt_id_18, dt_id_19, dt_id_20, dt_id_5, dt_id_6, dt_id_7, dt_id_8, dt_id_13, dt_id_14])
        student_id_3 = await self.add_student(name="Согатин Николай Анатольевич", data=[dt_id_1, dt_id_6, dt_id_10, dt_id_16, dt_id_14, dt_id_11])
        student_id_4 = await self.add_student(name="Самсон Иван Евгеньевич", data=[dt_id_9, dt_id_2, dt_id_3, dt_id_12, dt_id_5, dt_id_6, dt_id_15, dt_id_14, dt_id_18, dt_id_19])


        rating_student_t_0 = await self.add_rating(datetime.now() + timedelta(days=0), student_id_1, [4, 2, 1], type_="teacher")
        rating_student_t_1 = await self.add_rating(datetime.now() + timedelta(days=1), student_id_1, [2, 1, 4], type_="teacher")
        rating_student_d_0 = await self.add_rating(datetime.now() + timedelta(days=1), student_id_1, [1, 2, 4, 3, 5, 6], type_="discipline")

        rating_student_t_2 = await self.add_rating(datetime.now() + timedelta(days=-1), student_id_2, [2, 6, 4], type_="teacher")
        rating_student_d_1 = await self.add_rating(datetime.now() + timedelta(days=1), student_id_2, [3, 1, 6, 3, 5], type_="discipline")

        rating_student_t_3 = await self.add_rating(datetime.now() + timedelta(days=0), student_id_3, [3, 1, 4, 2, 5], type_="teacher")
        rating_student_d_2 = await self.add_rating(datetime.now() + timedelta(days=0), student_id_3, [6, 3, 2, 1, 5], type_="discipline")

        rating_student_4 = await self.add_rating(datetime.now() + timedelta(days=2), student_id_4, [1, 5, 2, 5, 4], type_="teacher")
        rating_student_d_3 = await self.add_rating(datetime.now() + timedelta(days=0), student_id_4, [1, 3, 2, 6, 5], type_="discipline")
        await self.disconnect()







    # Примеры CRUD-методов student

    async def get_all_students(self):
        query = student.select()
        return await self._db.fetch_all(query)

    async def get_student_by_id(self, student_id: int):
        query = student.select().where(student.c.id_student == student_id)
        return await self._db.fetch_one(query)

    async def update_student(self, student_id: int, name: str, subject_teacher_ids: list[int]):
        query = student.update().where(student.c.id_student == student_id).values(
            name=name, data_subject_teacher=subject_teacher_ids)
        return await self._db.execute(query)

    async def delete_student(self, student_id: int):
        query = student.delete().where(student.c.id_student == student_id)
        return await self._db.execute(query)

    # Примеры CRUD-методов teacher
    async def add_teacher(self, name: str):
        query = teacher.insert().values(name=name)
        return await self._db.execute(query)

    async def get_all_teachers(self):
        query = teacher.select()
        return await self._db.fetch_all(query)

    async def get_teacher_by_id(self, teacher_id: int):
        query = teacher.select().where(teacher.c.id_teacher == teacher_id)
        return await self._db.fetch_one(query)

    async def update_teacher(self, teacher_id: int, name: str):
        query = teacher.update().where(teacher.c.id_teacher == teacher_id).values(name=name)
        return await self._db.execute(query)

    async def delete_teacher(self, teacher_id: int):
        query = teacher.delete().where(teacher.c.id_teacher == teacher_id)
        return await self._db.execute(query)

    # Примеры CRUD-методов discipline
    async def add_discipline(self, name: str, description: str):
        query = discipline.insert().values(name=name, description=description)
        return await self._db.execute(query)

    async def get_all_disciplines(self):
        query = discipline.select()
        return await self._db.fetch_all(query)

    async def update_discipline(self, discipline_id: int, name: str, description: str):
        query = discipline.update().where(discipline.c.id_discipline == discipline_id).values(
            name=name, description=description)
        return await self._db.execute(query)

    async def delete_discipline(self, discipline_id: int):
        query = discipline.delete().where(discipline.c.id_discipline == discipline_id)
        return await self._db.execute(query)

    async def add_discipline_teacher(self, id_teacher: int, id_discipline: int):
        query = discipline_teacher.insert().values(id_teacher=id_teacher, id_discipline=id_discipline)
        return await self._db.execute(query)

    # Примеры CRUD-методов discipline
    async def get_all_discipline_teachers(self):
        query = discipline_teacher.select()
        return await self._db.fetch_all(query)

    async def delete_discipline_teacher(self, id_: int):
        query = discipline_teacher.delete().where(discipline_teacher.c.id_discipline_teacher == id_)
        return await self._db.execute(query)

    # Примеры CRUD-методов rating
    async def add_rating(self, date, id_student: int, rating_list: list[int], type_: str):
        query = rating.insert().values(date=date, id_student=id_student, rating=rating_list, type=type_)
        return await self._db.execute(query)

    async def get_all_ratings(self):
        query = rating.select()
        return await self._db.fetch_all(query)

    async def delete_rating(self, rating_id: int):
        query = rating.delete().where(rating.c.id_rating == rating_id)
        return await self._db.execute(query)

    # Примеры CRUD-методов feedback
    async def add_feedback(self, date, id_student: int, id_discipline_teacher: int, review: str,
                           orientation: str, theme: str, tonality: bool, profitability: bool):
        query = feedback.insert().values(
            date=date,
            id_student=id_student,
            id_discipline_teacher=id_discipline_teacher,
            review=review,
            orientation=orientation,
            theme=theme,
            tonality=tonality,
            profitability=profitability,
        )
        return await self._db.execute(query)

    async def get_all_feedbacks(self):
        query = feedback.select()
        return await self._db.fetch_all(query)

    async def delete_feedback(self, feedback_id: int):
        query = feedback.delete().where(feedback.c.id_review == feedback_id)
        return await self._db.execute(query)