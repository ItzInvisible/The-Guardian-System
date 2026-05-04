"""
Guardian System Main Program

This is the main entry point for the Guardian System, a text-based simulation
for managing drones, enforcement officers, and responding to city crimes.

Features:
- List and manage drone statuses
- View suspects and enforcement officers
- Display a randomized city map with crime incidents
- Dispatch drones and enforcement to crime locations
- Crimes require both drone and enforcement response before resolution

Modules used:
- classes.py: Contains data for drones, suspects, and enforcement
- map.py: Handles city grid creation and display with crime tracking
"""

import time  # For adding delays in the menu for better UX

import map  # Import map module to access crime_details dynamically
from classes import (  # Import shared data structures
    drone_status,
    droneid,
    enforcement,
    suspect,
)
from map import create_city, display_grid  # Import map functions

# Global city grid created at startup
city_grid = create_city()


def status(drone_input):
    """
    Check and optionally update the status of a specific drone.

    Args:
        drone_input (str): The drone ID to check (e.g., 'DRN1A')

    Displays current status and prompts for status change if requested.
    Valid statuses: 'online', 'offline', 'patrol'
    """
    # Check whether the entered drone ID exists, then show its current status.
    # The user can optionally update the drone status to online/offline/patrol.
    if drone_input in drone_status:
        print(f"{drone_input} is {drone_status[drone_input]}.")
        change = input("Do you want to change the status? (y/n): ").lower()
        if change == "y":
            new_status = input("Enter new status (online/offline/patrol): ").lower()
            if new_status in ["online", "offline", "patrol"]:
                drone_status[drone_input] = new_status
                print(f"Status updated to {new_status}.")
            else:
                print("Invalid status. Must be 'online', 'offline', or 'patrol'.")
    else:
        print("Invalid Drone ID. Please try again.")


def list_drones():
    """
    Display all available drones with their labels and IDs.

    Prints a list of drone labels (e.g., 'Drone 1A') and their corresponding
    runtime IDs (e.g., 'DRN1A') from the droneid dictionary.
    """
    # Print all available drone labels and their runtime IDs.
    print("Available Drone IDs:")
    for label, code in droneid.items():
        print(f"  {label}: {code}")


def list_suspects():
    """
    Display the list of known suspects.

    Prints all suspects from the suspect dictionary, showing labels
    (e.g., 'Suspect 1') and names (e.g., 'Giovanni').
    """
    # Print the current list of suspects from the classes module.
    print("Known suspects:")
    for label, name in suspect.items():
        print(f"  {label}: {name}")


def list_enforcement():
    """
    Display the list of enforcement officers.

    Prints all enforcement officers from the enforcement dictionary,
    showing IDs (e.g., 'ENFORCE1') and names (e.g., 'Officer Stevenson').
    """
    # Print the enforcement team members defined in the classes module.
    print("Enforcement officers:")
    for label, name in enforcement.items():
        print(f"  {label}: {name}")


def check_status():
    """
    Display the current status of all drones in the system.

    Iterates through all drone statuses and prints each drone's ID and status.
    """
    # Show the status for every drone code in the system.
    print("Current drone statuses:")
    for code, status in drone_status.items():
        print(f"  {code}: {status}")


def set_all_drones_online():
    """
    Set all drones in the system to 'online' status.

    Useful for initializing or resetting drone availability.
    """
    # Set every drone in the system to online.
    for code in drone_status:
        drone_status[code] = "online"
    print("All drones are now set to online.")


