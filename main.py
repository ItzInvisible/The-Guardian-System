import math
from classes import enforcement, suspect, droneid, drone_status
import time

import classes 

def status(drone_input):
    if drone_input in drone_status:
        print(f"{drone_input} is {drone_status[drone_input]}.")
        change = input("Do you want to change the status? (y/n): ").lower()
        if change == 'y':
            new_status = input("Enter new status (online/offline): ").lower()
            if new_status in ['online', 'offline']:
                drone_status[drone_input] = new_status
                print(f"Status updated to {new_status}.")
            else:
                print("Invalid status. Must be 'online' or 'offline'.")
    else:
        print("Invalid Drone ID. Please try again.")


droneid_input = input("Enter Drone ID for Status Check:")
print(droneid)
time.sleep(1)
print("Checking status of drones...")
time.sleep(2)
status(droneid_input)