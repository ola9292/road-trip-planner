from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///planner.db"
# initialize the app with the extension
db.init_app(app)

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/save-location', methods=['POST', 'GET'])
def save_location():
    data = request.get_json()
    if request.method == 'POST':
        print(data)
        location = Location(
            name = data.get("name"),
            latitude = data.get("latitude"),
            longitude = data.get("longitude"),
        )
        db.session.add(location)
        db.session.commit()
        return redirect(url_for("home"))
    else:
        print('nothing dey here ')
    return render_template('home.html')

@app.route('/get-locations', methods=['POST', 'GET'])
def get_location():
    locations = db.session.execute(db.select(Location).order_by(Location.name)).scalars()
    locations_list = [
        {
            "id": loc.id,
            "name": loc.name,
            "latitude": loc.latitude,
            "longitude": loc.longitude
        }
        for loc in locations
    ]

    return jsonify(locations_list), 200

@app.route("/location/<int:id>/delete", methods=["GET", "POST"])
def location_delete(id):
    location = db.get_or_404(Location, id)

    if request.method == "POST":
        db.session.delete(location)
        db.session.commit()
        return {"message": "Location deleted", "id": id}


class Location(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)
    
with app.app_context():
    db.create_all()