def dispatch_drone(city_grid):
    """
    Handle drone dispatch to a crime location.

    Prompts user to select a drone, checks its status, asks for crime location,
    verifies crime exists, and dispatches if confirmed. Sets drone to 'patrol'
    and marks drone_dispatched flag. Removes crime if both dispatches complete.

    Args:
        city_grid: The current city grid (not used in this function)

    Returns:
        tuple: (row, col) of dispatched location, or None if failed
    """
    # Ask user which drone to send to a crime location.
    list_drones()
    drone_input = input("Enter Drone ID to send to crime location: ").strip()

    if drone_input not in drone_status:
        print("Invalid Drone ID. Please try again.")
        return None

    check_status()
    if drone_status[drone_input] == "offline":
        print(f"{drone_input} is currently offline. Please choose an online drone.")
        return None

    # Ask for location
    coord_input = input("Enter crime location as row,col (for example 5,3): ").strip()
    try:
        row_str, col_str = coord_input.split(",")
        row = int(row_str)
        col = int(col_str)
    except (ValueError, AttributeError):
        print("Invalid format. Use row,col like 5,3.")
        return None

    # Check what crime is at that location
    if (row, col) in map.crime_details:
        crime_info = map.crime_details[(row, col)]
        crime_type = crime_info["type"]
        assigned_drone = crime_info["drone"]
        print(f"Crime at ({row},{col}): {crime_type}")
        print(f"Assigned drone: {assigned_drone}")
        confirm = input("Send this drone anyway? (y/n): ").lower()
        if confirm == "y":
            print(f"{drone_input} dispatched to ({row}, {col}) for {crime_type}.")
            drone_status[drone_input] = "patrol"
            map.crime_details[(row, col)]["drone_dispatched"] = True
            if map.crime_details[(row, col)]["enforcement_dispatched"]:
                del map.crime_details[(row, col)]
            return (row, col)
        else:
            return None
    else:
        print("No crime reported at that location.")
        return None


def dispatch_enforcement(city_grid):
    """
    Handle enforcement officer dispatch to a location.

    Prompts user to select an enforcement officer, asks for location,
    and dispatches. Marks enforcement_dispatched flag if crime exists.
    Removes crime if both dispatches complete.

    Args:
        city_grid: The current city grid (not used in this function)

    Returns:
        tuple: (row, col) of dispatched location, or None if failed
    """
    # Ask user which enforcement officer to send to a location.
    print("Enforcement officers:")
    for label, name in enforcement.items():
        print(f"  {label}: {name}")

    enforce_id = input("Enter Enforcement ID to send to location: ").strip()
    if enforce_id not in enforcement:
        print("Invalid Enforcement ID. Please try again.")
        return None

    coord_input = input("Enter location as row,col (for example 5,3): ").strip()
    try:
        row_str, col_str = coord_input.split(",")
        row = int(row_str)
        col = int(col_str)
    except (ValueError, AttributeError):
        print("Invalid format. Use row,col like 5,3.")
        return None

    print(f"{enforcement[enforce_id]} dispatched to ({row}, {col}).")
    if (row, col) in map.crime_details:
        map.crime_details[(row, col)]["enforcement_dispatched"] = True
        if map.crime_details[(row, col)]["drone_dispatched"]:
            del map.crime_details[(row, col)]
    return (row, col)


def show_menu():
    """
    Display the main menu options to the user.

    Prints the Guardian System header and numbered menu options.
    """
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
    """
    Main program loop.

    Displays menu, processes user choices, and handles program flow
    until user chooses to exit.
    """
    # Loop until the user chooses to exit.
    while True:
        show_menu()
        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            list_drones()
        elif choice == "2":
            droneid_input = input("Enter Drone ID for Status Check: ").strip()
            print("Checking status of drones...")
            time.sleep(1)
            status(droneid_input)
        elif choice == "3":
            list_suspects()
        elif choice == "4":
            list_enforcement()
            print("Press type 'quit' to return to the menu.")
            if input().lower() == "quit":
                continue
            print("Returning to menu...")
            time.sleep(1)
        elif choice == "5":
            print("Checking status of all drones...")
            time.sleep(1)
            check_status()
        elif choice == "6":
            set_all_drones_online()
        elif choice == "7":
            print("Displaying city map...")
            time.sleep(1)
            print("-----------------------------------------")
            display_grid(city_grid, (0, 0))
            print("-----------------------------------------")

            service_choice = (
                input(
                    "Would you like to send a drone or enforcement? (drone/enforcement/quit): "
                )
                .strip()
                .lower()
            )
            if service_choice == "drone":
                result = dispatch_drone(city_grid)
                if result:
                    print("Updated city map after dispatch:")
                    display_grid(city_grid, (0, 0))
            elif service_choice == "enforcement":
                result = dispatch_enforcement(city_grid)
                if result:
                    print("Updated city map after dispatch:")
                    display_grid(city_grid, (0, 0))

            print("Returning to menu...")
            time.sleep(1)
        elif choice == "8":
            print("Exiting Guardian System. Goodbye.")
            break
        else:
            print("Invalid selection. Please choose a number from 1 to 7.")


if __name__ == "__main__":
    main()
