from sanic import Blueprint, json


from article.models import Article, User, UserEmailHistory

from article.dtos import (
    ArticleDto, UserDto, UserEmailHistoryDto,
    CreateUserEmailHistoryDto
)
from sanic_openapi.openapi3 import openapi
from sqlalchemy.future import select

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


@users.get('/user/<user_id:int>')
async def get_user_by_id(request, user_id):
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
