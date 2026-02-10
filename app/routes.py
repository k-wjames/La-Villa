from flask import Blueprint, request, jsonify, current_app
from .models import Reservation
from .schemas import ReservationSchema
from . import db
from datetime import datetime
import threading

from flask_mail import Message
from app import mail


reservation_bp = Blueprint("reservations", __name__)

reservation_schema = ReservationSchema()
reservations_schema = ReservationSchema(many=True)


@reservation_bp.route("/test-mail", methods=["GET", "POST"])
def test_mail():
    msg = Message(
        subject="Test Email from Flask",
        recipients=["kwjames9326@gmail.com"],  # change this to your real inbox
        body="If you see this, Flask-Mail works 🎉"
    )
    try:
        mail.send(msg)
        print("✅ Test email sent successfully!")
        return jsonify({"message": "Email sent successfully!"}), 200
    except Exception as e:
        print(f"❌ Email sending failed: {e}")
        return jsonify({"error": str(e)}), 500




@reservation_bp.route("/health", methods=["POST"])
def health_check():
    data = request.get_json()  
    try:
        reservation = Reservation(
            full_name=data["full_name"],
            phone_number=data["phone_number"],
            email=data["email"],
            persons=data["persons"],
            date=datetime.strptime(data["date"], "%Y-%m-%d").date(),
            time=datetime.strptime(data["time"], "%H:%M").time()
        )

        serialized = reservation_schema.dump(reservation)
        return jsonify({"message": "Success", "data": serialized}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Send mails asynclonously on a separate thread so it doesn’t block the request.
def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
            print(f"Email sent successfully to {msg.recipients}")
        except Exception as e:
            print(f"Email sending failed: {e}")


# Make a reservation: Send confirmation mails to the client and the host

@reservation_bp.route("/book", methods=["POST"])
def create_booking():
    data = request.get_json()

    # Extract booking info
    full_name = data.get("full_name")
    email = data.get("email")
    phone = data.get("phone_number")
    persons=data.get("persons")
    date = data.get("date")
    time = data.get("time")

    # --- Send confirmation to the customer ---
    customer_msg = Message(
        subject="Reservation Confirmation - LaVilla",
        recipients=[email],
        body=f"Hi {full_name},\n\nYour reservtion for {date} at {time} for {persons} has been confirmed.\n\nThank you!\n\n— LaVilla Team"
    )
    # mail.send(customer_msg)

    # --- Send notification to host business ---
    host_msg = Message(
        subject="New Reservation Received",
        recipients=["reservations@lavilla.co.ke"],
        body=f"New reservation received:\n\nName: {full_name}\nEmail: {email}\nPhone: {phone}\nPersons: {persons}\nDate: {date}\nTime: {time}"
    )
    # mail.send(host_msg)

    # Run mail sends in background threads
    threading.Thread(target=send_async_email, args=(current_app._get_current_object(), customer_msg)).start()
    threading.Thread(target=send_async_email, args=(current_app._get_current_object(), host_msg)).start()

    return jsonify({"message": "Booking successful, emails queued!"}), 200




@reservation_bp.route("/create", methods=["POST"])
def create_reservation():
    data = request.get_json()
    try:
        reservation = Reservation(
            full_name=data["full_name"],
            phone_number=data["phone_number"],
            email=data["email"],
            persons=data["persons"],
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
            "persons":r.persons,
          "date": r.date.strftime("%d-%m-%y"),
            "time": r.time.strftime("%H:%M"),
           "created_at": r.created_at.strftime("%d-%m-%y %H:%M:%S")
        } for r in reservations
    ]
    return jsonify(result)  


@reservation_bp.route("/", methods=["GET"])
def home():
    return "<h2>Reservation API is running!</h2>"
