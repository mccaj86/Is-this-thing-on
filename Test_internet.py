#!/usr/bin/env python

'''
Test_internet.py: A program see if the internet is accessible.
Adapted from https://stackoverflow.com/questions/20913411/test-if-an-internet-connection-is-present-in-python
A. J. McCulloch, March 2019
'''

####################################################################################################
# Import modules
####################################################################################################

import time # Module to retrieve system time
import datetime # Module to handle timestamp manipulation
import socket # Import network interface
import os.path # Module for file verification
import schedule # Module to handle scheduling
from pytz import timezone # Module to handle local timezone

####################################################################################################
# Define functions
####################################################################################################

# Function will return a True/False for external connection
def is_connected(hostname):
  try:
    # see if we can resolve the host name -- tells us if there is
    # a DNS listening
    host = socket.gethostbyname(hostname)
    # connect to the host -- tells us if the host is actually
    # reachable
    s = socket.create_connection((host, 80), 2)
    return True
  except:
     pass
  return False

# Function to write the speed test results (a dictionary) to a .csv file
def writetxt(string, file = 'connectionlog.txt'):
    # Check if the file exists
    file_exists = os.path.isfile(file)
    # Open the file in append mode
    with open(file, 'a') as f:
        if not file_exists:
            # Make a header for the csv
            f.write("Time stamp, connected\n")
        f.write(string)

# Runner function to test the connection to a given server, and write a text file with timestamps from location
def test_connection(REMOTE_SERVER = "www.google.com", location = ['Australia/Melbourne']):
    # Test the connection and timestamp
    result = datetime.datetime.now(timezone(*location)).strftime('%Y-%m-%d %H:%M:%S') + ', ' + str(is_connected(REMOTE_SERVER)) + '\n'
    # Write the result
    writetxt(result)

####################################################################################################
####################################################################################################
# Code starts here
####################################################################################################
####################################################################################################

# Set the schedule for performing a speed test
schedule.every(1).minutes.do(test_connection)

'''
Note scheduler does not account for the time it takes to run the script!
'''

# Execute the program
while True:
    # Verify if a task is pending (it should be!)
    schedule.run_pending()
    # Don't do anything for a second
    time.sleep(1)
