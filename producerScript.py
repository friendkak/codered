#!/bin/python
import boto3
import json
import random
import calendar
import time
import sys
from datetime import datetime
import psycopg2
from psycopg2.extras import LogicalReplicationConnection

############################################
# Specify inputs that to be taken care     #
############################################


user_id = sys.argv[1]
username = sys.argv[2]

############################################
# Connect to database usinf db credentals  #
############################################

my_connection  = psycopg2.connect(
                   database='testdb',
                   user='shubhankar',
                   password='shubhankar',
                   host='shubhankar.abcdefgg59e.us-east-1.rds.amazonaws.com',
                   port=5432)
cur = my_connection.cursor()

############################################
# Execute statements based on input        #
############################################

cur.execute("INSERT INTO account (user_id, username) VALUES ('"+ user_id + "','" +username+"' );")
cur.execute("COMMIT")
