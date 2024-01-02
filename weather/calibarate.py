# small script to calibrate the rain gauge
# I pour 3 times a fixed amount into the rain gauge and count the number of rocks
# based on the amount of water and the count of rocks I can calculate the amount of water per rock
# the surface of the rain gauge is 26590.44021998400997 mm2, but this is based on the diameter of the rain gauge
# if you decide to use another rain gauge you need to calculate the surface of the rain gauge
# and replace the #surface variable
import math

top_ring_diameter = 180

# calibration values
calibration_volume_l = 0.25
calibration_rocks = 65


def get_diameter(diameter_top_circle_mm):
    surface = (diameter_top_circle_mm / 2) ** 2 * math.pi
    return surface * 0.000001


def single_rock_volume(diameter_top_circle):
    in_liters_per_m2 = get_diameter(diameter_top_circle)
    calibration_volume_per_mm2 = calibration_volume_l * (1 / in_liters_per_m2)
    return calibration_volume_per_mm2 / calibration_rocks



in_liters_per_rock = single_rock_volume(top_ring_diameter)
print(f"One rock is {in_liters_per_rock} liters")
