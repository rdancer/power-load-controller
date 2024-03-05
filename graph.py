import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Load the power over time data and event labels
power_data = pd.read_csv(power_data_path)
events_data = pd.read_csv(events_data_path, sep=' ', parse_dates=['Time'])

# Convert 'Time' column to datetime for plotting
power_data['Time'] = pd.to_datetime(power_data['Time'])

# Plotting
fig, ax = plt.subplots(figsize=(12, 6))

# Plot power over time
ax.plot(power_data['Time'], power_data['Power'], label='Power Load', color='blue')

# Formatting the date on the x-axis
ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

# Plot event labels
for _, row in events_data.iterrows():
    ax.axvline(x=row['Time'], color=row['Color'], linestyle='--')
    ax.text(row['Time'], power_data['Power'].max(), row['Label'], rotation=45, ha='right', color=row['Color'])

# Labeling
ax.set_xlabel('Time')
ax.set_ylabel('Power (A)')
ax.set_title('Power Load Over Time with Device Events')
plt.xticks(rotation=45)
plt.tight_layout()
plt.legend()

# Show plot
plt.show()
