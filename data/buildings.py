from data.maps import (
    era_1920s_map,
    era_1950s_map,
    era_1960s_map,
    era_1980s_map,
    era_1990s_map,
    interior_1920s_club,
    interior_1920s_bank,
    interior_1920s_warehouse
)

building_data = {
    
    ("1920s", 5, 4): {"name": "Club", "target_map": interior_1920s_club, "spawn": (9, 11)},
    ("1920s", 6, 4): {"name": "Club", "target_map": interior_1920s_club, "spawn": (9, 11)},
    ("1920s", 22, 4): {"name": "Bank", "target_map": interior_1920s_bank, "spawn": (9, 11)},
    ("1920s", 23, 4): {"name": "Bank", "target_map": interior_1920s_bank, "spawn": (9, 11)},
    ("1920s", 22, 13): {"name": "Warehouse", "target_map": interior_1920s_warehouse, "spawn": (9, 11)},
    ("1920s", 23, 13): {"name": "Warehouse", "target_map": interior_1920s_warehouse, "spawn": (9, 11)},
    
    ("1960s", 10, 7): {"name": "Cafe", "target_map": interior_1920s_club, "spawn": (9, 11)},  # placeholder interior
    ("1980s", 10, 4): {"name": "Office", "target_map": interior_1920s_bank, "spawn": (9, 11)},  # placeholder interior
    ("1990s", 8, 12): {"name": "Mall", "target_map": interior_1920s_warehouse, "spawn": (9, 11)},  # placeholder interior

    # INTERIOR EXITS

    # Club / Cafe 
    ("Club", 9, 13): {"name": "1920s", "target_map": era_1920s_map, "spawn": (5, 5)},
    ("Cafe", 8, 13): {"name": "1960s", "target_map": era_1960s_map, "spawn": (10, 8)},

    # Bank / Office
    ("Bank", 8, 12): {"name": "1920s", "target_map": era_1920s_map, "spawn": (22, 5)},
    ("Bank", 9, 12): {"name": "1920s", "target_map": era_1920s_map, "spawn": (22, 5)},
    ("Office", 8, 12): {"name": "1980s", "target_map": era_1980s_map, "spawn": (10, 5)},
    ("Office", 9, 12): {"name": "1980s", "target_map": era_1980s_map, "spawn": (10, 5)},

    # Warehouse / Mall 
    ("Warehouse", 8, 13): {"name": "1920s", "target_map": era_1920s_map, "spawn": (22, 12)},
    ("Warehouse", 9, 13): {"name": "1920s", "target_map": era_1920s_map, "spawn": (22, 12)},
    ("Mall", 8, 13): {"name": "1990s", "target_map": era_1990s_map, "spawn": (8, 13)},
    ("Mall", 9, 13): {"name": "1990s", "target_map": era_1990s_map, "spawn": (8, 13)},
}