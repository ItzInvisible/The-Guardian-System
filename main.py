import time
from classes import enforcement, suspect, droneid, drone_status
from map import create_city, add_alert, display_grid

# This program is a simple text-based menu for the Guardian System.
# It allows the user to list drones, check or change a drone status,
# and view the known suspects and enforcement officers.

city_grid = create_city()

def status(drone_input):
    # Check whether the entered drone ID exists, then show its current status.
    # The user can optionally update the drone status to online/offline/patrol.
    if drone_input in drone_status:
        print(f"{drone_input} is {drone_status[drone_input]}.")
        change = input("Do you want to change the status? (y/n): ").lower()
        if change == 'y':
            new_status = input("Enter new status (online/offline/patrol): ").lower()
            if new_status in ['online', 'offline', 'patrol']:
                drone_status[drone_input] = new_status
                print(f"Status updated to {new_status}.")
            else:
                print("Invalid status. Must be 'online', 'offline', or 'patrol'.")
    else:
        print("Invalid Drone ID. Please try again.")


def list_drones():
    # Print all available drone labels and their runtime IDs.
    print("Available Drone IDs:")
    for label, code in droneid.items():
        print(f"  {label}: {code}")


def list_suspects():
    # Print the current list of suspects from the classes module.
    print("Known suspects:")
    for label, name in suspect.items():
        print(f"  {label}: {name}")


def list_enforcement():
    # Print the enforcement team members defined in the classes module.
    print("Enforcement officers:")
    for label, name in enforcement.items():
        print(f"  {label}: {name}")
    

def check_status():
    # Show the status for every drone code in the system.
    print("Current drone statuses:")
    for code, status in drone_status.items():
        print(f"  {code}: {status}")


def show_menu():
    # Display the main user menu with numbered options.
    print("-----------------------------------------")
    print("Welcome to the Guardian System")
    print("-----------------------------------------")
    print("\nGuardian System Menu")
    print("1. List drones")
    print("2. Check or change drone status")
    print("3. List suspects")
    print("4. List enforcement officers")
    print("5. Check status of all drones")
    print("6. View City Map")
    print("7. Exit")
    print("-----------------------------------------")


def main():
    # Loop until the user chooses to exit.
    while True:
        show_menu()
        choice = input("Choose an option (1-7): ").strip()

        if choice == '1':
            list_drones()
        elif choice == '2':
            droneid_input = input("Enter Drone ID for Status Check: ").strip()
            print("Checking status of drones...")
            time.sleep(1)
            status(droneid_input)
        elif choice == '3':
            list_suspects()
        elif choice == '4':
            list_enforcement()
            print("Press type 'quit' to return to the menu.")
            if input().lower() == 'quit':
                continue
            print("Returning to menu...")
            time.sleep(1)
        elif choice == '5':
            check_status()
        elif choice == '6':
            print("Displaying city map...")
            time.sleep(1)
            print("-----------------------------------------")
            display_grid(city_grid, (0, 0))  # Example drone position
            print("------------------------------------------")
            print("Press type 'quit' to return to the menu.")
            if input().lower() == 'quit':
                continue
            print("Returning to menu...")
            time.sleep(1)
        elif choice == '7':
            print("Exiting Guardian System. Goodbye.")
            break
        else:
            print("Invalid selection. Please choose a number from 1 to 7.")


if __name__ == '__main__':
    main()


