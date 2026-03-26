import sys
from manufacturing_calc import (
    calculate_oee,
    calculate_cycle_time,
    calculate_defect_rate,
    calculate_throughput,
    estimate_production_cost,
)

PASS = "✅"
FAIL = "❌"
errors = []


def check(label: str, actual, expected, tolerance: float = 0.01):
    """Assert a computed value is within tolerance of the expected value."""
    ok = abs(actual - expected) <= tolerance
    status = PASS if ok else FAIL
    print(f"  {status} {label}: {actual} (expected ≈ {expected})")
    if not ok:
        errors.append(f"{label}: got {actual}, expected {expected}")


print("\n" + "="*60)
print("  Manufacturing CI/CD — Integration Smoke Test")
print("="*60)

# ── Scenario: Automotive stamping press, one 8-hour shift ──────────────────
print("\n📋 Scenario: Automotive Stamping Press — Day Shift\n")

# OEE
oee = calculate_oee(availability=0.87, performance=0.91, quality=0.996)
check("OEE", oee, 0.7885)

# Cycle time (28 800 s shift, 3 450 good parts)
ct = calculate_cycle_time(total_time_seconds=28_800, units_produced=3_450)
check("Cycle Time (s/unit)", ct, 8.35)

# Defect rate
dr = calculate_defect_rate(defective_units=14, total_units=3_464)
check("Defect Rate (%)", dr, 0.40)

# Throughput
tp = calculate_throughput(units_produced=3_450, time_period_hours=8)
check("Throughput (units/hr)", tp, 431.25)

# Production cost
cost = estimate_production_cost(
    units=3_450,
    material_cost_per_unit=1.85,
    labor_cost_per_hour=32.00,
    hours=8,
    overhead_rate=0.18,
)
check("Total Production Cost ($)", cost, 8_330.37, tolerance=1.0)

# ── Edge-case guards ────────────────────────────────────────────────────────
print("\n🔒 Edge-Case Guards\n")

def expect_error(label: str, fn, *args, **kwargs):
    try:
        fn(*args, **kwargs)
        print(f"  {FAIL} {label}: expected ValueError but none raised")
        errors.append(f"{label}: missing ValueError")
    except ValueError:
        print(f"  {PASS} {label}: ValueError raised correctly")

expect_error("OEE with availability > 1", calculate_oee, 1.1, 0.9, 0.9)
expect_error("Cycle time with 0 units",   calculate_cycle_time, 3600, 0)
expect_error("Defects exceed total",       calculate_defect_rate, 200, 100)
expect_error("Throughput with 0 hours",   calculate_throughput, 100, 0)
expect_error("Negative material cost",    estimate_production_cost, 10, -5.0, 20.0, 4)

# ── Summary ─────────────────────────────────────────────────────────────────
print("\n" + "="*60)
if errors:
    print(f"  {FAIL} SMOKE TEST FAILED — {len(errors)} error(s):")
    for e in errors:
        print(f"     • {e}")
    print("="*60 + "\n")
    sys.exit(1)
else:
    print(f"  {PASS} ALL SMOKE TESTS PASSED")
    print("="*60 + "\n")
    sys.exit(0)