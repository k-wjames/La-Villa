from . import ma
from .models import Reservation

class ReservationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Reservation
        load_instance = True
