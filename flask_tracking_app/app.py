from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)
api = Api(app)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tracking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the tracking model
class TrackingRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tracking_number = db.Column(db.String(80), unique=True, nullable=False)
    status = db.Column(db.String(120), nullable=False)

# Create the database
with app.app_context():
    db.create_all()

# Define tracking API
class Tracking(Resource):
    def get(self, tracking_number):
        record = TrackingRecord.query.filter_by(tracking_number=tracking_number).first()
        if record:
            return jsonify({"tracking_number": record.tracking_number, "status": record.status})
        return jsonify({"message": "Tracking number not found"}), 404

    def post(self):
        data = request.json
        new_record = TrackingRecord(
            tracking_number=data.get('tracking_number'),
            status=data.get('status', 'In Transit')
        )
        db.session.add(new_record)
        db.session.commit()
        return jsonify({"message": "Tracking record created"}), 201

# Add resource endpoints
api.add_resource(Tracking, '/track', '/track/<string:tracking_number>')

# Health check endpoint
@app.route("/health", methods=["GET"])
def health_check():
    return "OK", 200

# Main entry point for local development
if __name__ == "__main__":
    app.run(debug=True)  # This is for local development only