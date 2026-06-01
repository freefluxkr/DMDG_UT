import os
import time
import sys

try:
    import psutil
except ImportError:
    print("Error: 'psutil' library is required to run this script.")
    print("Please install it by running: pip install psutil")
    sys.exit(1)

def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def monitor_system(interval=1):
    print("="*60)
    print("  Real-time System Monitor (Task Manager Data)")
    print("  Press Ctrl + C to exit")
    print("="*60)
    
    # Initial network stats to calculate speed
    net_old = psutil.net_io_counters()
    
    try:
        while True:
            # 1. CPU Usage
            cpu_usage = psutil.cpu_percent(interval=None) # Non-blocking call
            cpu_cores = psutil.cpu_percent(interval=None, percpu=True)
            
            # 2. Memory Usage
            mem = psutil.virtual_memory()
            mem_total = get_size(mem.total)
            mem_used = get_size(mem.used)
            mem_avail = get_size(mem.available)
            mem_percent = mem.percent
            
            # 3. Network speed calculation
            net_new = psutil.net_io_counters()
            bytes_sent = net_new.bytes_sent - net_old.bytes_sent
            bytes_recv = net_new.bytes_recv - net_old.bytes_recv
            
            speed_sent = get_size(bytes_sent / interval) + "/s"
            speed_recv = get_size(bytes_recv / interval) + "/s"
            
            # Reset old network values
            net_old = net_new
            
            # Clear terminal screen (cross-platform)
            os.system('cls' if os.name == 'nt' else 'clear')
            
            # Display stats
            print("="*60)
            print(f" Real-time System Monitor | Interval: {interval}s")
            print("="*60)
            
            print(f" [CPU Usage]: {cpu_usage}%")
            # Draw a mini progress bar for CPU
            bar_len = 20
            filled_len = int(bar_len * cpu_usage / 100)
            bar = '█' * filled_len + '-' * (bar_len - filled_len)
            print(f"  CPU Bar: |{bar}|")
            print(f"  Cores (Per Core): {', '.join([f'{c}%' for c in cpu_cores])}")
            print("-" * 60)
            
            print(f" [Memory Usage]: {mem_percent}%")
            mem_filled = int(bar_len * mem_percent / 100)
            mem_bar = '█' * mem_filled + '-' * (bar_len - mem_filled)
            print(f"  Memory Bar: |{mem_bar}|")
            print(f"  Total: {mem_total} | Used: {mem_used} | Available: {mem_avail}")
            print("-" * 60)
            
            print(" [Network Traffic]:")
            print(f"  Upload Speed:   {speed_sent}")
            print(f"  Download Speed: {speed_recv}")
            print(f"  Total Sent:     {get_size(net_new.bytes_sent)}")
            print(f"  Total Received: {get_size(net_new.bytes_recv)}")
            print("="*60)
            
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")

if __name__ == "__main__":
    monitor_system(interval=1)
