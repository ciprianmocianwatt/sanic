import sanic_openapi.openapi3.openapi
from sanic import Blueprint, json


from article.models import Article, User, UserEmailHistory

from article.dtos import (
    ArticleDto, UserDto, UserEmailHistoryDto,
    CreateUserEmailHistoryDto
)
from sanic_openapi.openapi3 import openapi
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

articles = Blueprint("articles", url_prefix='/articles')
users = Blueprint("users", url_prefix='/users')


@articles.get('/<article_id:int>')
@openapi.response(200, {"application/json": ArticleDto})
async def get_article(request, article_id):
    async_session = request.app.ctx.session
    async with async_session() as session:
        async with session.begin():
            query = select(Article).where(Article.id == article_id)
            result = await session.execute(query)
            article = result.scalar()

    return json(ArticleDto.from_orm(article).dict())


@articles.get('/')
@openapi.summary("Retrieve all articles")
@openapi.response(200, {"application/json": ArticleDto.schema()})
async def get_articles(request):
    async_session = request.app.ctx.session
    async with async_session() as session:
        async with session.begin():
            _articles = await session.execute(select(Article))
            arts = []
            for article in _articles.scalars():
                arts.append(ArticleDto.from_orm(article).dict())

    return json(arts)


@articles.post('/article')
@openapi.summary("Retrieve all articles")
@openapi.body({"application/json": ArticleDto.schema()})
@openapi.response(200, {"application/json": ArticleDto.schema()})
@openapi.parameter("bearer", str, location="header", required=True)
async def create_article(request):
    article_dto: ArticleDto = ArticleDto.parse_obj(request.json)
    async_session = request.app.ctx.session
    async with async_session() as session:
        async with session.begin():
            article = Article(
                title=article_dto.title,
                author=article_dto.author,
                content=article_dto.content
            )

            session.add(article)
            session.commit()

    return json(ArticleDto.from_orm(article).dict())


@users.post("/")
async def create_user(request):
    user_dto: UserDto = UserDto.parse_obj(request.json)
    async_session = request.app.ctx.session
    async with async_session() as session:
        async with session.begin():
            user = User(email=user_dto.email)
            session.add(user)
            session.commit()

    return json(UserDto.from_orm(user).dict())


@users.get("/")
async def get_user_eh(request):
    async_session = request.app.ctx.session
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(
                select(UserEmailHistory.user_email).where(UserEmailHistory.user_id == 3)
            )
            user_eh = result.scalars()
            print(type(user_eh))
            if "ciprian5@mailinator.com" in user_eh:
                print("fuck off")


    return json({"emai": "fuck"})


@users.get('/user/<user_id:int>')
async def get_user_by_email_history_id(request, user_id):
    async_session = request.app.ctx.session
    async with async_session() as session:
        async with session.begin():
            query = select(User).where(User.id == user_id)
            result = await session.execute(query)
            user = result.scalars().first()

    return json(UserDto.from_orm(user).dict())


@users.get('/email-history/<user_id:int>')
async def get_email_history_by_user_id(request, user_id):
    async_session = request.app.ctx.session
    async with async_session() as session:
        async with session.begin():
            query = select(UserEmailHistory).join(User).where(User.id == user_id)
            result = await session.execute(query)
            email_histories = result.scalars()
            l = []
            for eh in email_histories:
                l.append(UserEmailHistoryDto.from_orm(eh).dict())

    return json(l)


@users.get('/email-histories')
async def get_user_by_email_histories(request):
    async_session = request.app.ctx.session
    async with async_session() as session:
        async with session.begin():
            query = select(UserEmailHistory)
            result = await session.execute(query)
            email_histories = result.scalars()
            l = []
            for eh in email_histories:
                l.append(UserEmailHistoryDto.from_orm(eh).dict())

    return json(l)


@users.post('/create-email-history')
async def create_email_history(request):
    email_history_dto = CreateUserEmailHistoryDto.parse_obj(request.json)
    async_session = request.app.ctx.session
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(
                select(User).options(
                    selectinload(User.email_history)
                ).where(User.id == 3)
            )
            user = result.scalars().first()

            email_history = UserEmailHistory(
                user_email = email_history_dto.user_email,
                user_id = user.id
            )

            session.add(email_history)
            session.commit()

    return json(UserEmailHistoryDto.from_orm(email_history).dict())


@users.put('/update-email-history/<eh:int>')
async def create_email_history(request, eh):
    email_history_dto = UserEmailHistoryDto.parse_obj(request.json)
    async_session = request.app.ctx.session
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(
                select(UserEmailHistory).where(UserEmailHistory.id == eh)
            )
            email_history = result.scalars().first()
            email_history.user_email = email_history_dto.user_email
            session.add(email_history)
            session.commit()

    return json(UserEmailHistoryDto.from_orm(email_history).dict())


