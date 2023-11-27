# small script to calibrate the rain gauge
# I pour 3 times a fixed amount into the rain gauge and count the number of rocks
# based on the amount of water and the count of rocks I can calculate the amount of water per rock
# the surface of the rain gauge is 26590.44021998400997 mm2, but this is based on the diameter of the rain gauge
# if you decide to use another rain gauge you need to calculate the surface of the rain gauge
# and replace the #surface variable

calibration_volume_l = 0.250
calibration_rocks = 52
surface = 26590.44021998400997
in_liters_per_m2 = 1000000 / surface
in_liters_per_rock = (calibration_volume_l / calibration_rocks) * in_liters_per_m2
print(in_liters_per_rock)
