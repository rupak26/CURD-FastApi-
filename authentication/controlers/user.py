from schemas import  User2 , showUser
from database import get_db
from models import User
from fastapi import Depends, FastAPI , status , Response , HTTPException , APIRouter
from sqlalchemy.orm import Session  
from utils.oauth2 import role_required
from utils.hasing import Hasing
from typing import List
from repository import user
from response.schema import ApiResponse

router = APIRouter(
    prefix= '/api/v1/auth',
    tags=['User'] 
) 

@router.post('/create-user/', 
             summary="Create new user"  , 
             description='''
             Create New Users
             ''',
             status_code=status.HTTP_201_CREATED,
             response_model = ApiResponse)
def create_user_route(request: User2, db: Session = Depends(get_db)):
    return user.create_user(request, db)

@router.get('/get-all-users/',
            summary="Get all user",
            description='''
            Get all users
            ''',
            status_code=status.HTTP_202_ACCEPTED,
            response_model=ApiResponse)
def show_user(db : Session = Depends(get_db)):
    return user.show_all_user(db)

@router.get('/get-user/{id}',
            summary="Get individul user",
            description='''
            Get individul user based upon their id
            ''',
            status_code=status.HTTP_202_ACCEPTED,
            response_model=ApiResponse)
def show_user(id:int , db : Session = Depends(get_db)):
    return user.show_user_by_id(id , db)

########################################################
# @router.post(
#     "/introspect" ,
#     summary="Give token to different services",
#     include_in_schema=False
#     )
# def introspect_imple(request: TokenRequest):
#     service = UserServicesImpl()
#     response = service.introspect_token(request)
#     return response

# def introspect_token(self, request):
#         try:
#             db_row = user_repo.introspect_tokens(self,request.token)
#             payload = jwt.decode(request.token, SECRET_KEY, algorithms=[ALGORITHM])

#             if db_row:
#                 return {
#                     "active": True,
#                     "sub": payload.get("sub"),
#                     "role": payload.get("role"),
#                     "exp": payload.get("exp")
#                 }
#             else:
#                 return {"active": False}
#         except JWTError as e:
#             logger.error(f"JWT error in introspect: {str(e)}")
#             return {"active": False, "error": "Invalid token"}
#         except Exception as e:
#             logger.error(f"Unexpected error in introspect: {str(e)}")
#             return {"active": False, "error": str(e)}
        
# def introspect_tokens(self, token: str):
#     try:
#         with pool.acquire() as conn:
#             cursor = conn.cursor()
#             cursor.execute(
#                 """SELECT * FROM AUTH_TOKEN WHERE ACCESS_TOKEN = :token FETCH FIRST 1 ROWS ONLY""",
#                 {"token": token}
#             )
#             return cursor.fetchone()
#     except oracledb.DatabaseError as e:
#         logger.error(f"DB error in introspect_token: {e.args[0].message}")
#         raise

###############################################################