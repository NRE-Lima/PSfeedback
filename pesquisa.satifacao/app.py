from flask import Flask, request, jsonify
from flask_mail import Mail, Message
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="satisfaction_db"
)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'pesquisasatisfacao75@gmail.com'
app.config['MAIL_PASSWORD'] = 'PS123456'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

@app.route('/submit_survey', methods=['POST'])
def submit_survey():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    rating = data.get('rating')
    comments = data.get('comments')

    cursor = db.cursor()
    query = "INSERT INTO surveys (name, email, rating, comments) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (name, email, rating, comments))
    db.commit()

    msg = Message('Pesquisa de Satisfação', sender='andreluiz.jg54@gmail.com', recipients=[email])
    msg.body = f"Obrigado por enviar seu feedback, {name}!\n\nSua avaliação: {rating}\nComentários: {comments}"
    mail.send(msg)

    return jsonify({"message": "Feedback enviado com sucesso!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
