def calculate_oee(availability: float, performance: float, quality: float) -> float:
    
    for name, value in [("availability", availability),
                        ("performance", performance),
                        ("quality", quality)]:
        if not (0.0 <= value <= 1.0):
            raise ValueError(f"{name} must be between 0.0 and 1.0, got {value}")

    return round(availability * performance * quality, 4)


def calculate_cycle_time(total_time_seconds: float, units_produced: int) -> float:
   
    if total_time_seconds < 0:
        raise ValueError("total_time_seconds cannot be negative")
    if units_produced <= 0:
        raise ValueError("units_produced must be greater than zero")

    return round(total_time_seconds / units_produced, 2)


def calculate_defect_rate(defective_units: int, total_units: int) -> float:
   
    if total_units <= 0:
        raise ValueError("total_units must be greater than zero")
    if defective_units < 0:
        raise ValueError("defective_units cannot be negative")
    if defective_units > total_units:
        raise ValueError("defective_units cannot exceed total_units")

    return round((defective_units / total_units) * 100, 2)


def calculate_throughput(units_produced: int, time_period_hours: float) -> float:
  
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