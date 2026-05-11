"""
Маршруты регистрации, входа и профиля.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import get_auth_usecase, get_current_user_id
from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserPublic
from app.usecases.auth import AuthUseCase

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    body: RegisterRequest,
    auth: Annotated[AuthUseCase, Depends(get_auth_usecase)],
) -> UserPublic:
    """Создание пользователя без передачи пароля в ответе."""

    user = await auth.register(body.email, body.password)
    return UserPublic.model_validate(user)


@router.post("/login", response_model=TokenResponse)
async def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth: Annotated[AuthUseCase, Depends(get_auth_usecase)],
) -> TokenResponse:
    """Выдаёт JWT; поле username формы содержит email."""

    token = await auth.login(form.username, form.password)
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserPublic)
async def read_me(
    user_id: Annotated[int, Depends(get_current_user_id)],
    auth: Annotated[AuthUseCase, Depends(get_auth_usecase)],
) -> UserPublic:
    """Профиль по токену текущего пользователя."""

    user = await auth.get_profile(user_id)
    return UserPublic.model_validate(user)
