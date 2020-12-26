from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)        #creating object 
#references this file : __name__

#Setting up DB

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chats.db'

db = SQLAlchemy(app)

#MVC: Model(structure) - View - Controller

#We have to define classes, each class variable is considered as a piece of data in the database

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.Text, nullable = False)
    date_sent = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self): #It prints out whenever a new chat is created
        return 'Chat ' + str(self.id)


#Dummy Data

# all_chats = [
#     {
#         'content': 'Hai there!'
#     },
#     {
#         'content': 'Hello, who are you?'
#     },
#     {
#         'content': 'I am a chatbot'
#     },
#     {
#         'content': 'What can you do?'
#     },
#     {
#         'content': 'For now, I can tell you a quote'
#     },
#     {
#         'content': 'Thank you so much'
#     },
#     {
#         'content': 'You are welcome'
#     },
#     {
#         'content': 'bye'
#     },
#     {
#         'content': 'bye'
#     }
# ]





@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chats', methods = ['GET', 'POST'])
def chats():
    # Just before like rendering the template, we are retrieving the data entered by the user in the form and we are storing it in the database
    if request.method == 'POST':
        chat_content = request.form['content']
        new_chat = Chat(content = chat_content)
        db.session.add(new_chat)    #only for current session
        db.session.commit()     #permanent
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
        



        

        return redirect('/chats')
    else:
        all_chats = Chat.query.order_by(Chat.date_sent).all()
        return render_template('chats.html', chats = all_chats)     #we are like sending some data through a variable called chats in the form of list of dictionaries. We can access this data in chats.html


@app.route('/chats/delete/<int:id>')    #when we get to this url, then we get the chat id and delete it from db and redirect to /chats route 
def delete(id):
    chat = Chat.query.get_or_404(id)
    db.session.delete(chat)
    db.session.commit()
    return redirect('/chats')

@app.route('/chats/edit/<int:id>', methods = ['GET', 'POST'])       #when we get to this url, then we get the chat id and update it from db and redirect to /chats route 
def edit(id):
    chat = Chat.query.get_or_404(id)
    if request.method == 'POST':
        chat.content = request.form['content']
        db.session.commit()
        return redirect('/chats')
    else:
        return render_template('edit.html', chat = chat)

#GET to get data  from a specified resource
#POST to send data to a server to create/update a resource


if __name__ == "__main__":
    app.run(debug = True)
