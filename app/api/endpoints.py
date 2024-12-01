from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..schemas import schemas
from ..crud import crud

router = APIRouter()
# 创建学生 Создание студентa
@router.post("/students/", response_model=schemas.Student, tags=["students"], summary="Create Student")
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = crud.get_student(db, student_id=student.id)
    if db_student:
        raise HTTPException(status_code=400, detail="Student ID already registered")
    return crud.create_student(db=db, student=student)
# 创建组 Создать группу
@router.post("/groups/", response_model=schemas.Group, tags=["groups"], summary="Create Group")
def create_group(group: schemas.GroupCreate, db: Session = Depends(get_db)):
    return crud.create_group(db=db, group=group)
# 获取学生 Получить студента по ID
@router.get("/students/{student_id}", response_model=schemas.Student, tags=["students"], summary="GET Student By ID")
def read_student(student_id: str, db: Session = Depends(get_db)):
    student = crud.get_student(db, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student
#获取组 Получить группу по ID
@router.get("/groups/{group_id}", response_model=schemas.Group, tags=["groups"], summary="GET Group By ID")
def read_group(group_id: int, db: Session = Depends(get_db)):
    group = crud.get_group(db, group_id)
    if group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return group
#删除学生 Удаление студентa
@router.delete("/students/{student_id}", tags=["students"], summary="Delete Student")
def delete_student(student_id: str, db: Session = Depends(get_db)):
    student = crud.delete_student(db, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted"}
#删除组Удаление группу
@router.delete("/groups/{group_id}", tags=["groups"], summary="Delete Group")
def delete_group(group_id: int, db: Session = Depends(get_db)):
    group = crud.delete_group(db, group_id)
    if group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return {"message": "Group deleted"}

# 获取学生 Получить студентов
@router.get("/students/", response_model=list[schemas.Student], tags=["students"], summary="Get Students")
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    students = crud.get_students(db, skip=skip, limit=limit)
    return students
# 获取组 Получить группы
@router.get("/groups/", response_model=list[schemas.Group], tags=["groups"], summary="Get Groups")
def read_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    groups = crud.get_groups(db, skip=skip, limit=limit)
    return groups
# 将学生添加到组 Добавить студентa в группу
@router.post("/groups/{group_id}/students/{student_id}", tags=["groups"],  summary="Add Student To Group")
def add_student_to_group(group_id: int, student_id: str, db: Session = Depends(get_db)):
    success = crud.add_student_to_group(db, student_id, group_id)
    if not success:
        raise HTTPException(status_code=404, detail="Student or group not found")
    return {"message": "Student added to group"}
# 将学生从组中删除 Удалить студентa из группы
@router.delete("/groups/{group_id}/students/{student_id}", tags=["groups"], summary="Delete Student From Group")
def remove_student_from_group(group_id: int, student_id: str, db: Session = Depends(get_db)):
    success = crud.remove_student_from_group(db, student_id, group_id)
    if not success:
        raise HTTPException(status_code=404, detail="Student or group not found")
    return {"message": "Student removed from group"}
# 获取组中的学生 Получить студентов из группы
@router.get("/groups/{group_id}/students/", response_model=list[schemas.Student], tags=["groups"], summary="Get Students In Group")
def read_students_in_group(group_id: int, db: Session = Depends(get_db)):
    students = crud.get_students_in_group(db, group_id)
    return students
#将学生从小组 A 转移到小组 B Переместить студентa из группы А в группу Б
@router.post("/students/{student_id}/transfer/", tags=["students"], summary="Transfer Student From A Group To B Group")
def transfer_student(student_id: str, from_group_id: int, to_group_id: int, db: Session = Depends(get_db)):
    success = crud.transfer_student(db, student_id, from_group_id, to_group_id)
    if not success:
        raise HTTPException(status_code=404, detail="Transfer failed")
    return {"message": "Student transferred successfully"}
