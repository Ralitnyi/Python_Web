from sqlalchemy import func

from connect_db import session
from models import Group, Student, Teacher

MODELS_DICT = {"Teacher": Teacher, "Student": Student, "Group": Group}


def create(name, id_, model):
    db_model = MODELS_DICT[model]
    if model == "Student":
        group_id = (
            session.query(Group.id, func.count(Student.id).label("student_count"))
            .select_from(Group)
            .join(Student, Group.id == Student.group_id)
            .group_by(Group.id)
            .order_by("student_count")
            .first()[0]
        )
        person = db_model(name=name, group_id=group_id)

    elif model == "Teacher" or model == "Group":
        person = db_model(name=name)

    session.add(person)
    session.commit()
    return (
        session.query(db_model.id, db_model.name)
        .select_from(db_model)
        .filter(db_model.name == name)
        .all()
    )


def list(name, id_, model):
    db_model = MODELS_DICT[model]
    return session.query(db_model.id, db_model.name).all()


def update(name, id_, model):
    db_model = MODELS_DICT[model]
    person = (
        session.query(db_model).select_from(db_model).filter(db_model.id == id_).first()
    )
    if person:
        person.name = name
        session.commit()
        return [person.id, person.name]
    return [f"{name} name not found"]


def remove(name, id_, model):
    db_model = MODELS_DICT[model]
    query = (
        session.query(db_model).select_from(db_model).filter(db_model.id == id_).first()
    )
    session.delete(query)
    session.commit()
    return [f"{query.name} was deleted"]
