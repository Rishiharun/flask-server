import boto3

import key_config as keys


dynamodb_client = boto3.client(
    'dynamodb',
    aws_access_key_id     = keys.ACCESS_KEY_ID,
    aws_secret_access_key = keys.ACCESS_SECRET_KEY,
    region_name           = keys.REGION_NAME,
)
dynamodb_resource = boto3.resource(
    'dynamodb',
    aws_access_key_id     = keys.ACCESS_KEY_ID,
    aws_secret_access_key = keys.ACCESS_SECRET_KEY,
    region_name           = keys.REGION_NAME,
)

def create_user_table():
    
   table = dynamodb_resource.create_table(
       TableName = 'users', # Name of the table
       KeySchema = [
           {
               'AttributeName': 'email',
               'KeyType'      : 'HASH' #RANGE = sort key, HASH = partition key
           }
       ],
       AttributeDefinitions = [
           {
               'AttributeName': 'email', # Name of the attribute
               'AttributeType': 'S'   # N = Number (B= Binary, S = String)
           }
       ],
       ProvisionedThroughput={
           'ReadCapacityUnits'  : 10,
           'WriteCapacityUnits': 10
       }
   )
   return table


user = dynamodb_resource.Table("users")

     
def add_item_to_user_table(fullname, registration_number, email, password, degree, contact, introduction, GPA, skills):
    
    response = user.put_item(
        Item={
             'fullname' : fullname,
             'registration_number' : registration_number,
             'email' : email,
             'password' : password,
             'degree' : degree,
             'contact' : contact,
             'introduction' : introduction,
             'GPA' : GPA,
             'skills' : skills
        }
    )
    return response
    
    
def update_user_profile(email,data:dict):
    
    response = user.update_item(
        
        Key = {
           'email': email
        },
        AttributeUpdates={
            
            'fullname': {
               'Value'  : data['fullname'],
               'Action' : 'PUT' 
            },
            'registration_number': {
               'Value'  : data['registration_number'],
               'Action' : 'PUT'
            },
            'password': {
               'Value'  : data['password'],
               'Action' : 'PUT'
            },
            'degree': {
               'Value'  : data['degree'],
               'Action' : 'PUT'
            },
            'contact': {
               'Value'  : data['contact'],
               'Action' : 'PUT'
            },
            'introduction': {
               'Value'  : data['introduction'],
               'Action' : 'PUT'
            },
            'GPA': {
               'Value'  : data['GPA'],
               'Action' : 'PUT'
            },
            'skills': {
               'Value'  : data['skills'],
               'Action' : 'PUT'
            },
            
        },
        
        ReturnValues = "UPDATED_NEW"  # returns the new updated values
    )
    
    return response
    
    
def get_user_profile(registration_number):
    
    response = user.scan(
        FilterExpression=f'registration_number = :registration_number',
        ExpressionAttributeValues={':registration_number': registration_number}
    )
    item = response["Items"][0]
    return item

    

  
  
  