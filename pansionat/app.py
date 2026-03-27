from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/pansionat'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# табличка комнат
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(10))
    floor = db.Column(db.Integer)
    type = db.Column(db.String(50))  # "лежачие" или "активные"
    is_booked = db.Column(db.Boolean, default=False)

# табличка бронирования
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(50))
    description = db.Column(db.Text)
    suggested_room = db.Column(db.String(50))

with app.app_context():
    db.create_all()

    # 💡добавление комнат если их нет
    if Room.query.count() == 0:
        rooms = [
            Room(room_number="101", floor=1, type="лежачие"),
            Room(room_number="102", floor=1, type="лежачие"),
            Room(room_number="201", floor=2, type="активные"),
            Room(room_number="202", floor=2, type="активные"),
        ]
        db.session.add_all(rooms)
        db.session.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        desc = request.form['description'].lower()

        # определение типа комнаты под возможности и характерисьики человека
        if "лежач" in desc or "инвалид" in desc or "не ходит" in desc:
            room_type = "лежачие"
        elif "ходит" in desc or "активн" in desc or "самостоятельн" in desc:
            room_type = "активные"
        else:
            room_type = None

        room = None

        # поиск свободной комнатв подходящей по типу
        if room_type:
            room = Room.query.filter_by(type=room_type, is_booked=False).first()

        if room:
            # бронируем
            room.is_booked = True
            suggested_room = f"Комната {room.room_number}, {room.floor} этаж ({room.type})"
            booking = Booking(name=name, phone=phone, description=desc, suggested_room=suggested_room)
            db.session.add(booking)
            db.session.commit()
            message = f"Мы подобрали для вас {suggested_room}"
        else:
            # ответ когла вс подходящие места щаняты
            message = "К сожалению, все подходящие комнаты сейчас заняты. Мы свяжемся с вами, когда освободится место."

        return render_template('result.html', name=name, message=message)

    return render_template('booking.html')

if __name__ == '__main__':
    app.run(debug=True)
