import datetime
import enum

from marshmallow_enum import EnumField

from billing.extensions import db, marshmallow

__all__ = ["BalanceTransaction"]


class BalanceTransactionType(enum.Enum):
    charge = "charge"
    payment = "payment"
    payment_refund = "payment_refund"


class BalanceTransactionStatus(enum.Enum):
    available = "available"
    pending = "pending"


class BalanceTransaction(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    account_id = db.Column(db.Integer(), db.ForeignKey("account.id"))
    type = db.Column(db.Enum(BalanceTransactionType, create_constraint=True))
    amount = db.Column(db.Integer(), default=0)
    currency = db.Column(db.String(3))
    status = db.Column(
        db.Enum(BalanceTransactionStatus, create_constraint=True), default=BalanceTransactionStatus.pending
    )

    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<BalanceTransaction {self.id}: {self.account_id}>"


class BalanceTransactionSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = BalanceTransaction
        include_fk = True

    type = EnumField(BalanceTransactionType, by_value=True)
    status = EnumField(BalanceTransactionStatus, by_value=True)


balance_transaction_schema = BalanceTransactionSchema()
balance_transactions_schema = BalanceTransactionSchema(many=True)
