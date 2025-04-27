from sqlalchemy.orm import Query

def paginate(query: Query, skip: int = 0, limit: int = 10):
    total = query.count()

    items = query.offset(skip).limit(limit).all()

    return items, total
