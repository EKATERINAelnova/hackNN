from sqlalchemy import (
    create_engine, MetaData, Table, Column,
    Integer, String, DateTime, Boolean, ForeignKey, ARRAY
)

metadata = MetaData()

# Таблицы
student = Table(
    "student", metadata,
    Column("id_student", Integer, primary_key=True, autoincrement=True),
    Column("name", String, nullable=False),
    Column("ids_discipline_teacher", ARRAY(Integer))
)

teacher = Table(
    "teacher", metadata,
    Column("id_teacher", Integer, primary_key=True, autoincrement=True),
    Column("name", String, nullable=False),
)

discipline = Table(
    "discipline", metadata,
    Column("id_discipline", Integer, primary_key=True, autoincrement=True),
    Column("name", String, nullable=False),
    Column("description", String),
)

discipline_teacher = Table(
    "discipline_teacher", metadata,
    Column("id_discipline_teacher", Integer, primary_key=True, autoincrement=True),
    Column("id_teacher", Integer, ForeignKey("teacher.id_teacher")),
    Column("id_discipline", Integer, ForeignKey("discipline.id_discipline")),
)

rating = Table(
    "rating", metadata,
    Column("id_rating", Integer, primary_key=True, autoincrement=True),
    Column("date", DateTime),
    Column("id_student", Integer, ForeignKey("student.id_student")),
    Column("rating", ARRAY(Integer)),
    Column("type", String),
)

feedback = Table(
    "feedback", metadata,
    Column("id_review", Integer, primary_key=True, autoincrement=True),
    Column("date", DateTime),
    Column("id_student", Integer, ForeignKey("student.id_student")),
    Column("id_discipline_teacher", Integer, ForeignKey("discipline_teacher.id_discipline_teacher")),
    Column("review", String),
    Column("orientation", String),
    Column("theme", String),
    Column("tonality", Boolean),
    Column("profitability", Boolean),
)