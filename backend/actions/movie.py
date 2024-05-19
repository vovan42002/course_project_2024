from typing import Union

from api.models import AllMoviesShow, MovieCreate, MovieShow
from db.dals import MovieDAL


async def _create(body: MovieCreate, session) -> Union[MovieShow, None]:
    async with session.begin():
        movie_dall = MovieDAL(session)
        movie = await movie_dall.create(
            title=body.title,
            description=body.description,
        )
        if movie is not None:
            return MovieShow(
                title=movie.title,
                description=movie.description,
                is_active=movie.is_active,
                created_at=movie.created_at,
                updated_at=movie.updated_at,
            )


async def _delete(movie_id, session) -> Union[int, None]:
    async with session.begin():
        movie_dall = MovieDAL(session)
        deleted_movie = await movie_dall.delete(movie_id=movie_id)
        return deleted_movie


async def _update(
    updated_movie_params: dict, movie_id: int, session
) -> Union[int, None]:
    async with session.begin():
        movie_dall = MovieDAL(session)
        updated_movie = await movie_dall.update(movie_id, **updated_movie_params.dict())
        return updated_movie


async def _get_by_id(movie_id, session) -> Union[MovieShow, None]:
    async with session.begin():
        movie_dall = MovieDAL(session)
        movie = await movie_dall.get_by_id(movie_id=movie_id)
        if movie is not None:
            return MovieShow(
                title=movie.title,
                description=movie.description,
                is_active=movie.is_active,
                created_at=movie.created_at,
                updated_at=movie.updated_at,
            )


async def _get_all(session) -> Union[AllMoviesShow, None]:
    async with session.begin():
        movie_dal = MovieDAL(session)
        movies = await movie_dal.get_all_active()
        movies_show = []
        if movies is not None:
            for movie in movies:
                movies_show.append(
                    MovieShow(
                        title=movie.title,
                        description=movie.description,
                        is_active=movie.is_active,
                        created_at=movie.created_at,
                        updated_at=movie.updated_at,
                    )
                )
            return AllMoviesShow(result=movies_show)
