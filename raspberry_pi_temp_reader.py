#!/usr/bin/env python3
"""
Raspberry Pi 5 Temperature Reader

This script reads the CPU temperature from a Raspberry Pi 5.
It supports multiple methods for reading temperature:
1. Using vcgencmd (VideoCore GPU command-line tool)
2. Reading from thermal zone files in /sys/class/thermal/

Usage:
    python3 raspberry_pi_temp_reader.py
    python3 raspberry_pi_temp_reader.py --continuous
    python3 raspberry_pi_temp_reader.py --fahrenheit
"""

import os
import subprocess
import sys
import time
import argparse
import shutil
from typing import Optional, Tuple


class RaspberryPiTempReader:
    """Class to read temperature from Raspberry Pi 5"""
    
    THERMAL_ZONE_PATH = "/sys/class/thermal/thermal_zone0/temp"
    
    def __init__(self):
        """Initialize the temperature reader"""
        self.method = self._detect_best_method()
    
    def _detect_best_method(self) -> str:
        """
        Detect the best available method for reading temperature
        
        Returns:
            str: 'vcgencmd' or 'thermal_zone'
        """
        # Check if vcgencmd is available
        if shutil.which('vcgencmd') is not None:
            return 'vcgencmd'
        
        # Check if thermal zone file exists
        if os.path.exists(self.THERMAL_ZONE_PATH):
            return 'thermal_zone'
        
        return 'thermal_zone'  # Default fallback
    
    def read_temp_vcgencmd(self) -> Optional[float]:
        """
        Read temperature using vcgencmd command
        
        Returns:
            float: Temperature in Celsius, or None if failed
        """
        try:
            result = subprocess.run(
                ['vcgencmd', 'measure_temp'],
                capture_output=True,
                text=True,
                check=True
            )
            # Output format: temp=42.8'C
            temp_str = result.stdout.strip()
            temp_value = temp_str.split('=')[1].split("'")[0]
            return float(temp_value)
        except (subprocess.CalledProcessError, IndexError, ValueError, FileNotFoundError):
            return None
    
    def read_temp_thermal_zone(self) -> Optional[float]:
        """
        Read temperature from thermal zone file
        
        Returns:
            float: Temperature in Celsius, or None if failed
        """
        try:
            with open(self.THERMAL_ZONE_PATH, 'r') as f:
                temp_millidegrees = int(f.read().strip())
                return temp_millidegrees / 1000.0
        except (FileNotFoundError, ValueError, PermissionError):
            return None
    
    def get_temperature(self) -> Tuple[Optional[float], str]:
        """
        Get the current CPU temperature
        
        Returns:
            tuple: (temperature in Celsius, method used)
        """
        if self.method == 'vcgencmd':
            temp = self.read_temp_vcgencmd()
            if temp is not None:
                return temp, 'vcgencmd'
        
        # Fallback to thermal zone
        temp = self.read_temp_thermal_zone()
        return temp, 'thermal_zone'
    
    @staticmethod
    def celsius_to_fahrenheit(celsius: float) -> float:
        """
        Convert Celsius to Fahrenheit
        
        Args:
            celsius: Temperature in Celsius
            
        Returns:
            float: Temperature in Fahrenheit
        """
        return (celsius * 9/5) + 32
    
    def display_temperature(self, use_fahrenheit: bool = False) -> None:
        """
        Display the current temperature in a formatted way
        
        Args:
            use_fahrenheit: If True, display in Fahrenheit; otherwise Celsius
        """
        temp_celsius, method = self.get_temperature()
        
        if temp_celsius is None:
            print("❌ Error: Unable to read temperature")
            print("   Make sure you're running this on a Raspberry Pi")
            return
        
        if use_fahrenheit:
            temp_value = self.celsius_to_fahrenheit(temp_celsius)
            unit = "°F"
        else:
            temp_value = temp_celsius
            unit = "°C"
        
        # Determine temperature status
        status = self._get_temp_status(temp_celsius)
        
        print(f"🌡️  Raspberry Pi 5 CPU Temperature")
        print(f"   Temperature: {temp_value:.1f}{unit}")
        print(f"   Status: {status}")
        print(f"   Method: {method}")
    
    @staticmethod
    def _get_temp_status(temp_celsius: float) -> str:
        """
        Get a descriptive status based on temperature
        
        Args:
            temp_celsius: Temperature in Celsius
            
        Returns:
            str: Status description
        """
        if temp_celsius < 50:
            return "✅ Cool"
        elif temp_celsius < 60:
            return "🟡 Normal"
        elif temp_celsius < 70:
            return "🟠 Warm"
        elif temp_celsius < 80:
            return "🔶 Hot"
        else:
            return "🔥 Very Hot - Consider cooling!"


def main():
    """Main function to run the temperature reader"""
    parser = argparse.ArgumentParser(
        description="Raspberry Pi 5 Temperature Reader",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 raspberry_pi_temp_reader.py              # Read temperature once
  python3 raspberry_pi_temp_reader.py --continuous # Continuous monitoring
  python3 raspberry_pi_temp_reader.py --fahrenheit # Display in Fahrenheit
  python3 raspberry_pi_temp_reader.py -c -f        # Continuous in Fahrenheit
        """
    )
    
    parser.add_argument(
        '-c', '--continuous',
        action='store_true',
        help='Continuously monitor temperature (updates every 2 seconds)'
    )
    
    parser.add_argument(
        '-f', '--fahrenheit',
        action='store_true',
        help='Display temperature in Fahrenheit instead of Celsius'
    )
    
    parser.add_argument(
        '-i', '--interval',
        type=int,
        default=2,
        help='Update interval in seconds for continuous mode (default: 2)'
    )
    
    args = parser.parse_args()
    
    reader = RaspberryPiTempReader()
    
    try:
        if args.continuous:
            print("Starting continuous temperature monitoring...")
            print("Press Ctrl+C to stop\n")
            while True:
                reader.display_temperature(use_fahrenheit=args.fahrenheit)
                print()  # Empty line for readability
                time.sleep(args.interval)
        else:
            reader.display_temperature(use_fahrenheit=args.fahrenheit)
    
    except KeyboardInterrupt:
        print("\n\n👋 Temperature monitoring stopped")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
