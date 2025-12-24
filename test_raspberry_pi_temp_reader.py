#!/usr/bin/env python3
"""
Unit tests for Raspberry Pi 5 Temperature Reader

These tests validate the core functionality of the temperature reader.
Run with: python3 test_raspberry_pi_temp_reader.py
"""

import unittest
import sys
import os

# Add the current directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from raspberry_pi_temp_reader import RaspberryPiTempReader


class TestRaspberryPiTempReader(unittest.TestCase):
    """Test cases for RaspberryPiTempReader class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.reader = RaspberryPiTempReader()
    
    def test_celsius_to_fahrenheit_conversion(self):
        """Test temperature conversion from Celsius to Fahrenheit"""
        # Test freezing point
        self.assertEqual(self.reader.celsius_to_fahrenheit(0), 32.0)
        
        # Test boiling point
        self.assertEqual(self.reader.celsius_to_fahrenheit(100), 212.0)
        
        # Test typical Raspberry Pi temperature
        self.assertAlmostEqual(self.reader.celsius_to_fahrenheit(50), 122.0, places=1)
        
        # Test negative temperature
        self.assertAlmostEqual(self.reader.celsius_to_fahrenheit(-40), -40.0, places=1)
    
    def test_temp_status_cool(self):
        """Test temperature status for cool temperatures"""
        status = self.reader._get_temp_status(45)
        self.assertIn("Cool", status)
    
    def test_temp_status_normal(self):
        """Test temperature status for normal temperatures"""
        status = self.reader._get_temp_status(55)
        self.assertIn("Normal", status)
    
    def test_temp_status_warm(self):
        """Test temperature status for warm temperatures"""
        status = self.reader._get_temp_status(65)
        self.assertIn("Warm", status)
    
    def test_temp_status_hot(self):
        """Test temperature status for hot temperatures"""
        status = self.reader._get_temp_status(75)
        self.assertIn("Hot", status)
    
    def test_temp_status_very_hot(self):
        """Test temperature status for very hot temperatures"""
        status = self.reader._get_temp_status(85)
        self.assertIn("Very Hot", status)
    
    def test_method_detection(self):
        """Test that method detection returns a valid method"""
        method = self.reader._detect_best_method()
        self.assertIn(method, ['vcgencmd', 'thermal_zone'])
    
    def test_get_temperature_returns_tuple(self):
        """Test that get_temperature returns a tuple"""
        result = self.reader.get_temperature()
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        
        temp, method = result
        # Temperature can be None if not on a Raspberry Pi
        if temp is not None:
            self.assertIsInstance(temp, float)
            self.assertGreater(temp, 0)  # Should be above absolute zero
            self.assertLess(temp, 120)  # Should be below a reasonable max
        
        self.assertIsInstance(method, str)
    
    def test_fahrenheit_conversion_accuracy(self):
        """Test accuracy of Fahrenheit conversion"""
        test_cases = [
            (0, 32),
            (10, 50),
            (20, 68),
            (30, 86),
            (40, 104),
            (50, 122),
        ]
        
        for celsius, expected_fahrenheit in test_cases:
            result = self.reader.celsius_to_fahrenheit(celsius)
            self.assertAlmostEqual(result, expected_fahrenheit, places=1)


class TestTemperatureReadingMethods(unittest.TestCase):
    """Test temperature reading methods"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.reader = RaspberryPiTempReader()
    
    def test_read_temp_thermal_zone_returns_float_or_none(self):
        """Test that thermal zone reading returns float or None"""
        result = self.reader.read_temp_thermal_zone()
        self.assertTrue(result is None or isinstance(result, float))
    
    def test_read_temp_vcgencmd_returns_float_or_none(self):
        """Test that vcgencmd reading returns float or None"""
        result = self.reader.read_temp_vcgencmd()
        self.assertTrue(result is None or isinstance(result, float))


def run_tests():
    """Run all tests and display results"""
    # Create a test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestRaspberryPiTempReader))
    suite.addTests(loader.loadTestsFromTestCase(TestTemperatureReadingMethods))
    
    # Run the tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    exit(run_tests())
