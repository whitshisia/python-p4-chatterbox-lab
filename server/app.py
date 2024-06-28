from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=["GET", "POST"])
def messages():
    if request.method == "GET":
        for message in Message.query.order_by(Message.created_at.asc).all():
            message_dict = [message.to_dict() for message in message.messages]
            return make_response(jsonify(message_dict), 200)
    elif request.method == "POST":
         data = request.get_json()
         body = data.get("body")
         username = data.get("username")
         
         if not body or not username:
             return make_response({"error": "Missing required fields"}, 400)
         
         message = Message(body=body, username=username)
         db.session.add(message)
         db.session.commit()
         
         return make_response(jsonify(message.to_dict()), 201)

@app.route('/messages/<int:id>', methods =["DELETE", "PATCH"])
def messages_by_id(id):
    if request.method == "DELETE":
        message = Message.query.get_or_404(id)
        db.session.delete(message)
        db.session.commit()
        
        return make_response({"message":"Message succefully deleted"})
    elif request.method == "PATCH":
         message = Message.query.get_or_404(id)
         data = request.get_json()
         body = data.get('body')
         
         if body:
             message.body = body
             db.session.commit()
             
         return make_response(jsonify(message.to_dict()), 200)    
        
if __name__ == '__main__':
    app.run(port=5555)
