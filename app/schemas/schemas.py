from pydantic import BaseModel
from typing import Optional, List, ForwardRef

class StudentBase(BaseModel):
    name: str
    email: str
    information: Optional[str] = None 
    
class StudentCreate(StudentBase):
    id: str  

class Student(StudentBase):
    id: str  

    class Config:
        from_attributes = True  

# 用于返回包含组信息的学生数据
# Для возврата данных студента, включая информацию о группах
class StudentWithGroups(Student):
    groups: List["Group"] = []

class GroupBase(BaseModel):
    id: int
    description: Optional[str] = None

class GroupCreate(GroupBase):
    pass

class Group(GroupBase):
    id: int
    class Config:
        from_attributes = True  

# 用于返回包含学生信息的组数据
# Для возврата данных группы, включая информацию о студентах
class GroupWithStudents(Group):
    students: List[Student] = []

# 解决循环引用问题
# Решение проблемы циклических ссылок
StudentWithGroups.model_rebuild()
