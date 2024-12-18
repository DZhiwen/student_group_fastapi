from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models import models
from ..schemas import schemas


def create_student(db: Session, student: schemas.StudentCreate) -> models.Student:
    try:
        db_student = models.Student(**student.model_dump())
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        return db_student
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def create_group(db: Session, group: schemas.GroupCreate) -> models.Group:
    try:
        db_group = models.Group(**group.model_dump())
        db.add(db_group)
        db.commit()
        db.refresh(db_group)
        return db_group
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def get_student(db: Session, student_id: str) -> Optional[models.Student]:
    return db.query(models.Student).filter(models.Student.id == student_id).first()

def get_group(db: Session, group_id: int) -> Optional[models.Group]:
    return db.query(models.Group).filter(models.Group.id == group_id).first()

def get_students(db: Session, skip: int = 0, limit: int = 100) -> List[models.Student]:
    return db.query(models.Student).offset(skip).limit(limit).all()

def get_groups(db: Session, skip: int = 0, limit: int = 100) -> List[models.Group]:
    return db.query(models.Group).offset(skip).limit(limit).all()

def delete_student(db: Session, student_id: str) -> models.Student:
    try:
        student = get_student(db, student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        db.delete(student)  #删除学生 Удалить студента
        db.commit()
        return student
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def delete_group(db: Session, group_id: int) -> models.Group:
    try:
        group = get_group(db, group_id)
        if not group:
            raise HTTPException(status_code=404, detail="Group not found")
        
        db.delete(group)
        db.commit()
        return group
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def add_student_to_group(db: Session, student_id: str, group_id: int) -> bool:
    try:
        student = get_student(db, student_id)
        group = get_group(db, group_id)
        
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        if not group:
            raise HTTPException(status_code=404, detail="Group not found")
        if student in group.students:
            raise HTTPException(status_code=400, detail="Student already in group")
        
        group.students.append(student)
        db.commit()
        return True
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def remove_student_from_group(db: Session, student_id: str, group_id: int) -> bool:
    try:
        student = get_student(db, student_id)
        group = get_group(db, group_id)
        
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        if not group:
            raise HTTPException(status_code=404, detail="Group not found")
        if student not in group.students:
            raise HTTPException(status_code=400, detail="Student not in group")
        
        group.students.remove(student)
        db.commit()
        return True
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def transfer_student(db: Session, student_id: str, from_group_id: int, to_group_id: int) -> bool:
    try:
        student = get_student(db, student_id)
        from_group = get_group(db, from_group_id)
        to_group = get_group(db, to_group_id)
        
        if not all([student, from_group, to_group]):
            raise HTTPException(status_code=404, detail="Student or group not found")
        
        if student not in from_group.students:
            raise HTTPException(status_code=400, detail="Student not in source group")
        
        if student in to_group.students:
            raise HTTPException(status_code=400, detail="Student already in target group")
        
        from_group.students.remove(student)
        to_group.students.append(student)
        db.commit()
        return True
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
def get_students_in_group(db: Session, group_id: int) -> List[models.Student]:
    group = get_group(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group.students