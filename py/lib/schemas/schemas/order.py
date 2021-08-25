from dataclasses import dataclass

from dataclasses_avroschema import AvroModel


@dataclass
class OrderConfirmed(AvroModel):
    "An OrderConfirmed event"
    order_id: int

    class Meta:
        namespace = "OrderConfirmed.v1"
        aliases = ["order-confirmed-v1"]
