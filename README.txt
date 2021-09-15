Credit Transactions.

This module is intended to create a summary containing monthly and overall information. Once the summary is created, 
it is sent to an addressee via e-mail with a Gmail account, and the information is stored in a DynamoDB table.

Set Up.
The following steps describe the requirements so that this module is implemented correctly.
- Create a Table in DynamoDB.
    Set 'Id' [str] as the primary key.
- Create a Bucket, and a Folder in which a csv file is to be uploaded containing the transactions information in the
    following columns: 
        Id [int] -> unique operation identifier.
        Date [str] -> (m/dd) date of operation.
        Transaction [str] -> indicate with a (+) sign if the operation is a Credit transaction, else indicate with a 
        (-) sign a Debit transaction.
- Create an AWS Lambda with Python 3.8 runtime.
- Add the following Layer as ARN: 
    arn:aws:lambda:us-east-2:629941798500:function:TransactionsService
- Add the following permissions to the AWS Lambda:
    AmazonSQSFullAccess
    AmazonS3FullAccess
    AmazonDynamoDBFullAccess
    AmazonSESFullAccess
- Create a SQS queue.
    Modify the access policy so that the Statement contains the following entry:
        "Statement": [
            {
            "Sid": "__owner_statement",
            "Effect": "Allow",
            "Principal": {
                "AWS": "*"
            },
            "Action": "SQS:*",
            "Resource": "arn:aws:sqs:us-east-2:629941798500:transactionsQUEUE"
            }
        ]
    In lambda triggers add the url of the aws lambda you just created.   
- Add the following environment variables to the AWS Lambda:
    BUCKET -> Location for the transaction csv files.
    FOLDER -> Location for the transaction csv files.
    LOGLEVEL -> Logger level to write in CloudWatch.
    QUEUE -> URL of the SQS which triggers the lambda.
    SENDER -> email of the sender.
    TABLE -> Name of the DynamoDB table to store the information.
- Give permissions to the sender's gmail account.
    allow less secure apps to use your account with the followinf link
    https://myaccount.google.com/lesssecureapps
- Give S3 Bucket permissions to create a SQS message.
    Go to the S3 Bucket where the transaction files are to be stored.
    Go to properties and allow Event notifications. As prefix set the FOLDER name. In Event Types select 'All object create events'. 
    As Destination select SQS queue, and select the one you created above.


Once the AWS infrastructure is set up, the data flow will run authomatically every time a new file is inserted into the Bucket/Folder/
stated above.