from flask import Blueprint, request, jsonify
from .models import Reservation
from .schemas import ReservationSchema
from . import db
from datetime import datetime



reservation_bp = Blueprint("reservations", __name__)

reservation_schema = ReservationSchema()
reservations_schema = ReservationSchema(many=True)


@reservation_bp.route("/create", methods=["POST"])
def create_reservation():
    data = request.get_json()
    try:
        reservation = Reservation(
            full_name=data["full_name"],
            phone_number=data["phone_number"],
            email=data["email"],
            date=datetime.strptime(data["date"], "%Y-%m-%d").date(),
            time=datetime.strptime(data["time"], "%H:%M").time()
        )
        db.session.add(reservation)
        db.session.commit()
        return jsonify({"message": "Reservation created", "id": reservation.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# @reservation_bp.route("/reservations", methods=["GET"])
# def get_reservations():
#     reservations = Reservation.query.all()
#     return reservations_schema.jsonify(reservations), 200
  
  
@reservation_bp.route("/all", methods=["GET"])
def get_reservations():
    reservations = Reservation.query.all()
    result = [
        {
            "id": r.id,
            "full_name": r.full_name,
            "phone_number": r.phone_number,
            "email": r.email,
          "date": r.date.strftime("%d-%m-%y"),
            "time": r.time.strftime("%H:%M"),
           "created_at": r.created_at.strftime("%d-%m-%y %H:%M:%S")
        } for r in reservations
    ]
    return jsonify(result)  


@reservation_bp.route("/", methods=["GET"])
def home():
    return "<h2>Reservation API is running!</h2>"
