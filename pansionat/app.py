from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/pansionat'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


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
