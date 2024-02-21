from dataclasses import dataclass
from typing import Optional, List

from sqlalchemy import String, ForeignKey, Column, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fcfmramos.model import db


class Departamento(db.Model):
    __tablename__ = "departamento"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(128), unique=True)
    codigo: Mapped[str] = mapped_column(String(128), unique=True)
    ucampus_id: Mapped[int] = mapped_column(unique=True)
    color: Mapped[Optional[str]] = mapped_column(String(6))


@dataclass
class Ramo(db.Model):
    __tablename__ = "ramo"
    id: Mapped[int] = mapped_column(primary_key=True)
    codigo: Mapped[str] = mapped_column(String(128), unique=True)
    nombre: Mapped[str] = mapped_column(String(128))
    departamento_id: Mapped[int] = mapped_column(ForeignKey("departamento.id"))
    sct: Mapped[int] = mapped_column()
    sustentabilidad: Mapped[bool] = mapped_column(default=False)
    requisitos: Mapped[str] = mapped_column(String(256))

    cursos: Mapped[List["Curso"]] = relationship(back_populates="ramo")


class Curso(db.Model):
    __tablename__ = "curso"
    id: Mapped[int] = mapped_column(primary_key=True)
    año: Mapped[int] = mapped_column()
    semestre: Mapped[int] = mapped_column()
    seccion: Mapped[int] = mapped_column()

    ramo_id: Mapped[int] = mapped_column(ForeignKey("ramo.id"))
    ramo: Mapped["Ramo"] = relationship(back_populates="cursos")

    profesores: Mapped[List["Profesor"]] = relationship(
        secondary="curso_profesor", back_populates="cursos"
    )


curso_profesor = Table(
    "curso_profesor",
    db.Model.metadata,
    Column("curso_id", ForeignKey("curso.id"), primary_key=True),
    Column("profesor_id", ForeignKey("profesor.id"), primary_key=True),
)


class Profesor(db.Model):
    __tablename__ = "profesor"

    id: Mapped[int] = mapped_column(primary_key=True)
    ucampus_id: Mapped[str] = mapped_column(String(128), unique=True)
    nombre: Mapped[str] = mapped_column(String(128))

    cursos: Mapped[List["Curso"]] = relationship(
        secondary="curso_profesor", back_populates="profesores"
    )
