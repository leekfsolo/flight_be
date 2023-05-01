from provider.authProvider import authenticate_user, encodeJWT
from fastapi import Depends, APIRouter, HTTPException, status, Body, Header
from models.user import UserLogin, User
from provider.jwtProvider import jwtBearer
from provider.authProvider import decodeJWT

auth = APIRouter()

@auth.post("/token")
async def login_for_access_token(user: UserLogin = Body(default=None)):
    userDB = authenticate_user(username=user.email, password=user.password)
    if not userDB:
        return {'success': False, 'message': 'Invalid email or password'}
    access_token = encodeJWT(user=userDB["email"])
    return {'success': True, 'token': access_token, 'message': 'Login successfully'}


@auth.get("/getMyInfo",dependencies=[Depends(jwtBearer())])
async def getMyInfo(Authorization: str = Header(default=None)):
    token = Authorization.split(' ')[1]
    userDB = decodeJWT(token)
    return {"success": True, "data": userDB['user']}

@auth.post("/logout",dependencies=[Depends(jwtBearer())])
async def logout():
    return {"success": True, "message": "Logout successfully"}