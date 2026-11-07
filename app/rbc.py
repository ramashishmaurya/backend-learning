
from enum import Enum

from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel

app = FastAPI()


# 1. Define user roles
class UserRole(str, Enum):
    EMPLOYEE = "employee"
    MANAGER = "manager"
    ADMIN = "admin"


# 2. Define the User model
class User(BaseModel):
    id: int
    username: str
    email: str
    role: UserRole


# 3. Get the current user (demo only)
def get_current_user() -> User:
    return User(
        id=1,
        username="john",
        email="ashish123@gmail.com",
        role=UserRole.EMPLOYEE,
    )


# 4. RBAC permission checker
class RoleChecker:
    def __init__(self, allowed_roles: list[UserRole]):
        self.allowed_roles = allowed_roles

    def __call__(  
        self,
        current_user: User = Depends(get_current_user),
    ) -> User:
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient Permissions",
            )

        return current_user


# 5. Profile route: any authenticated user
@app.get("/api/v1/profile")
def get_my_profile(
    current_user: User = Depends(get_current_user),
):
    return {
        "message": f"Welcome {current_user.username}",
        "data": current_user.role,
    }


# 6. Manager/Admin route
@app.get(
    "/api/v1/manager/reports",
    dependencies=[
        Depends(
            RoleChecker([UserRole.MANAGER, UserRole.ADMIN])
        )
    ],
)
def get_manager_reports():
    return {
        "status": "success",
        "data": [
            "Team Performance Q3",
            "Salary Reviews",
            "Leave Approvals",
        ],
    }


# 7. Admin-only route
@app.delete(
    "/api/v1/admin/users/{user_id}",
    dependencies=[
        Depends(RoleChecker([UserRole.ADMIN]))
    ],
)
def delete_user_account(user_id: int):
    return {
        "status": "success",
        "data": f"User account {user_id} has been deleted",
    }

