from sqlalchemy.orm import Query
import logging

def paginate(query: Query, skip: int = 0, limit: int = 10):
    logging.info(f"Paginate called with skip: {skip}, limit: {limit}")
    total_query = query.order_by(None).with_entities(query.column_descriptions[0]['entity'].id)
    total = total_query.distinct().count()
    logging.info(f"Total distinct products: {total}")
    items = query.offset(skip).limit(limit).all()
    logging.info(f"Products returned: {len(items)}")
    return items, total
