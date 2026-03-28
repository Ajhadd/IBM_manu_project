import unittest
import sys
import os

# Make the parent directory importable when running tests directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from manufacturing_calc import (
    calculate_oee,
    calculate_cycle_time,
    calculate_defect_rate,
    calculate_throughput,
    estimate_production_cost,
)


# ---------------------------------------------------------------------------
# OEE Tests
# ---------------------------------------------------------------------------
class TestCalculateOEE(unittest.TestCase):
    """Tests for Overall Equipment Effectiveness calculation."""

    def test_world_class_oee(self):
        """World-class OEE (≥ 85%) should be calculated correctly."""
        result = calculate_oee(0.90, 0.95, 0.99)
        self.assertAlmostEqual(result, 0.8464, places=4)

    def test_perfect_oee(self):
        """All factors at 100% should yield OEE of 1.0."""
        self.assertEqual(calculate_oee(1.0, 1.0, 1.0), 1.0)

    def test_zero_oee_on_any_zero_factor(self):
        """If any factor is zero, OEE must be zero."""
        self.assertEqual(calculate_oee(0.0, 0.95, 0.99), 0.0)
        self.assertEqual(calculate_oee(0.90, 0.0, 0.99), 0.0)
        self.assertEqual(calculate_oee(0.90, 0.95, 0.0), 0.0)

    def test_typical_factory_oee(self):
        """Typical factory scenario: 73% availability, 80% performance, 98% quality."""
        result = calculate_oee(0.73, 0.80, 0.98)
        self.assertAlmostEqual(result, 0.5723, places=4)

    def test_oee_raises_on_availability_above_1(self):
        """Availability > 1.0 is physically impossible; should raise ValueError."""
        with self.assertRaises(ValueError):
            calculate_oee(1.1, 0.9, 0.9)

    def test_oee_raises_on_negative_performance(self):
        """Negative performance is invalid; should raise ValueError."""
        with self.assertRaises(ValueError):
            calculate_oee(0.9, -0.1, 0.9)

    def test_oee_raises_on_quality_above_1(self):
        """Quality > 1.0 is invalid; should raise ValueError."""
        with self.assertRaises(ValueError):
            calculate_oee(0.9, 0.9, 1.5)


# ---------------------------------------------------------------------------
# Cycle Time Tests
# ---------------------------------------------------------------------------
class TestCalculateCycleTime(unittest.TestCase):
    """Tests for cycle time per unit calculation."""

    def test_standard_cycle_time(self):
        """3 600 s to make 100 units → 36 s/unit."""
        self.assertEqual(calculate_cycle_time(3600, 100), 36.0)

    def test_fractional_cycle_time(self):
        """Verify correct rounding for non-integer results."""
        result = calculate_cycle_time(1000, 3)
        self.assertAlmostEqual(result, 333.33, places=2)

    def test_single_unit(self):
        """Cycle time for a single unit equals total time."""
        self.assertEqual(calculate_cycle_time(250.5, 1), 250.5)

    def test_high_volume_line(self):
        """High-speed line: 1 hour producing 7 200 units → 0.5 s/unit."""
        self.assertEqual(calculate_cycle_time(3600, 7200), 0.5)

    def test_raises_on_zero_units(self):
        """Division by zero units must raise ValueError."""
        with self.assertRaises(ValueError):
            calculate_cycle_time(3600, 0)

    def test_raises_on_negative_units(self):
        """Negative unit count is nonsensical; should raise ValueError."""
        with self.assertRaises(ValueError):
            calculate_cycle_time(3600, -10)

    def test_raises_on_negative_time(self):
        """Negative production time is invalid; should raise ValueError."""
        with self.assertRaises(ValueError):
            calculate_cycle_time(-100, 50)

    def test_zero_time_allowed(self):
        """Zero production time is technically valid (instantaneous); returns 0.0."""
        self.assertEqual(calculate_cycle_time(0, 10), 0.0)


