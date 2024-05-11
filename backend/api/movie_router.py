from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from api import models
from db.session import get_db
from actions.movie import _create, _delete, _get_by_id, _update


movie_router = APIRouter(prefix="/movie")


@movie_router.post("/", response_model=models.MovieShow)
async def create_movie(
    movie: models.MovieCreate,
    session: AsyncSession = Depends(get_db),
) -> models.MovieShow:
    new_movie = await _create(body=movie, session=session)
    if new_movie is None:
        raise HTTPException(
            status_code=404, detail=f"Movie with name {movie.name} already exists"
        )
    return new_movie


@movie_router.delete(
    "/{movie_id}",
    response_model=models.MovieUpdated,
)
async def delete_movie(
    movie_id: int,
    session: AsyncSession = Depends(get_db),
) -> models.MovieUpdated:
    deleted_movie_id = await _delete(movie_id, session)
    if deleted_movie_id is None:
        raise HTTPException(
            status_code=404, detail=f"Movie with id {movie_id} not found"
        )
    logging.info("Delete movie with id: %s", deleted_movie_id)
    return models.MovieUpdated(movie_id=deleted_movie_id)


@movie_router.get(
    "/{movie_id}",
    response_model=models.MovieShow,
)
async def get_movie_by_id(
    movie_id: int,
    session: AsyncSession = Depends(get_db),
) -> models.MovieShow:
    movie = await _get_by_id(movie_id, session)
    if movie is None:
        logging.warning("Movie with id %s not found", movie_id)
        raise HTTPException(
            status_code=404, detail=f"Movie with id {movie_id} not found"
        )
    logging.info("movie with id %s found", movie_id)
    return movie


@movie_router.patch(
    "/{movie_id}",
    response_model=models.MovieUpdated,
)
async def update_movie_by_id(
    movie_id: int,
    body: models.MovieUpdateRequest,
    session: AsyncSession = Depends(get_db),
) -> models.MovieUpdated:
    if body.dict(exclude_none=True) == {}:
        raise HTTPException(
            status_code=422,
            detail="At least one parameter for movie update info should be provided",
        )
    movie = await _get_by_id(movie_id, session)
    if movie is None:
        raise HTTPException(
            status_code=404, detail=f"movie with id {movie_id} not found"
        )
    updated_movie_id = await _update(
        updated_movie_params=body,
        movie_id=movie_id,
        session=session,
    )
    logging.info("Movie with id: %s updated successfully", updated_movie_id)
    return models.MovieUpdated(movie_id=updated_movie_id)
