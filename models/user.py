from sqlalchemy import String, BigInteger, ForeignKey
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import BaseModel


class User(BaseModel):
    name: Mapped[str] = mapped_column(String(255))
    username: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    favorite_films: Mapped[list['FavoriteFilm']] = relationship('FavoriteFilm', back_populates='user',
                                                                foreign_keys='FavoriteFilm.user_id')


class FavoriteFilm(BaseModel):
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey(User.id, ondelete='CASCADE'))
    kinopoisk_id: Mapped[int] = mapped_column(BigInteger)
    information: Mapped[dict] = mapped_column(JSON)
    user: Mapped['User'] = relationship('User', back_populates='favorite_films', foreign_keys=[user_id])
