"""
Classes Module for Guardian System

This module defines the core data structures used throughout the system:
- Drone identifiers and their statuses
- Known suspects
- Enforcement officers

All data is stored in dictionaries for easy access and modification.
"""

droneid = {
    "Drone 1A": "DRN1A",  # Drone label to ID mapping
    "Drone 1B": "DRN1B",
    "Drone 2A": "DRN2A",
    "Drone 2B": "DRN2B",
    "Drone 3A": "DRN3A",
    "Drone 3B": "DRN3B",
}

drone_status = {
    "DRN1A": "offline",  # Initial status for each drone (offline/online/patrol)
    "DRN1B": "offline",
    "DRN2A": "offline",
    "DRN2B": "offline",
    "DRN3A": "offline",
    "DRN3B": "offline",
}

suspect = {
    "Suspect 1": "Giovanni",  # Known suspects with labels and names
    "Suspect 2": "Lillain",
    "Suspect 3": "Marcello",
}


enforcement = {
    "ENFORCE1": "Officer Stevenson",  # Enforcement officers with IDs and names
    "ENFORCE2": "Officer Darling",
}
