import random

# city_grid.py
# This module creates and displays a randomized city grid.
# The grid includes residential, commercial, restricted, and empty cells.
# It also places crime markers (!) and enforcement needed markers (E).

# Cell types used inside the city grid.
RESIDENTIAL = 'R'          # Residential area
COMMERCIAL = 'C'           # Commercial area
RESTRICTED = 'X'           # Restricted zone, special warnings may apply
EMPTY = '.'                # Empty road or open space
CRIME = '!'                # Crime marker to show where incidents occur
ENFORCEMENT_NEEDED = 'E'   # Enforcement needed marker for police response

# Alerts stored as {(row, col): "description"}.
# These can be added manually with add_alert().
alerts = {}


def create_city(rows=10, cols=10, crime_count=5, enforcement_count=4):
    """Create a randomized city grid with crime and enforcement markers."""
    # Possible zone types for random placement.
    cell_types = [RESIDENTIAL, COMMERCIAL, EMPTY, RESTRICTED]
    weights = [0.4, 0.25, 0.25, 0.1]

    # Build a random base grid using weighted choices for each cell.
    grid = [
        [random.choices(cell_types, weights)[0] for _ in range(cols)]
        for _ in range(rows)
    ]

    # Prepare a shuffled list of all grid coordinates.
    empty_cells = [(r, c) for r in range(rows) for c in range(cols)]
    random.shuffle(empty_cells)

    # Place crime markers randomly in the grid.
    placed = 0
    for (r, c) in empty_cells:
        if placed >= crime_count:
            break
        if grid[r][c] not in (CRIME, ENFORCEMENT_NEEDED):
            grid[r][c] = CRIME
            placed += 1

    # Place enforcement-needed markers in different random cells.
    random.shuffle(empty_cells)
    placed = 0
    for (r, c) in empty_cells:
        if placed >= enforcement_count:
            break
        if grid[r][c] not in (CRIME, ENFORCEMENT_NEEDED):
            grid[r][c] = ENFORCEMENT_NEEDED
            placed += 1

    return grid


def add_alert(grid, row, col, message):
    # Add a custom alert message for a specific grid cell.
    # If the cell is restricted, also print a warning immediately.
    if grid[row][col] == RESTRICTED:
        print(f"  [!] WARNING: Alert in RESTRICTED zone at ({row},{col})!")
    alerts[(row, col)] = message


def display_grid(grid, drone_pos):
    # Draw the city grid and show the drone position.
    # Also collect coordinates of crimes and enforcement-needed markers.
    drone_row, drone_col = drone_pos
    crime_positions = []
    enforcement_positions = []

    # Print the column headers.
    print("\n  " + " ".join(str(i) for i in range(len(grid[0]))))
    print("  " + "--" * len(grid[0]))

    for r, row in enumerate(grid):
        print(f"{r}|", end=" ")
        for c, cell in enumerate(row):
            if (r, c) == (drone_row, drone_col):
                print('D', end=" ")
            elif (r, c) in alerts:
                # Show alert markers as ! in the grid.
                print('!', end=" ")
            elif cell == CRIME:
                print('!', end=" ")
                crime_positions.append((r, c))
            elif cell == ENFORCEMENT_NEEDED:
                print('E', end=" ")
                enforcement_positions.append((r, c))
            else:
                print(cell, end=" ")
        print()

    # Legend for grid symbols.
    print("\n  Legend: D=Drone  R=Residential  C=Commercial  X=Restricted  !=Crime/Alert  .=Road E=Enforcement Needed")

    # Print a summary of crime marker positions.
    if crime_positions:
        print("\n  Crimes reported at:")
        for r, c in crime_positions:
            print(f"    ({r},{c})")

    # Print a summary of enforcement-needed positions.
    if enforcement_positions:
        print("\n  Enforcement needed at:")
        for r, c in enforcement_positions:
            print(f"    ({r},{c})")

    # Print custom active alerts, if any were added.
    if alerts:
        print("\n  Active Alerts:")
        for (r, c), msg in alerts.items():
            zone = grid[r][c]
            print(f"    ({r},{c}) [{zone}] — {msg}")
