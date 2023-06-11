# Import libraries needed for the code to run.
import boto3
from datetime import datetime

# Get the current date
today = datetime.today()

# Format the current date as YYYYMMDD
todays_date = today.strftime("%Y%m%d")


def lambda_handler(event, context):

    # Create an S3 client
    s3_client = boto3.client('s3')

    # Specify the bucket name
    bucket_name = "jordancampbell-organize-s3-objects"

    # Retrieve the list of objects in the bucket
    list_objects_response = s3_client.list_objects_v2(Bucket = bucket_name)

    # Extract the contents from the response
    get_contents = list_objects_response.get("Contents")

    # Create a list to store all the S3 object and folder names
    get_all_s3_object_and_folder_names = []

    # Iterate over the objects in the bucket and retrieve their names
    for item in get_contents:
        s3_object_name = item.get("Key")

        get_all_s3_object_and_folder_names.append(s3_object_name)

    # Create a directory name using the current date
    directory_name = todays_date + "/"

    # Check if the directory already exists in the list of object and folder names
    # If it doesn't exist, create the directory in the bucket
    if directory_name not in get_all_s3_object_and_folder_names:
        s3_client.put_object(Bucket=bucket_name, Key=(directory_name))

    # Iterate over the objects in the bucket again
    for item in get_contents:
        # Get the creation date of the object and format it as YYYYMMDD
        object_creation_date = item.get("LastModified").strftime("%Y%m%d") + "/"
        # Get the name of the object
        object_name = item.get("Key")

        # If the object's creation date matches the current date directory
        # and it is not already in a subdirectory, copy it to the current date directory
        # and delete the original object
        if object_creation_date == directory_name and "/" not in object_name:
            s3_client.copy_object(Bucket=bucket_name, CopySource=bucket_name+"/"+object_name, Key=directory_name+object_name)
            s3_client.delete_object(Bucket=bucket_name, Key=object_name)