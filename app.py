from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sent_email import send_email

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:postgres123@localhost/datacollector'
db=SQLAlchemy(app)

class Data(db.Model):
    __tablename__ = "data"
    id=db.Column(db.Integer, primary_key=True)
    email_=db.Column(db.String(120), unique=True)
    height_=db.Column(db.Integer)

    def __init__(self, email_, height_):
        self.email_ = email_
        self.height_ = height_


@app.route("/") #decorator
def index():
    return render_template("index.html")

@app.route("/success", methods=['POST'])
def success():
    if request.method == 'POST':
        email=request.form['user_email']
        height=request.form['user_height']
        # send_email(email,height)
        print(request.form)
        if db.session.query(Data).filter(Data.email_==email).count() == 0:
            data = Data(email, height)
            db.session.add(data)
            db.session.commit()
            return render_template("success.html")
        else:
            return render_template("index.html",
             text="Seems like we've got something from that email already.")

if __name__=="__main__":
    app.debug=True
    app.run()