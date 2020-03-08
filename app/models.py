from gino.ext.aiohttp import Gino

db = Gino()


class Dummy(db.Model):  # type: ignore
    __tablename__ = "dummy"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String())
