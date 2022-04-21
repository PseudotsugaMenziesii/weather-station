from gpiozero import MCP3008
import time
import math


voltage_bearing = {0.4: 0, 
                   1.4: 22.5, 
                   1.2: 45, 
                   2.8: 67.5, 
                   2.7: 90, 
                   2.9: 112.5, 
                   2.2: 135, 
                   2.5: 157.5, 
                   1.8: 180, 
                   2.0: 202.5, 
                   0.7: 225, 
                   0.8: 247.5, 
                   0.1: 270, 
                   0.3: 292.5, 
                   0.2: 315, 
                   0.6: 337.5}

def get_angle(voltage):
    if voltage in voltage_bearing.keys():
        return voltage_bearing[voltage]
    else:
        return None

def get_average(angles):
    """Stolen from the demo..."""
    sin_sum = 0.0
    cos_sum = 0.0

    for angle in angles:
        r = math.radians(angle)
        sin_sum += math.sin(r)
        cos_sum += math.cos(r)

    flen = float(len(angles))
    s = sin_sum / flen
    c = cos_sum / flen
    arc = math.degrees(math.atan(s / c))
    average = 0.0

    if s > 0 and c > 0:
        average = arc
    elif c < 0:
        average = arc + 180
    elif s < 0 and c > 0:
        average = arc + 360

    return 0.0 if average == 360 else average

def get_value(time_secs=5):
    data = []
    start_time = time.time()

    # Open device connection
    ADC = MCP3008(channel=0)

    while time.time() - start_time < time_secs:
        wind = round(ADC.value * 3.3, 1)
        wind_angle = get_angle(wind)
        if wind_angle:
            data.append(wind_angle)

    # Close device connection
    ADC.close()

    if data:
        return get_average(data)
    print("NO GOOD WIND DIRECTION VALUES!!")
    return 999.99

if __name__ == '__main__':
    print(get_value(10))
