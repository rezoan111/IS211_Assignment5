# IS211 Assignment 5
# This program will simulate network requests

# Request class
# This class will store one request from the csv file
# It will save request time
# It will save file path
# It will save processing time

class Request:
    # This will save one request data
    def __init__(self, time, file_path, process_time):
        self.time = time
        self.file_path = file_path
        self.process_time = process_time
      
# Server class
# This class will handle current request and time left

# One server simulation
# This part will read the csv file
# This part will put requests in one queue
# This part will calculate average wait time

# Many servers simulation
# This part will use more than one server
# Requests will go to servers in round robin order
# This part will also calculate average wait time

# Main function
# This part will read --file
# This part will also read --servers if given
# If no --servers then run one server simulation
# If --servers is given then run many servers simulation
