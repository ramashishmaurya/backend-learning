import select
from fastapi import FastAPI, Depends , HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from auth import get_db 
from auth import User , Responsemodel
from auth import CreateUser , LoginRequest , Updateinformation
from jose import jwt 
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from datetime import datetime, timedelta, timezone

from auth import hash_password , verify_password
from auth.key import SECRET_KEY

app = FastAPI()

@app.post("/users/")
async def create_user(
    user : CreateUser , 
    db : AsyncSession = Depends(get_db)
):
    new_user = User(
        name = user.name , 
        email = user.email , 
        password = hash_password(user.password)

    )

    db.add(new_user)

    await db.commit()
    await db.refresh(new_user)

    return {
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email
    
    }

SECRET_KEYS = "8zxHBOkiYT5roos1I6hKs1qxluBT9Z7JzG8DfUXrpVU"
ALGORITHM = "HS256"
EXCESS_EXPIRY_MINUTES = 30 

def create_access_token(data : dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    to_encode.update({'exp' : expire})

    encode_jwt = jwt.encode(to_encode , SECRET_KEYS , algorithm=ALGORITHM)

    return encode_jwt



@app.get("/getdata", response_model=list[Responsemodel])  
async def get_information(
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User)
    )

    user = result.scalars().all()

    return user
    

@app.get("/pdata/{id}/")
async def getdata(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(User.id == id)
    )

    user = result.scalar_one_or_none()

    if user is None:
        return {
            "message": "User not found"
        }

    return {
        "datainformation": user
    }


@app.delete("/userdelete/{id_name}/")
async def userdeleteinformation(id_name:int , db : AsyncSession= Depends(get_db)) :
    result = await db.execute(
        select(User).where(User.id == id_name)
    )

    rs = result.scalar_one_or_none()

    if rs is None:
        return {"messages" : "Product not found"}
    
    await db.delete(rs)
    await db.commit()

    return{"messages" : "product deleted successfully"}


@app.post("/signup/")
async def register_user(
    user: CreateUser,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(User.email == user.email)
    )

    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)

    await db.commit()
    await db.refresh(new_user)

    return {
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email , 
        "password" : new_user.password
    }


@app.post("/login/")
async def login_user(
    user : LoginRequest , 
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(User.email == user.email)
    )

    db_user = result.scalar_one_or_none()

    if db_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    if not verify_password(
        user.password ,
        db_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    
    access_token = create_access_token({
        "db_user" : db_user.id
    })

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@app.post("/loginuser/")
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    
    result = await db.execute(
        select(User).where(User.email == form_data.username)
    )

    db_user = result.scalar_one_or_none()

    if db_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # 3. Password verify 
    if not verify_password(
        form_data.password,
        db_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # 4. JWT token banao
    access_token = create_access_token({
        "user_id": db_user.id
    })

    # 5. Token return karo
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }



@app.put("/update/{user_id}/")
async def updateinformation(
    user_id : int ,
    user : Updateinformation , 
    db : AsyncSession = Depends(get_db)
):
    result  =  await db.execute(
        select(User).where(User.id == user_id)
    )

    reps  = result.scalar_one_or_none()

    if reps is None:
        raise HTTPException(
            status_code=400 , 
            detail="USer id not found"
        )
    
    reps.email = user.email

    await db.commit()
    await db.refresh(reps)

    return ({
        "id" : reps.id , 
        "email" : reps.email

    }
    )


@app.get("/getdata/{user_id}/" ,response_model=Responsemodel)
async def getdatabyid( user_id : int , db : AsyncSession = Depends(get_db)):

    result  = await db.execute(
        select(User).where(User.id ==user_id)
    )

    db_conn = result.scalar_one_or_none()

    return db_conn

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Ye hamara custom bouncer (Dependency) hai jo Token ko khol ke padhega
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        # Token ko open karo apne secret key ke sath
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        
        # Token me se username aur role nikalo
        username = payload.get("sub")
        role = payload.get("role")
        
        if username is None:
            raise HTTPException(status_code=401, detail="Nakli Token!")
            
        return {"username": username, "role": role}
        
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token expire ya kharab ho gaya")

