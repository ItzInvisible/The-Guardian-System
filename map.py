import random
from classes import drone_status

# Simple city map module for the Guardian System
# Creates and displays a randomized city grid with crime and enforcement markers

# Grid cell types
RESIDENTIAL = 'R'  # Residential area
COMMERCIAL = 'C'   # Commercial area  
EMPTY = '.'        # Empty road
CRIME = '!'        # Crime incident

# Crime types with recommended response
CRIME_TYPES = {
    'Robbery': 'Drone',
    'Assault': 'Drone',
    'Theft': 'Drone',
    'Vandalism': 'Drone',
    'Disturbance': 'Drone'
}

# Dictionary to store crime details: {(row, col): {'type': crime_type, 'drone': assigned_drone_id}}
crime_details = {}


def create_city(rows=8, cols=8):
    """Create a randomized city grid with random crime markers and assigned drone IDs."""
    global crime_details
    crime_details = {}
    
    # Fill grid with mostly empty cells (roads)
    grid = [[EMPTY for _ in range(cols)] for _ in range(rows)]
    
    # Add some residential and commercial zones
    for r in range(rows):
        for c in range(cols):
            if random.random() < 0.3:
                grid[r][c] = random.choice([RESIDENTIAL, COMMERCIAL])
    
    # Get list of available drone IDs from classes.py
    drone_ids = list(drone_status.keys())
    
    # Place crime markers randomly with crime types and assigned drones
    for _ in range(random.randint(2, 4)):
        r, c = random.randint(0, rows - 1), random.randint(0, cols - 1)
        if grid[r][c] not in (CRIME,):
            grid[r][c] = CRIME
            crime_type = random.choice(list(CRIME_TYPES.keys()))
            assigned_drone = random.choice(drone_ids)
            crime_details[(r, c)] = {'type': crime_type, 'drone': assigned_drone}
    
    return grid


def display_grid(grid, drone_pos=(0, 0)):
    """Display the city grid with drone position and highlight crime incidents."""
    drone_row, drone_col = drone_pos
    crimes = []
    
    # Print column numbers
    print("\n  " + " ".join(str(i) for i in range(len(grid[0]))))
    print("  " + "--" * len(grid[0]))
    
    # Print grid
    for r, row in enumerate(grid):
        print(f"{r}|", end=" ")
        for c, cell in enumerate(row):
            if (r, c) == (drone_row, drone_col):
                print('D', end=" ")  # Drone
            elif cell == CRIME:
                print('!', end=" ")
                crimes.append((r, c))
            else:
                print(cell, end=" ")
        print()
    
    # Show legend
    print("\nLegend: D=Drone  R=Residential  C=Commercial  !=Crime  .=Road")
    
    # Print crimes with needed resources
    if crimes:
        print("\n=== CRIMES & RESPONSE NEEDED ===")
        for r, c in crimes:
            crime_info = crime_details.get((r, c), {'type': 'Unknown', 'drone': 'UNKNOWN'})
            crime_type = crime_info['type']
            assigned_drone = crime_info['drone']
            print(f"  ({r},{c}): {crime_type}")
            print(f"       Assigned Drone: {assigned_drone}")
            print(f"       Enforcement needed: Yes\n")

