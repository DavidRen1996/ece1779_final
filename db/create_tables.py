import boto3
from db.constants import *

client = boto3.client('dynamodb')
dynamodb = boto3.resource('dynamodb')

def create_tables():
    # Get the service resource.
    existing_tables = client.list_tables()['TableNames']

    # Create the DynamoDB table.
    if PUBLIC_USER_INFO not in existing_tables:
        table = dynamodb.create_table(
            TableName=PUBLIC_USER_INFO,
            KeySchema=[
                {
                    'AttributeName': USERNAME,
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': USERNAME,
                    'AttributeType': 'S'
                }
            ],
            BillingMode='PAY_PER_REQUEST',
        )

        # Wait until the table exists.
        table.meta.client.get_waiter('table_exists').wait(TableName=PUBLIC_USER_INFO)
        print('table created with rows ' + str(table.item_count))
    else:
        print(PUBLIC_USER_INFO + " table already exists")

    # Create the DynamoDB table.
    if PRIVATE_USER_INFO not in existing_tables:
        table = dynamodb.create_table(
            TableName=PRIVATE_USER_INFO,
            KeySchema=[
                {
                    'AttributeName': USERNAME,
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': USERNAME,
                    'AttributeType': 'S'
                },
            ],
            BillingMode='PAY_PER_REQUEST',
        )

        # Wait until the table exists.
        table.meta.client.get_waiter('table_exists').wait(TableName=PRIVATE_USER_INFO)
        print('table created with rows ' + str(table.item_count))
    else:
        print(PRIVATE_USER_INFO + " table already exists")

    # Create the DynamoDB table.
    if PHOTO_INFO not in existing_tables:
        table = dynamodb.create_table(
            TableName=PHOTO_INFO,
            KeySchema=[
                {
                    'AttributeName': USERNAME,
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': PHOTO_LOCATION,
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': USERNAME,
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': PHOTO_LOCATION,
                    'AttributeType': 'S'
                }
            ],
            BillingMode='PAY_PER_REQUEST',
        )
        # Wait until the table exists.
        table.meta.client.get_waiter('table_exists').wait(TableName=PHOTO_INFO)
        print('table created with rows ' + str(table.item_count))
    else:
        print(PHOTO_INFO + " table already exists")

    # Create the DynamoDB table.
    if USER_LOCATION not in existing_tables:
        table = dynamodb.create_table(
            TableName=USER_LOCATION,
            KeySchema=[
                {
                    'AttributeName': USERNAME,
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': GENDER_AND_INTEREST,
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': USERNAME,
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': GENDER_AND_INTEREST,
                    'AttributeType': 'N'
                }
            ],
            BillingMode='PAY_PER_REQUEST',
        )
        # Wait until the table exists.
        table.meta.client.get_waiter('table_exists').wait(TableName=USER_LOCATION)
        print('table created with rows ' + str(table.item_count))
    else:
        print(USER_LOCATION + " table already exists")


create_tables()
