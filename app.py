from faker import Faker
from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime, timedelta
from random import randint
from flask import jsonify

"""
app: Flask App configuration
db: DB configuration for using ORM
faker: for generate fake data
"""
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
faker_obj: Faker = Faker()
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Meter(db.Model):
    """
        Meter Table which is going to hold meter objects
    """
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(255), nullable=False)
    meter_data = db.relationship('MeterData', backref='meter', lazy=True)


class MeterData(db.Model):
    """
        Meter Table which is going to hold meter's data
    """
    id = db.Column(db.Integer, primary_key=True)
    meter_id = db.Column(db.Integer, db.ForeignKey('meter.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    value = db.Column(db.Integer, nullable=False)


@app.route('/meters/')
def get_meters():
    """api to get all the meters available in database
    :return: jsonify meter labels
    """
    meters: list[Meter] = Meter.query.all()
    meter_labels: list = [{"label": meter.label,
                           "meters_url": url_for('get_meter_data', meter_id=meter.id, _external=True)
                           } for meter in meters]
    return jsonify(meter_labels)


@app.route('/meters/<int:meter_id>/', methods=['GET'])
def get_meter_data(meter_id: int):
    """api to get all the meter' data available in database based on meter id
    :return: jsonify meter data
    """
    meter: int = Meter.query.get(meter_id)
    if not meter:
        return jsonify({'error': 'Meter not found'}), 404

    meter_data: list[MeterData] = MeterData.query.filter_by(meter_id=meter_id) \
        .order_by(MeterData.timestamp).all()

    data = [
        {
            'timestamp': entry.timestamp,
            'value': entry.value
        }
        for entry in meter_data
    ]

    return jsonify(data)


@app.route('/generate_dummy_data', methods=['GET'])
def generate_dummy_data():
    """api for generating fake data for Meter and MeterData table
    :return: jsonify meter labels and meter data
    """
    num_meters: int = 5
    num_records: int = 10

    # Generate dummy Meter records
    dummy_meters: list = []
    dummy_data: list = []
    for i in range(num_meters):
        label = f'Meter {faker_obj.name()}'
        meter = Meter(label=label)
        db.session.add(meter)
        dummy_meters.append({'label': label})

        # Generate dummy meter data for the current meter
        current_time = datetime.now()
        for _ in range(num_records):
            timestamp = current_time - timedelta(minutes=randint(1, 60))
            value = randint(0, 100)
            meter_data: MeterData = MeterData(meter=meter, timestamp=timestamp, value=value)
            db.session.add(meter_data)
            dummy_data.append({'timestamp': timestamp, 'value': value})

    db.session.commit()

    return jsonify({'dummy_meters': dummy_meters, 'dummy_meters_data': dummy_data})


if __name__ == '__main__':
    with app.app_context():
        generate_dummy_data()
    app.run()
