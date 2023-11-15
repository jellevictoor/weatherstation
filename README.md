# Micropython Weatherstation

## calculate surface to benchmark to know the rained mm
    - 36 rocks = 300 ml
    - 1 rock = 300/36
    - surface_in_mm =  pow(180/2,2) * math.pi
    - ml_in_mm2 = surface_in_mm/1000
    - liter_modifier = rock/ml_in_mm2