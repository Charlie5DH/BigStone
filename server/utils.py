from bson.objectid import ObjectId
from datetime import datetime
from datetime import timedelta


def convert_object_id(o):
    '''
    ObjectId values are nested within the object and are not at the top level.
    In this case, you will need to use a custom function that recursively searches for and
    converts any ObjectId values to strings.
'''
    if isinstance(o, dict):
        return {convert_object_id(k): convert_object_id(v) for k, v in o.items()}
    elif isinstance(o, list):
        return [convert_object_id(v) for v in o]
    elif isinstance(o, ObjectId):
        return str(o)
    elif isinstance(o, datetime):
        return o.isoformat()
    else:
        return o


def get_init_and_end_timestamp_from_period(period):

    if period == "Hoje":
        start_timestamp = datetime.now().replace(
            hour=0, minute=0, second=0, microsecond=0)
        end_timestamp = datetime.now().replace(
            hour=23, minute=59, second=59, microsecond=999999)
    elif period == "Ontem":
        start_timestamp = datetime.now().replace(hour=0, minute=0, second=0,
                                                 microsecond=0) - timedelta(days=1)
        end_timestamp = datetime.now().replace(hour=23, minute=59, second=59,
                                               microsecond=999999) - timedelta(days=1)
    elif period == "Últimos 7 dias":
        start_timestamp = datetime.now().replace(hour=0, minute=0, second=0,
                                                 microsecond=0) - timedelta(days=7)
        end_timestamp = datetime.now().replace(
            hour=23, minute=59, second=59, microsecond=999999)
    elif period == "Últimos 30 dias":
        start_timestamp = datetime.now().replace(hour=0, minute=0, second=0,
                                                 microsecond=0) - timedelta(days=30)
        end_timestamp = datetime.now().replace(
            hour=23, minute=59, second=59, microsecond=999999)
    elif period == "3 Mêses":
        start_timestamp = datetime.now().replace(hour=0, minute=0, second=0,
                                                 microsecond=0) - timedelta(days=90)
        end_timestamp = datetime.now().replace(
            hour=23, minute=59, second=59, microsecond=999999)
    elif period == "Selecione um período":
        if start_timestamp is None or end_timestamp is None:
            raise HTTPException(
                status_code=400, detail="start_timestamp and end_timestamp must be provided")
        start_timestamp = datetime.fromisoformat(start_timestamp)
        end_timestamp = datetime.fromisoformat(end_timestamp)

    # timestamp in db is in isoformat
    start_timestamp = start_timestamp.isoformat()
    end_timestamp = end_timestamp.isoformat()

    return start_timestamp, end_timestamp
