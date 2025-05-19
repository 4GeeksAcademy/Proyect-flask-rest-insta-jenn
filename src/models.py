from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    lastname: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(120), nullable=False)

    # esto lo va a relacionar con las otras tablas
    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="author")
    followers = relationship("Follower", foreign_keys="[Follower.user_to_id]", back_populates="followed")
    following = relationship("Follower", foreign_keys="[Follower.user_from_id]", back_populates="follower")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "lastname": self.lastname,
            "email": self.email,
            # no incluir la contraseña aquí
        }
class Post(db.Model):
    __tablename__ = 'post'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)

    # Relaciones
    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    media_items = relationship("Media", back_populates="post", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
        }
class Comment(db.Model):
    __tablename__ = 'comment'

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)
    comment_text: Mapped[str] = mapped_column(Text, nullable=True)

    # Relaciones
    author = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

    def serialize(self):
        return {
            "id": self.id,
            "author_id": self.author_id,
            "post_id": self.post_id,
            "comment_text": self.comment_text
        }
class Follower(db.Model):
    __tablename__ = 'follower'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_from_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    user_to_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)

    # Relaciones hacia el modelo User
    follower = relationship("User", foreign_keys=[lambda: Follower.user_from_id], back_populates="following")
    followed = relationship("User", foreign_keys=[lambda: Follower.user_to_id], back_populates="followers")

    def serialize(self):
        return {
            "id": self.id,
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id
        }

class Media(db.Model):
    __tablename__ = 'media'

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)

    # Relación con Post
    post = relationship("Post", back_populates="media_items")

    def serialize(self):
        return {
            "id": self.id,
            "url": self.url,
            "post_id": self.post_id
        }
