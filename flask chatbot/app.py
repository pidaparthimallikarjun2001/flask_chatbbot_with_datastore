from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)        

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chats.db'

db = SQLAlchemy(app)


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.Text, nullable = False)
    date_sent = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return 'Chat ' + str(self.id)


#Dummy Data

all_chats = [
    {
        'content': 'Hai there!'
    },
    {
        'content': 'Hello, who are you?'
    },
    {
        'content': 'I am a chatbot'
    },
    {
        'content': 'What can you do?'
    },
    {
        'content': 'For now, I can tell you a quote'
    },
    {
        'content': 'Thank you so much'
    },
    {
        'content': 'You are welcome'
    },
    {
        'content': 'bye'
    },
    {
        'content': 'bye'
    }
]





@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chats', methods = ['GET', 'POST'])
def chats():
    if request.method == 'POST':
        chat_content = request.form['content']
        new_chat = Chat(content = chat_content)
        db.session.add(new_chat)
        db.session.commit()
        # replying to the user accordingly
        if chat_content.lower() == "hello" or chat_content.lower() == "hai":
            botreplytoinput = Chat(content = "Hai, there!")
            db.session.add(botreplytoinput)
            db.session.commit()
        
        elif "who are you" in chat_content.lower():
            botreplytoinput = Chat(content = "I am a chatbot")
            db.session.add(botreplytoinput)
            db.session.commit()

        elif "what can you do" in chat_content.lower():
            botreplytoinput = Chat(content = "I am still being developed. But don't worry, for now, I can tell you a quote to motivate you!")
            db.session.add(botreplytoinput)
            db.session.commit()
        
        elif "quote" in chat_content.lower():
            botreplytoinput = Chat(content = "Effort makes you. You will regret someday if you don’t do your best now. Don’t think it’s too late but keep working on it. It takes time, but there’s nothing that gets worse due to practicing. So practice. You may get depressed, but it’s evidence that you are doing good.")
            db.session.add(botreplytoinput)
            db.session.commit()
        
        elif "thank" in chat_content.lower():
            botreplytoinput = Chat(content = "You're welcome")
            db.session.add(botreplytoinput)
            db.session.commit()

        elif "health" in chat_content.lower():
            botreplytoinput = Chat(content = "Eat a variety of foods. Base your diet on plenty of foods rich in carbohydrates. Replace saturated with unsaturated fat. Enjoy plenty of fruits and vegetables. Reduce salt and sugar intake. Eat regularly, control the portion size. Drink plenty of fluids. Maintain a healthy body weight.")
            db.session.add(botreplytoinput)
            db.session.commit()
        
        else:
            botreplytoinput = Chat(content = "For now, I can only do limited things. Sorry! I am not programmed to do this. Ask me something else")
            db.session.add(botreplytoinput)
            db.session.commit()
        



        

        return redirect('/chats',)
    else:
        all_chats = Chat.query.order_by(Chat.date_sent).all()
        return render_template('chats.html', chats = all_chats)     


@app.route('/chats/delete/<int:id>')
def delete(id):
    chat = Chat.query.get_or_404(id)
    db.session.delete(chat)
    db.session.commit()
    return redirect('/chats')

@app.route('/chats/edit/<int:id>', methods = ['GET', 'POST'])
def edit(id):
    chat = Chat.query.get_or_404(id)
    if request.method == 'POST':
        chat.content = request.form['content']
        db.session.commit()
        return redirect('/chats')
    else:
        return render_template('edit.html', chat = chat)




if __name__ == "__main__":
    app.run(debug = True)