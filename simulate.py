import pandas as pd
import numpy as np
import datetime
import random

# Load devices from the previously saved structure
devices = [
    {"name": "Pool Pump", "load": 3, "preemptable": True, "scheduling_flexible": True, "demand_times": ["09:30", "15:00"]},
    {"name": "Washing Machine", "load": 2, "preemptable": False, "scheduling_flexible": True, "demand_times": ["19:16", "23:28"]},
    {"name": "A/C", "load": 5, "preemptable": False, "scheduling_flexible": True, "demand_times": ["12:00", "17:00", "22:00"]},
    {"name": "Dishwasher", "load": 1.5, "preemptable": True, "scheduling_flexible": True, "demand_times": ["22:15"]},
    {"name": "Refrigerator", "load": 1, "preemptable": False, "scheduling_flexible": False, "demand_times": []},  # Always on
    {"name": "Microwave", "load": 2.5, "preemptable": False, "scheduling_flexible": False, "demand_times": ["18:23", "20:23", "08:05"]},
    {"name": "Oven", "load": 4, "preemptable": False, "scheduling_flexible": False, "demand_times": ["12:30", "18:30"]},
    {"name": "TV", "load": 0.5, "preemptable": True, "scheduling_flexible": True, "demand_times": ["20:00", "22:00"]},
    {"name": "Computer", "load": 0.7, "preemptable": True, "scheduling_flexible": True, "demand_times": ["08:00", "23:00"]},
    {"name": "Heater", "load": 3.5, "preemptable": False, "scheduling_flexible": False, "demand_times": ["06:30", "21:00"]}
]

# Define a maximum load
max_load = 13

# Helper function to convert time string to a timedelta for easier time manipulation
def time_str_to_timedelta(time_str):
    hours, minutes = map(int, time_str.split(':'))
    return datetime.timedelta(hours=hours, minutes=minutes)

# Adjusting simulation to fix previous issue
def simulate_device_usage_corrected(devices, max_load):
    start_time = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    end_time = start_time + datetime.timedelta(days=1)
    time_index = pd.date_range(start=start_time, end=end_time, freq='T').to_pydatetime()[:-1]  # Exclude last as it's 00:00 next day
    power_over_time = pd.Series(0, index=time_index)
    events = []  # Time, Event, Color

    for device in devices:
        for demand_time in device['demand_times']:
            dt_start = start_time + time_str_to_timedelta(demand_time)
            # Randomly determine usage duration between 30 to 120 minutes
            dt_end = dt_start + datetime.timedelta(minutes=random.randint(30, 120))

            # Check load constraint before turning on the device
            if power_over_time[dt_start:dt_end].max() + device['load'] > max_load:
                # Log delay due to load constraint
                events.append((dt_start, f"{device['name']} delay", "grey"))
                continue  # Skip to next demand time or device
            
            # Simulate device turning on
            power_over_time[dt_start:dt_end] += device['load']
            events.append((dt_start, f"{device['name']} ON", "green"))
            
            # Assuming device turns off after duration, log the event
            events.append((dt_end, f"{device['name']} OFF", "red"))

    return power_over_time, events

# Re-run the corrected simulation
power_over_time_corrected, events_corrected = simulate_device_usage_corrected(devices, max_load)

# Convert results to suitable formats for gnuplot
power_over_time_df = pd.DataFrame({'Time': power_over_time_corrected.index, 'Power': power_over_time_corrected.values})
events_df = pd.DataFrame(events_corrected, columns=['Time', 'Label', 'Color'])

# Save to files
power_data_path = "data/power_over_time_corrected.csv"
events_data_path = "data/events_for_gnuplot.txt"
power_over_time_df.to_csv(power_data_path, index=False)
events_df.to_csv(events_data_path, index=False, sep=' ')

power_data_path, events_data_path
