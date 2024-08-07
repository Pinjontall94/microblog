from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db


class User(db.Model):
    # Define the fields (a.k.a. the columns in the User table)
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(128), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    # Define relationships (NOTE: these are not fields!)
    #  NOTE: WriteOnlyMapped determines posts is a collection type of
    #        individual Post models
    #
    #  NOTE: Post class is in quotes as a forward reference; otherwise
    #        just the class name would suffice
    posts: so.WriteOnlyMapped["Post"] = so.relationship(back_populates="author")

    # Define some text representation for an instance of this model
    def __repr__(self):
        return "<User {}>".format(self.username)


class Post(db.Model):
    # Define fields
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc)
    )
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

    # Define relationships
    author: so.Mapped[User] = so.relationship(back_populates="posts")

    # Define the text representation
    def __repr__(self):
        return "<Post {}>".format(self.body)
