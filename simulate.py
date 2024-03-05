# Adjusting the simulation approach to correctly handle time ranges and events for gnuplot graphing

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
power_data_path = "/mnt/data/power_over_time_corrected.csv"
events_data_path = "/mnt/data/events_for_gnuplot.txt"
power_over_time_df.to_csv(power_data_path, index=False)
events_df.to_csv(events_data_path, index=False, sep=' ')

power_data_path, events_data_path
