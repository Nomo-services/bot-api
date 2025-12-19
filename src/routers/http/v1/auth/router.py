from fastapi import APIRouter, Depends, Request, Response, status

AuthRouter = APIRouter(prefix="/auth", tags=["Auth"])

@AuthRouter.post(
    "/signin",
    status_code=status.HTTP_200_OK,
)
async def telegram_signin(
    request: Request,
    response: Response,
    body: TelegramSigninRequest,
) -> TelegramSigninResponse:
