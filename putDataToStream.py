#!/bin/python
import argparse
import logging
import os.path
import boto3
import glob
import json
import random
import calendar
import time
import re
import sys
from datetime import datetime
import psycopg2
from psycopg2.extras import LogicalReplicationConnection

##########################################
# Replace multiple values from a string  #
##########################################

def replaceMultiple(mainString, toBeReplaces, newString):
    # Iterate over the strings to be replaced
    for elem in toBeReplaces:
        # Check if string is in the main string
        if elem in mainString:
            # Replace the string
            mainString = mainString.replace(elem, newString)

    return mainString

##########################################
# Read value of args to analyse log file #
# based on insert/update/delete          #
##########################################

def putData(region,aws_access_key,aws_secret_key,aws_session_token,log_file):
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y %H:%M:%S")

    print('LOG FILE : '+log_file)


##########################################
# create connection to kinesis client    #
##########################################

    my_stream_name = 'collector'
    kinesis_client = boto3.client(
                   'kinesis', region_name=region, aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key,aws_session_token=aws_session_token)

##########################################
# Read recent downloaded log file        #
# Folder Structure :                     #
# Configure the payload/json dump for S3 #
##########################################

    init = open(log_file, "r")
    for line in init:
        if any(re.findall(r'insert', line, re.IGNORECASE)):
           print(line)
           #INSERT INTO account (user_id, username) VALUES (101, 'Shubhankar');#
           payload={
                       line
                   }
           print(payload)

           try:
                response=kinesis_client.put_record(StreamName=my_stream_name, Data=json.dumps(payload), PartitionKey="default")
                logging.info(response)
           except Exception:
                logging.exception('Failed pushing data to firehose stream')
