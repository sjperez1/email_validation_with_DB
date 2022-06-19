# session would be added to the end of the following line if we were using it in this file
from flask import render_template, redirect, request, flash
from flask_app import app
# import the class from corresponding model
from flask_app.models.email import Email


@app.route("/")
def display_create_email():
    return render_template("index.html")

@app.route("/", methods = ['POST'])
def create_email():
    if not Email.validate_email(request.form):
        return redirect('/')

    Email.create(request.form)
    return redirect("/success")

@app.route("/success")
def display_emails():
    
    return render_template("success.html", all_emails = Email.get_all_emails())

@app.route("/delete/<int:id>")
def delete_email(id):
    data = {
        "id" : id
    }
    Email.delete(data)
    return redirect("/success")