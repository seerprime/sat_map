import json
import random
import os

# =========================
# CONFIG
# =========================
POINTS_COUNT = 200  # number of points per dataset
OUTPUT_DIR = "assets/mock_data"

# Bhubaneswar bounding box
LAT_MIN, LAT_MAX = 20.24, 20.36
LNG_MIN, LNG_MAX = 85.76, 85.88

# =========================
# GENERATORS
# =========================
def generate_trash_data(points=POINTS_COUNT):
    """Generate trash hotspot heatmap data."""
    return [
        {
            "lat": round(random.uniform(LAT_MIN, LAT_MAX), 6),
            "lng": round(random.uniform(LNG_MIN, LNG_MAX), 6),
            "intensity": round(random.uniform(0.6, 0.98), 2),
            "type": "trash"
        }
        for _ in range(points)
    ]

def generate_water_quality(points=POINTS_COUNT):
    """Generate water contamination data."""
    qualities = ["good", "moderate", "poor", "critical"]
    weights = [0.2, 0.3, 0.35, 0.15]  # probability distribution
    return [
        {
            "lat": round(random.uniform(LAT_MIN, LAT_MAX), 6),
            "lng": round(random.uniform(LNG_MIN, LNG_MAX), 6),
            "quality": random.choices(qualities, weights=weights, k=1)[0],
            "contamination": round(random.uniform(0.3, 0.95), 2)
        }
        for _ in range(points)
    ]

def generate_disease_risk(points=POINTS_COUNT):
    """Generate disease risk heatmap data."""
    levels = ["low", "medium", "high", "critical"]
    weights = [0.25, 0.35, 0.3, 0.1]
    return [
        {
            "lat": round(random.uniform(LAT_MIN, LAT_MAX), 6),
            "lng": round(random.uniform(LNG_MIN, LNG_MAX), 6),
            "risk_level": random.choices(levels, weights=weights, k=1)[0],
            "risk_score": round(random.uniform(0.4, 0.97), 2)
        }
        for _ in range(points)
    ]

# =========================
# MAIN SCRIPT
# =========================
if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    datasets = {
        "heatmap_data.json": generate_trash_data(),
        "water_quality.json": generate_water_quality(),
        "disease_risk.json": generate_disease_risk()
    }

    for filename, data in datasets.items():
        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
        print(f"✅ Generated {filepath} ({len(data)} points)")

    print("\n🚀 All mock datasets generated successfully for Bhubaneswar!")