# ---------------------------------------------------------------------------
# Defect Rate Tests
# ---------------------------------------------------------------------------
class TestCalculateDefectRate(unittest.TestCase):
    """Tests for defect / rejection rate calculation."""

    def test_no_defects(self):
        """Zero defects → 0.00% defect rate."""
        self.assertEqual(calculate_defect_rate(0, 500), 0.0)

    def test_all_defective(self):
        """All units defective → 100.00% defect rate."""
        self.assertEqual(calculate_defect_rate(200, 200), 100.0)

    def test_typical_defect_rate(self):
        """5 bad parts out of 200 → 2.50%."""
        self.assertEqual(calculate_defect_rate(5, 200), 2.5)

    def test_six_sigma_level(self):
        """Six-sigma quality: 3 defects per million. Result rounds to near zero."""
        result = calculate_defect_rate(3, 1_000_000)
        self.assertAlmostEqual(result, 0.0, places=2)   # 0.0003% rounds to 0.00 at 2dp

    def test_raises_on_zero_total(self):
        """Cannot compute rate with zero total units."""
        with self.assertRaises(ValueError):
            calculate_defect_rate(0, 0)

    def test_raises_when_defects_exceed_total(self):
        """More defects than total units is logically impossible."""
        with self.assertRaises(ValueError):
            calculate_defect_rate(150, 100)

    def test_raises_on_negative_defects(self):
        """Negative defect count is invalid."""
        with self.assertRaises(ValueError):
            calculate_defect_rate(-5, 100)


# ---------------------------------------------------------------------------
# Throughput Tests
# ---------------------------------------------------------------------------
class TestCalculateThroughput(unittest.TestCase):
    """Tests for production throughput calculation."""

    def test_standard_throughput(self):
        """480 units over 8 hours → 60 units/hour."""
        self.assertEqual(calculate_throughput(480, 8), 60.0)

    def test_fractional_hours(self):
        """100 units in 2.5 hours → 40 units/hour."""
        self.assertEqual(calculate_throughput(100, 2.5), 40.0)

    def test_zero_units(self):
        """No production → 0 units/hour."""
        self.assertEqual(calculate_throughput(0, 8), 0.0)

    def test_raises_on_zero_time(self):
        """Division by zero hours must raise ValueError."""
        with self.assertRaises(ValueError):
            calculate_throughput(100, 0)

    def test_raises_on_negative_time(self):
        """Negative time period is invalid."""
        with self.assertRaises(ValueError):
            calculate_throughput(100, -2)

    def test_raises_on_negative_units(self):
        """Negative unit count is invalid."""
        with self.assertRaises(ValueError):
            calculate_throughput(-10, 8)


# ---------------------------------------------------------------------------
# Production Cost Tests
# ---------------------------------------------------------------------------
class TestEstimateProductionCost(unittest.TestCase):
    """Tests for production cost estimation."""

    def test_basic_cost_calculation(self):
        """
        100 units × $5.00 material + 8 h × $25.00 labor + 15% overhead
        Material = $500, Labor = $200, Overhead = $105 → Total = $805.00
        """
        result = estimate_production_cost(
            units=100,
            material_cost_per_unit=5.00,
            labor_cost_per_hour=25.00,
            hours=8,
            overhead_rate=0.15,
        )
        self.assertEqual(result, 805.0)

    def test_zero_overhead(self):
        """No overhead: cost is purely material + labor."""
        result = estimate_production_cost(
            units=10,
            material_cost_per_unit=10.0,
            labor_cost_per_hour=20.0,
            hours=5,
            overhead_rate=0.0,
        )
        # 10×$10 + 5×$20 = $100 + $100 = $200
        self.assertEqual(result, 200.0)

    def test_default_overhead_rate(self):
        """Default overhead rate is 15%."""
        result = estimate_production_cost(
            units=50,
            material_cost_per_unit=2.0,
            labor_cost_per_hour=15.0,
            hours=4,
        )
        # Material=$100, Labor=$60, Direct=$160, Overhead=$24 → Total=$184
        self.assertEqual(result, 184.0)

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


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    unittest.main(verbosity=2)