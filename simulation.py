import argparse
import csv
from collections import deque

# IS211 Assignment 5
# This program will simulate network requests


# Request class
# This class will store one request from the csv file
class Request:
    def __init__(self, time, file_path, process_time):
        self.time = time
        self.file_path = file_path
        self.process_time = process_time


# Server class
# This class will handle current request and time left
class Server:
    def __init__(self):
        self.current_request = None
        self.time_left = 0

    def is_busy(self):
        return self.current_request is not None

    def start_next_request(self, request):
        self.current_request = request
        self.time_left = request.process_time

    def process_one_second(self):
        if self.is_busy():
            self.time_left -= 1

            if self.time_left == 0:
                self.current_request = None


# This part will read the csv file
def load_requests(filename):
    requests = []

    with open(filename, "r", newline="") as file:
        reader = csv.reader(file)

        for row in reader:
            if not row:
                continue

            time = int(row[0].strip())
            file_path = row[1].strip()
            process_time = int(row[2].strip())

            request = Request(time, file_path, process_time)
            requests.append(request)

    requests.sort(key=lambda x: x.time)
    return requests


# This part will run the simulation
def run_simulation(requests, server_count):
    if not requests:
        return 0.0

    servers = []
    queues = []

    for i in range(server_count):
        servers.append(Server())
        queues.append(deque())

    wait_times = []
    current_time = 0
    request_index = 0
    next_server = 0

    while (
        request_index < len(requests)
        or any(queue for queue in queues)
        or any(server.is_busy() for server in servers)
    ):

        # Add requests that arrive at this time
        while request_index < len(requests) and requests[request_index].time == current_time:
            queues[next_server].append(requests[request_index])
            next_server = (next_server + 1) % server_count
            request_index += 1

        # Start next request if server is free
        for i in range(server_count):
            if not servers[i].is_busy() and queues[i]:
                next_request = queues[i].popleft()
                wait_time = current_time - next_request.time
                wait_times.append(wait_time)
                servers[i].start_next_request(next_request)

        # Process one second
        for server in servers:
            server.process_one_second()

        current_time += 1

    average_wait = sum(wait_times) / len(wait_times)
    return average_wait


# One server simulation
def simulateOneServer(filename):
    requests = load_requests(filename)
    average_wait = run_simulation(requests, 1)
    print("Average wait time: {:.2f}".format(average_wait))
    return average_wait


# Many servers simulation
def simulateManyServers(filename, servers):
    requests = load_requests(filename)
    average_wait = run_simulation(requests, servers)
    print("Average wait time: {:.2f}".format(average_wait))
    return average_wait


# Main function
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    parser.add_argument("--servers", type=int)

    args = parser.parse_args()

    if args.servers is not None and args.servers < 1:
        parser.error("--servers must be 1 or more")

    if args.servers is None:
        simulateOneServer(args.file)
    else:
        simulateManyServers(args.file, args.servers)


if __name__ == "__main__":
    main()
