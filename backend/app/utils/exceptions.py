from fastapi import HTTPException, status

def not_found(message: str):
    raise HTTPException(status_code=404, detail=message)

def bad_request(message: str):
    raise HTTPException(status_code=400, detail=message)

def conflict(message: str):
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=message
    )