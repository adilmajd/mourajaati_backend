from fastapi import HTTPException
from sqlmodel import Session, select


def create_entity(session: Session, entity):
    session.add(entity)
    session.commit()
    session.refresh(entity)
    return entity

def get_all_entities(session: Session, model):
    return session.exec(select(model)).all()

def get_entity_by_id(session: Session, model, entity_id: int):
    entity = session.get(model, entity_id)
    if not entity:
        raise HTTPException(404, f"{model.__name__} non trouvé")
    return entity

def update_entity(session: Session, model, entity_id: int, updates: dict):
    entity = session.get(model, entity_id)
    if not entity:
        raise HTTPException(404, f"{model.__name__} non trouvé")
    for key, value in updates.items():
        setattr(entity, key, value)
    session.add(entity)
    session.commit()
    session.refresh(entity)
    return entity

def delete_entity(session: Session, model, entity_id: int):
    entity = session.get(model, entity_id)
    if not entity:
        raise HTTPException(404, f"{model.__name__} non trouvé")
    session.delete(entity)
    session.commit()
    return {"message": f"{model.__name__} {entity_id} supprimé avec succès"}