import json
import boto3

# DynamoDB Client
client = boto3.client('dynamodb')


def lambda_handler(event, context):
    try:
        http_method = event.get('httpMethod')
        query_string = event.get('queryStringParameters')
        body = event.get('body')

        return page_router(http_method, query_string, body)

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET,POST,DELETE,OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            'body': json.dumps({'error': str(e)})
        }


def page_router(httpmethod, querystring, formbody):

    # Handle CORS Preflight Request
    if httpmethod == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET,POST,DELETE,OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": ""
        }

    # GET - Return Home Page
    elif httpmethod == "GET":
        try:
            with open("index.html", "r") as htmlFile:
                htmlContent = htmlFile.read()

            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "text/html",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": htmlContent
            }

        except Exception as e:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": str(e)})
            }

    # POST - Insert Record
    elif httpmethod == "POST":
        try:
            insert_record(formbody)

            with open("success.html", "r") as htmlFile:
                htmlContent = htmlFile.read()

            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "text/html",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": htmlContent
            }

        except Exception as e:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": str(e)})
            }

    # DELETE - Delete Record by Email
    elif httpmethod == "DELETE":
        try:

            if querystring is None or "email" not in querystring:
                return {
                    "statusCode": 400,
                    "body": json.dumps({
                        "message": "Please provide email query parameter"
                    })
                }

            email = querystring["email"]

            delete_record(email)

            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({
                    "message": "Record deleted successfully"
                })
            }

        except Exception as e:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": str(e)})
            }

    else:
        return {
            "statusCode": 405,
            "body": json.dumps({
                "message": "Method Not Allowed"
            })
        }


# -----------------------
# Insert Record
# -----------------------
def insert_record(formbody):

    formbody = formbody.replace("=", "' : '")
    formbody = formbody.replace("&", "', '")

    statement = "INSERT INTO veera VALUE {'" + formbody + "'}"

    response = client.execute_statement(
        Statement=statement
    )

    return response


# -----------------------
# Delete Record
# -----------------------
def delete_record(email):

    statement = f"DELETE FROM veera WHERE email = '{email}'"

    response = client.execute_statement(
        Statement=statement
    )

    return response
