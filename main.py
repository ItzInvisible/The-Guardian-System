import time
from classes import enforcement, suspect, droneid, drone_status
from map import create_city, display_grid, crime_details

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


def set_all_drones_online():
    # Set every drone in the system to online.
    for code in drone_status:
        drone_status[code] = 'online'
    print("All drones are now set to online.")


def dispatch_drone(city_grid):
    # Ask user which drone to send to a crime location.
    list_drones()
    drone_input = input("Enter Drone ID to send to crime location: ").strip()
    
    if drone_input not in drone_status:
        print("Invalid Drone ID. Please try again.")
        return None
    
    check_status()
    if drone_status[drone_input] == 'offline':
        print(f"{drone_input} is currently offline. Please choose an online drone.")
        return None
    
    # Ask for location
    row = int(input("Enter crime row coordinate: "))
    col = int(input("Enter crime column coordinate: "))
    
    # Check what crime is at that location
    if (row, col) in crime_details:
        crime_info = crime_details[(row, col)]
        crime_type = crime_info['type']
        assigned_drone = crime_info['drone']
        print(f"Crime at ({row},{col}): {crime_type}")
        print(f"Assigned drone: {assigned_drone}")
        confirm = input("Send this drone anyway? (y/n): ").lower()
        if confirm == 'y':
            print(f"{drone_input} dispatched to ({row}, {col}) for {crime_type}.")
            drone_status[drone_input] = 'patrol'
            return (row, col)
        else:
            return None
    else:
        print("No crime reported at that location.")
        return None


def dispatch_enforcement(city_grid):
    # Ask user which enforcement officer to send to a location.
    print("Enforcement officers:")
    for label, name in enforcement.items():
        print(f"  {label}: {name}")
    
    enforce_id = input("Enter Enforcement ID to send to location: ").strip()
    if enforce_id not in enforcement:
        print("Invalid Enforcement ID. Please try again.")
        return None
    
    row = int(input("Enter row coordinate: "))
    col = int(input("Enter column coordinate: "))
    
    print(f"{enforcement[enforce_id]} dispatched to ({row}, {col}).")
    return (row, col)


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
    print("6. Set all drones online")
    print("7. View City Map")
    print("8. Exit")
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
            print("Checking status of all drones...")
            time.sleep(1)
            check_status()
        elif choice == '6':
            set_all_drones_online()
        elif choice == '7':
            print("Displaying city map...")
            time.sleep(1)
            print("-----------------------------------------")
            display_grid(city_grid, (0, 0))
            print("-----------------------------------------")
            
            service_choice = input("Would you like to send a drone or enforcement? (drone/enforcement/quit): ").strip().lower()
            if service_choice == 'drone':
                dispatch_drone(city_grid)
            elif service_choice == 'enforcement':
                dispatch_enforcement(city_grid)
            
            print("Returning to menu...")
            time.sleep(1)
        elif choice == '8':
            print("Exiting Guardian System. Goodbye.")
            break
        else:
            print("Invalid selection. Please choose a number from 1 to 7.")


if __name__ == '__main__':
    main()


