"""
manufacturing_calc.py
---------------------
Core manufacturing calculation functions for the AI-Enhanced CI/CD project.
These functions simulate real-world manufacturing metrics used on the factory floor.
"""


def calculate_oee(availability: float, performance: float, quality: float) -> float:
    """
    Calculate Overall Equipment Effectiveness (OEE).

    OEE is the gold standard for measuring manufacturing productivity.
    OEE = Availability × Performance × Quality

    Args:
        availability: Ratio of actual run time to planned production time (0.0 – 1.0)
        performance:  Ratio of actual output rate to ideal output rate   (0.0 – 1.0)
        quality:      Ratio of good units to total units produced         (0.0 – 1.0)

    Returns:
        OEE as a float between 0.0 and 1.0

    Raises:
        ValueError: if any argument is outside the [0, 1] range
    """
    for name, value in [("availability", availability),
                        ("performance", performance),
                        ("quality", quality)]:
        if not (0.0 <= value <= 1.0):
            raise ValueError(f"{name} must be between 0.0 and 1.0, got {value}")

    return round(availability * performance * quality, 4)


def calculate_cycle_time(total_time_seconds: float, units_produced: int) -> float:
    """
    Calculate the average cycle time per unit.

    Cycle Time = Total Production Time / Units Produced

    Args:
        total_time_seconds: Total elapsed production time in seconds
        units_produced:     Number of finished units produced

    Returns:
        Average cycle time per unit in seconds (rounded to 2 decimal places)

    Raises:
        ValueError: if units_produced <= 0 or total_time_seconds < 0
    """
    if total_time_seconds < 0:
        raise ValueError("total_time_seconds cannot be negative")
    if units_produced <= 0:
        raise ValueError("units_produced must be greater than zero")

    return round(total_time_seconds / units_produced, 2)


def calculate_defect_rate(defective_units: int, total_units: int) -> float:
    """
    Calculate the defect (rejection) rate as a percentage.

    Defect Rate (%) = (Defective Units / Total Units) × 100

    Args:
        defective_units: Count of units that failed quality inspection
        total_units:     Total units inspected

    Returns:
        Defect rate as a percentage (0.0 – 100.0), rounded to 2 decimal places

    Raises:
        ValueError: if either argument is negative or total_units is zero,
                    or if defective_units > total_units
    """
    if total_units <= 0:
        raise ValueError("total_units must be greater than zero")
    if defective_units < 0:
        raise ValueError("defective_units cannot be negative")
    if defective_units > total_units:
        raise ValueError("defective_units cannot exceed total_units")

    return round((defective_units / total_units) * 100, 2)


def calculate_throughput(units_produced: int, time_period_hours: float) -> float:
    """
    Calculate production throughput (units per hour).

    Throughput = Units Produced / Time Period

    Args:
        units_produced:     Total number of good units produced
        time_period_hours:  Duration of the production run in hours

    Returns:
        Throughput in units/hour, rounded to 2 decimal places

    Raises:
        ValueError: if either argument is non-positive
    """
    if units_produced < 0:
        raise ValueError("units_produced cannot be negative")
    if time_period_hours <= 0:
        raise ValueError("time_period_hours must be greater than zero")

    return round(units_produced / time_period_hours, 2)


def estimate_production_cost(units: int,
                             material_cost_per_unit: float,
                             labor_cost_per_hour: float,
                             hours: float,
                             overhead_rate: float = 0.15) -> float:
    """
    Estimate the total production cost for a batch.

    Total Cost = (Material Cost × Units) + (Labor Cost × Hours) + Overhead
    Overhead   = overhead_rate × (Material + Labor)

    Args:
        units:                  Number of units in the batch
        material_cost_per_unit: Raw-material cost per unit (USD)
        labor_cost_per_hour:    Labor cost per hour (USD)
        hours:                  Total labor hours for the batch
        overhead_rate:          Overhead as a fraction of direct costs (default 15%)

    Returns:
        Estimated total cost in USD, rounded to 2 decimal places

    Raises:
        ValueError: if any numeric argument is negative
    """
    for name, val in [("units", units),
                      ("material_cost_per_unit", material_cost_per_unit),
                      ("labor_cost_per_hour", labor_cost_per_hour),
                      ("hours", hours),
                      ("overhead_rate", overhead_rate)]:
        if val < 0:
            raise ValueError(f"{name} cannot be negative")

    material = material_cost_per_unit * units
    labor = labor_cost_per_hour * hours
    direct = material + labor
    overhead = overhead_rate * direct
    return round(direct + overhead, 2)