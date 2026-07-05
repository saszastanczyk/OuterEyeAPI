import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, Request, HTTPException, status
from fastapi.dependencies.utils import Annotated

from Database import get_db
from Models import User


async def get_user(request:Request, db: Annotated[AsyncSession,Depends(get_db)]) -> User:
    username = request.headers.get('X-Username')

    if username is None or username.strip() == '':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="No username provided")
    else:
        query = sa.select(User).where(User.username == username)
        result = await db.execute(query)
        user = result.scalar_one_or_none()
        if user is None:
            user = User(username=username)
            db.add(user)
            await db.flush()
            await db.refresh(user)
            await db.commit()
        return user

CurrentUser = Annotated[User,Depends(get_user)]