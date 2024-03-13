from typing import Optional, List

from sqlalchemy import String, ForeignKey, Column, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import UniqueConstraint

from fcfmramos.model import db


class Departamento(db.Model):
    __tablename__ = "departamento"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(128), unique=True)
    codigo: Mapped[str] = mapped_column(String(128), unique=True)
    ucampus_id: Mapped[int] = mapped_column(unique=True)
    color: Mapped[Optional[str]] = mapped_column(String(6))
    is_ug: Mapped[bool] = mapped_column(default=False)

    ramos: Mapped[List["Ramo"]] = relationship(back_populates="departamento")
    planes: Mapped[List["Plan"]] = relationship(back_populates="departamento")


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
    departamento: Mapped["Departamento"] = relationship(back_populates="ramos")

    planes: Mapped[List["Plan"]] = relationship(
        secondary="plan_ramo", back_populates="ramos"
    )

    def serialize(self):
        sorted_cursos = sorted(
            self.cursos, key=lambda x: (x.año, x.semestre), reverse=True
        )
        latest_curso = sorted_cursos[0] if sorted_cursos else None
        return {
            "id": self.id,
            "codigo": self.codigo,
            "nombre": self.nombre,
            "departamento": self.departamento.nombre,
            "sct": self.sct,
            "sustentabilidad": self.sustentabilidad,
            "requisitos": self.requisitos,
            "ultima_dictacion": (
                f"{latest_curso.año}-{latest_curso.semestre}"
                if latest_curso
                else "Nunca"
            ),
            "planes": [plan.id for plan in self.planes]
        }


class Curso(db.Model):
    __tablename__ = "curso"
    id: Mapped[int] = mapped_column(primary_key=True)
    año: Mapped[int] = mapped_column()
    semestre: Mapped[int] = mapped_column()
    seccion: Mapped[int] = mapped_column()
    cupos: Mapped[int] = mapped_column()
    cupos_ocupados: Mapped[int] = mapped_column()

    ramo_id: Mapped[int] = mapped_column(ForeignKey("ramo.id"))
    ramo: Mapped["Ramo"] = relationship(back_populates="cursos")

    profesores: Mapped[List["Profesor"]] = relationship(
        secondary="curso_profesor", back_populates="cursos"
    )

    __table_args__ = (
        UniqueConstraint(
            "año", "semestre", "seccion", "ramo_id", name="sección"
        ),
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


class Plan(db.Model):
    __tablename__ = "plan"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(128), unique=True)

    departamento_id: Mapped[int] = mapped_column(ForeignKey("departamento.id"))

    departamento: Mapped["Departamento"] = relationship(
        back_populates="planes"
    )
    ramos: Mapped[List["Ramo"]] = relationship(
        secondary="plan_ramo", back_populates="planes"
    )


plan_ramo = Table(
    "plan_ramo",
    db.Model.metadata,
    Column("plan_id", ForeignKey("plan.id"), primary_key=True),
    Column("ramo_id", ForeignKey("ramo.id"), primary_key=True),
)
