import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from manufacturing_calc import (
    calculate_oee,
    calculate_cycle_time,
    calculate_defect_rate,
    calculate_throughput,
    estimate_production_cost,
)


class TestCalculateOEE(unittest.TestCase):

    def test_world_class_oee(self):
        result = calculate_oee(0.90, 0.95, 0.99)
        self.assertAlmostEqual(result, 0.8464, places=4)

    def test_perfect_oee(self):
        self.assertEqual(calculate_oee(1.0, 1.0, 1.0), 1.0)

    def test_zero_oee(self):
        self.assertEqual(calculate_oee(0.0, 0.95, 0.99), 0.0)

    def test_typical_factory_oee(self):
        result = calculate_oee(0.73, 0.80, 0.98)
        self.assertAlmostEqual(result, 0.5723, places=4)

    def test_oee_raises_above_1(self):
        with self.assertRaises(ValueError):
            calculate_oee(1.1, 0.9, 0.9)

    def test_oee_raises_negative(self):
        with self.assertRaises(ValueError):
            calculate_oee(0.9, -0.1, 0.9)


class TestCalculateCycleTime(unittest.TestCase):

    def test_standard_cycle_time(self):
        self.assertEqual(calculate_cycle_time(3600, 100), 36.0)

    def test_fractional_cycle_time(self):
        result = calculate_cycle_time(1000, 3)
        self.assertAlmostEqual(result, 333.33, places=2)

    def test_single_unit(self):
        self.assertEqual(calculate_cycle_time(250.5, 1), 250.5)

    def test_raises_on_zero_units(self):
        with self.assertRaises(ValueError):
            calculate_cycle_time(3600, 0)

    def test_raises_on_negative_units(self):
        with self.assertRaises(ValueError):
            calculate_cycle_time(3600, -10)

    def test_raises_on_negative_time(self):
        with self.assertRaises(ValueError):
            calculate_cycle_time(-100, 50)


class TestCalculateDefectRate(unittest.TestCase):

    def test_no_defects(self):
        self.assertEqual(calculate_defect_rate(0, 500), 0.0)

    def test_all_defective(self):
        self.assertEqual(calculate_defect_rate(200, 200), 100.0)

    def test_typical_defect_rate(self):
        self.assertEqual(calculate_defect_rate(5, 200), 2.5)

    def test_raises_on_zero_total(self):
        with self.assertRaises(ValueError):
            calculate_defect_rate(0, 0)

    def test_raises_when_defects_exceed_total(self):
        with self.assertRaises(ValueError):
            calculate_defect_rate(150, 100)

    def test_raises_on_negative_defects(self):
        with self.assertRaises(ValueError):
            calculate_defect_rate(-5, 100)


class TestCalculateThroughput(unittest.TestCase):

    def test_standard_throughput(self):
        self.assertEqual(calculate_throughput(480, 8), 60.0)

    def test_fractional_hours(self):
        self.assertEqual(calculate_throughput(100, 2.5), 40.0)

    def test_zero_units(self):
        self.assertEqual(calculate_throughput(0, 8), 0.0)

    def test_raises_on_zero_time(self):
        with self.assertRaises(ValueError):
            calculate_throughput(100, 0)

    def test_raises_on_negative_time(self):
        with self.assertRaises(ValueError):
            calculate_throughput(100, -2)

    def test_raises_on_negative_units(self):
        with self.assertRaises(ValueError):
            calculate_throughput(-10, 8)


class TestEstimateProductionCost(unittest.TestCase):

    def test_basic_cost_calculation(self):
        result = estimate_production_cost(
            units=100,
            material_cost_per_unit=5.00,
            labor_cost_per_hour=25.00,
            hours=8,
            overhead_rate=0.15,
        )
        self.assertEqual(result, 805.0)

    def test_zero_overhead(self):
        result = estimate_production_cost(
            units=10,
            material_cost_per_unit=10.0,
            labor_cost_per_hour=20.0,
            hours=5,
            overhead_rate=0.0,
        )
        self.assertEqual(result, 200.0)

    def test_raises_on_negative_units(self):
        with self.assertRaises(ValueError):
            estimate_production_cost(-5, 10.0, 20.0, 4)

    def test_raises_on_negative_material_cost(self):
        with self.assertRaises(ValueError):
            estimate_production_cost(10, -5.0, 20.0, 4)

    def test_raises_on_negative_labor_cost(self):
        with self.assertRaises(ValueError):
            estimate_production_cost(10, 5.0, -20.0, 4)

    def test_raises_on_negative_hours(self):
        with self.assertRaises(ValueError):
            estimate_production_cost(10, 5.0, 20.0, -4)

    def test_raises_on_negative_overhead_rate(self):
        with self.assertRaises(ValueError):
            estimate_production_cost(10, 5.0, 20.0, 4, overhead_rate=-0.1)


if __name__ == "__main__":
    unittest.main(verbosity=2)