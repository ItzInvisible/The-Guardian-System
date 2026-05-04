"""
Map Module for Guardian System

This module handles the creation and display of the city grid, including
random crime generation and tracking of crime response status.

Key components:
- Grid cell types (residential, commercial, empty, crime)
- Crime types and their recommended responses
- Crime details tracking with dispatch flags
- Grid creation with random elements
- Grid display with crime information
"""

import random

from classes import drone_status

# Grid cell types - symbols used in the city grid
RESIDENTIAL = "R"  # Residential area
COMMERCIAL = "C"  # Commercial area
EMPTY = "."  # Empty road
CRIME = "!"  # Crime incident

# Crime types with recommended response (all currently use drones)
CRIME_TYPES = {
    "Robbery": "Drone",
    "Assault": "Drone",
    "Theft": "Drone",
    "Vandalism": "Drone",
    "Disturbance": "Drone",
}

# Dictionary to store crime details: {(row, col): {'type': crime_type, 'drone': assigned_drone_id, 'drone_dispatched': bool, 'enforcement_dispatched': bool}}
crime_details = {}


def create_city(rows=8, cols=8):
    """
    Create a randomized city grid with random crime markers and assigned drone IDs.

    Args:
        rows (int): Number of rows in the grid (default 8)
        cols (int): Number of columns in the grid (default 8)

    Returns:
        list: 2D list representing the city grid with cell types

    Places 2-4 random crimes, assigns drones, and initializes dispatch flags.
    """
    global crime_details
    crime_details = {}  # Reset crime details for new city

    # Fill grid with mostly empty cells (roads)
    grid = [[EMPTY for _ in range(cols)] for _ in range(rows)]

    # Add some residential and commercial zones randomly
    for r in range(rows):
        for c in range(cols):
            if random.random() < 0.3:  # 30% chance for buildings
                grid[r][c] = random.choice([RESIDENTIAL, COMMERCIAL])

    # Get list of available drone IDs from classes.py
    drone_ids = list(drone_status.keys())

    # Place crime markers randomly with crime types and assigned drones
    for _ in range(random.randint(2, 4)):  # 2-4 crimes
        r, c = random.randint(0, rows - 1), random.randint(0, cols - 1)
        if grid[r][c] not in (CRIME,):  # Don't overwrite existing crimes
            grid[r][c] = CRIME
            crime_type = random.choice(list(CRIME_TYPES.keys()))
            assigned_drone = random.choice(drone_ids)
            crime_details[(r, c)] = {
                "type": crime_type,
                "drone": assigned_drone,
                "drone_dispatched": False,
                "enforcement_dispatched": False,
            }

    return grid


def display_grid(grid, drone_pos=(0, 0)):
    """
    Display the city grid with drone position and highlight crime incidents.

    Args:
        grid (list): 2D list of the city grid
        drone_pos (tuple): (row, col) position of the drone (default (0,0))

    Shows grid with symbols, legend, and list of unresolved crimes with details.
    Resolved crimes appear as empty spaces.
    """
    drone_row, drone_col = drone_pos
    crimes = []  # List of unresolved crime positions

    # Print column numbers
    print("\n  " + " ".join(str(i) for i in range(len(grid[0]))))
    print("  " + "--" * len(grid[0]))

    # Print grid rows
    for r, row in enumerate(grid):
        print(f"{r}|", end=" ")
        for c, cell in enumerate(row):
            if (r, c) == (drone_row, drone_col):
                print("D", end=" ")  # Drone position
            elif cell == CRIME:
                crime_info = crime_details.get((r, c), {})
                if not (
                    crime_info.get("drone_dispatched", False)
                    and crime_info.get("enforcement_dispatched", False)
                ):
                    print("!", end=" ")  # Unresolved crime
                    crimes.append((r, c))
                else:
                    print(".", end=" ")  # Resolved crime shown as empty
            else:
                print(cell, end=" ")  # Other cell types
        print()

    # Show legend
    print("\nLegend: D=Drone  R=Residential  C=Commercial  !=Crime  .=Road")

    # Print crimes with needed resources
    if crimes:
        print("\n=== CRIMES & RESPONSE NEEDED ===")
        for r, c in crimes:
            crime_info = crime_details.get(
                (r, c), {"type": "Unknown", "drone": "UNKNOWN"}
            )
            crime_type = crime_info["type"]
            assigned_drone = crime_info["drone"]
            print(f"  ({r},{c}): {crime_type}")
            print(f"       Assigned Drone: {assigned_drone}")
            print("       Enforcement needed: Yes\n")
