import screeninfo

from screeninfo import get_monitors

monitor_count = len(get_monitors())
print(f"Number of monitors detected: {monitor_count}")

# You can also iterate through them to see details:
for i, monitor in enumerate(get_monitors()):
    print(f"Monitor {i+1}: {monitor}")
