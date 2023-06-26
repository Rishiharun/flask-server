from flask import Flask, render_template, request
import boto3
import key_config as keys
import dynamodb_handler
import json
from boto3.dynamodb.conditions import Key, Attr

app = Flask(__name__)

dynamodb = boto3.resource(
    'dynamodb',
    #aws_access_key_id     = keys.ACCESS_KEY_ID,
    #aws_secret_access_key = keys.ACCESS_SECRET_KEY,
    region_name = keys.REGION_NAME,
)

@app.route('/')
def index():
    #dynamodb_handler.create_user_table()
    #return 'Table Created'
    return render_template('sign-in.html')

@app.route('/login')
def login():
    return render_template("login.html")
    

@app.route('/redirect')
def redirect():
    return render_template("sign-in.html")
    
    
@app.route('/signup', methods=['post'])
def signup():
    
    user_data = request.form.to_dict()
    
    dynamodb_handler.add_item_to_user_table(user_data['fullname'], int(user_data['registration_number']), user_data['email'], user_data['password'], user_data['degree'], (user_data['contact']), user_data['introduction'], user_data['gpa'], user_data['skills'])

    return  render_template("login.html")


@app.route('/check', methods=['post'])
def check():
    email = request.form["email"]
    login_password = request.form["password"]
    
    table = dynamodb.Table('users')
    
    response = table.query(
        KeyConditionExpression=Key("email").eq(email)
    )
    
    items = response['Items']
    
    fullname = items[0]['fullname']
    registration_number = items[0]['registration_number']
    password = items[0]['password']
    degree = items[0]['degree']
    contact = items[0]['contact']
    introduction = items[0]['introduction']
    gpa = items[0]['GPA']
    skills = items[0]['skills']
    
    
    if login_password == password:
        return render_template('update.html', email=email, password=password, fullname=fullname, registration_number=registration_number, 
        degree=degree, contact=contact, introduction=introduction, gpa=gpa, skills=skills)
        
        
@app.route('/update/<string:email>', methods=['PUT'])
def update_profile(email):
    data = request.get_json()
    
    response = dynamodb_handler.update_user_profile(email,data)
    
    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        return {
            'msg'                : 'Updated successfully',
            'ModifiedAttributes' : response['Attributes'],
            'response'           : response['ResponseMetadata']
        }

    return {
        'msg'      : 'Some error occured',
        'response' : response
    }
    
    
@app.route('/view/<int:registration_number>', methods=['GET'])
def public_profile_view(registration_number):
    profile = dynamodb_handler.get_user_profile(registration_number)
    
    fullname = profile["fullname"]
    email = profile["email"]
    registration_number = profile["registration_number"]
    degree = profile["degree"]
    contact = profile["contact"]
    introduction = profile["introduction"]
    GPA = profile["GPA"]
    skills = profile["skills"]
        
    return render_template("view.html", fullname=fullname, email=email, registration_number=registration_number, degree=degree, contact=contact, introduction=introduction, GPA=GPA, skills=skills)

        

if __name__ == '__main__':
    app.run(debug=True,port=8080,host="0.0.0.0")
    
    
    