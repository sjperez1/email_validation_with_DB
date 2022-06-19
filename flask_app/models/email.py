from flask_app import DATABASE
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Email:
    def __init__(self, data):
        self.id = data['id']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, data):
        query = "INSERT INTO emails(email) "
        query += "VALUES(%(email)s);"

        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def get_all_emails(cls):
        query = "SELECT * FROM emails ORDER BY created_at DESC;"
        result = connectToMySQL(DATABASE).query_db(query)
        print(result)
        if result:
            all_emails = []
            for one_email in result:
                all_emails.append(cls(one_email))
            return all_emails
        return []

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM emails "
        query += "WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)


    @staticmethod
    def validate_email(data):
        is_valid = True
        query = "SELECT * FROM emails WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if len(results) >= 1:
            flash("This email has already been submitted. Try again.", "error_email_duplicate")
            is_valid=False
        if not EMAIL_REGEX.match(data['email']): 
            flash("Email is not valid!", "error_email")
            is_valid = False
        return is_valid