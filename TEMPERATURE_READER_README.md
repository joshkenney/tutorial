# Raspberry Pi 5 Temperature Reader

A comprehensive Python script to monitor the CPU temperature on Raspberry Pi 5.

## Features

- 🌡️ Real-time CPU temperature monitoring
- 🔄 Continuous monitoring mode with customizable intervals
- 🌍 Support for both Celsius and Fahrenheit
- 🎯 Multiple reading methods (vcgencmd and thermal zone)
- 📊 Temperature status indicators (Cool, Normal, Warm, Hot, Very Hot)
- ⚡ Automatic fallback between reading methods
- 🎨 User-friendly colored output with emojis

## Requirements

- Raspberry Pi 5 (or other Raspberry Pi models)
- Python 3.x (pre-installed on Raspberry Pi OS)
- No additional Python packages required (uses standard library only)

## Installation

1. Clone this repository or download the script:
   ```bash
   git clone https://github.com/joshkenney/tutorial.git
   cd tutorial
   ```

2. Make the script executable (optional):
   ```bash
   chmod +x raspberry_pi_temp_reader.py
   ```

## Usage

### Basic Usage

Read temperature once:
```bash
python3 raspberry_pi_temp_reader.py
```

### Continuous Monitoring

Monitor temperature continuously (updates every 2 seconds):
```bash
python3 raspberry_pi_temp_reader.py --continuous
```

Or use the short form:
```bash
python3 raspberry_pi_temp_reader.py -c
```

### Fahrenheit Display

Display temperature in Fahrenheit:
```bash
python3 raspberry_pi_temp_reader.py --fahrenheit
```

Or use the short form:
```bash
python3 raspberry_pi_temp_reader.py -f
```

### Custom Update Interval

Continuous monitoring with custom interval (e.g., 5 seconds):
```bash
python3 raspberry_pi_temp_reader.py --continuous --interval 5
```

### Combined Options

Continuous monitoring in Fahrenheit with 3-second intervals:
```bash
python3 raspberry_pi_temp_reader.py -c -f -i 3
```

## Command-Line Options

| Option | Short | Description |
|--------|-------|-------------|
| `--continuous` | `-c` | Enable continuous monitoring mode |
| `--fahrenheit` | `-f` | Display temperature in Fahrenheit instead of Celsius |
| `--interval N` | `-i N` | Set update interval to N seconds (default: 2) |
| `--help` | `-h` | Show help message and exit |

## Example Output

```
🌡️  Raspberry Pi 5 CPU Temperature
   Temperature: 45.2°C
   Status: ✅ Cool
   Method: vcgencmd
```

## Temperature Status Indicators

| Temperature (°C) | Status | Description |
|-----------------|--------|-------------|
| < 50°C | ✅ Cool | Normal operating temperature |
| 50-60°C | 🟡 Normal | Typical under moderate load |
| 60-70°C | 🟠 Warm | Under heavy load |
| 70-80°C | 🔶 Hot | Consider improving cooling |
| > 80°C | 🔥 Very Hot | Critical - improve cooling immediately |

## How It Works

The script uses two methods to read the CPU temperature:

1. **vcgencmd**: Uses the VideoCore GPU command-line tool (preferred method)
   - Command: `vcgencmd measure_temp`
   - Available when the vcgencmd utility is installed

2. **Thermal Zone**: Reads from the system thermal zone file
   - Path: `/sys/class/thermal/thermal_zone0/temp`
   - Fallback method when vcgencmd is not available

The script automatically detects the best available method and falls back if needed.

## Troubleshooting

### Permission Denied Error

If you get a permission denied error when reading the thermal zone file, you can:

1. Run with sudo (not recommended for regular use):
   ```bash
   sudo python3 raspberry_pi_temp_reader.py
   ```

2. Or add your user to the video group:
   ```bash
   sudo usermod -a -G video $USER
   ```
   Then log out and log back in.

### "Unable to read temperature" Error

This error appears when:
- You're not running on a Raspberry Pi
- The thermal zone file is not accessible
- vcgencmd is not available and thermal zone file doesn't exist

**Solution**: Ensure you're running this script on a Raspberry Pi with Raspberry Pi OS.

### vcgencmd Not Found

If vcgencmd is not available, the script will automatically fall back to reading from the thermal zone file. No action needed.

## Testing on Non-Raspberry Pi Systems

For development/testing purposes on non-Raspberry Pi systems, you can create a mock thermal zone file:

```bash
# Create mock thermal zone directory
sudo mkdir -p /sys/class/thermal/thermal_zone0

# Create mock temperature file (45.2°C)
echo "45200" | sudo tee /sys/class/thermal/thermal_zone0/temp
```

## Integration Examples

### Cron Job for Logging

Log temperature every 5 minutes:

1. Create a log script:
   ```bash
   #!/bin/bash
   echo "$(date '+%Y-%m-%d %H:%M:%S') - $(python3 /path/to/raspberry_pi_temp_reader.py)" >> /home/pi/temp_log.txt
   ```

2. Add to crontab:
   ```bash
   crontab -e
   # Add this line:
   */5 * * * * /home/pi/log_temp.sh
   ```

### Python Integration

```python
from raspberry_pi_temp_reader import RaspberryPiTempReader

reader = RaspberryPiTempReader()
temp_celsius, method = reader.get_temperature()

if temp_celsius is not None:
    print(f"Current temperature: {temp_celsius}°C")
    
    # Convert to Fahrenheit
    temp_fahrenheit = reader.celsius_to_fahrenheit(temp_celsius)
    print(f"Temperature in Fahrenheit: {temp_fahrenheit}°F")
```

## License

This project is part of a Git tutorial repository. Feel free to use and modify as needed.

## Contributing

This is a tutorial repository. Feel free to fork and experiment with the code.

## Related Resources

- [Raspberry Pi Documentation](https://www.raspberrypi.org/documentation/)
- [vcgencmd Documentation](https://www.raspberrypi.com/documentation/computers/os.html#vcgencmd)
- [Raspberry Pi Cooling Solutions](https://www.raspberrypi.com/products/)

## Author

Created for the Git tutorial repository by joshkenney.
