#!/usr/bin/env python
#
#Import the required components
from __future__ import print_function

import argparse
import os.path
import sys
import putDataToStream
import boto3
from botocore.exceptions import NoRegionError, ClientError
from datetime import datetime

##########################################
# Read argument values from command line #
# and get the date value                 #
##########################################

aws_access_key = sys.argv[1]
aws_secret_key = sys.argv[2]
aws_session_token = sys.argv[3]
now = datetime.now()
dt_string = now.strftime("%Y-%m-%d-%H")

##########################################
# Print the value of aws credentials     #
##########################################
print('AWS KEY : '+aws_access_key)
print('AWS SECRET KEY :'+aws_secret_key)
print('AWS SESSION TOKEN :'+aws_session_token)
print("DATE :",dt_string)

##########################################
# Configure values as per region/instance#
# /log file location                     #
##########################################

region = 'us-east-1'
rds_instance = 'shubhankar'
log_file = 'error/postgresql.log.'+dt_string
local_log_file = '/home/codered/log/'+log_file

##########################################
# Create the file where log will be      #
# written                                #
##########################################


if local_log_file:
    print ('Local log file exists..')
else:
    print ('Creating file local log file..')
    open(local_log_file,"w+")

try:
    rds = boto3.client('rds', region, aws_access_key_id = aws_access_key, aws_secret_access_key = aws_secret_key, aws_session_token = aws_session_token)
except NoRegionError:
    rds = boto3.client('rds', region, aws_access_key_id = aws_access_key, aws_secret_access_key = aws_secret_key, aws_session_token = aws_session_token)


with open(local_log_file, 'w') as f:
    print('downloading {rds} log file {file}'.format(rds=rds_instance, file=log_file))
    token = '0'
    try:
        response = rds.download_db_log_file_portion(
            DBInstanceIdentifier=rds_instance,
            LogFileName=log_file,
            Marker=token)
        while response['AdditionalDataPending']:
            f.write(response['LogFileData'])
            token=response['Marker']
            response = rds.download_db_log_file_portion(
                DBInstanceIdentifier=rds_instance,
                LogFileName=log_file,
                Marker=token)
        f.write(response['LogFileData'])
    except ClientError as e:
        print(e)
        sys.exit(2)

###########################################
# Trigger another script to put data      #
# to kinesis stream                       #
###########################################

putDataToStream.putData(region, aws_access_key, aws_secret_key, aws_session_token, "/home/codered/log/"+log_file)
