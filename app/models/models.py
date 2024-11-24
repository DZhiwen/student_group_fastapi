from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from ..database.database import Base



# 学生-组关联表 Таблица связи студентов с группами
student_group = Table(
    'student_group',
    Base.metadata,
    Column('student_id', String, ForeignKey('students.id')),
    Column('group_id', Integer, ForeignKey('groups.id'))
)

class Student(Base):
    __tablename__ = "students"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    information = Column(String, nullable=True)
    groups = relationship("Group", secondary=student_group, back_populates="students")
    def __repr__(self):
        return f"<Student {self.name}>"

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    students = relationship("Student", secondary=student_group, back_populates="groups")
    description = Column(String)
