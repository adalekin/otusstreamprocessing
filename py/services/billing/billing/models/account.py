import datetime

from billing.extensions import db, marshmallow

__all__ = ["Account"]


class Account(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), index=True)
    balance = db.Column(db.Integer(), default=0)

    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<Account {self.id}: {self.user_id}>"


class AccountSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = Account


account_schema = AccountSchema()
accounts_schema = AccountSchema(many=True)
