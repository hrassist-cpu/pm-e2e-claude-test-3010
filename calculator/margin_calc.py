"""Калькулятор маржі Christmas Reskin: python margin_calc.py [днів] [людей через кому]."""
import csv, sys
from pathlib import Path

RATE_CLIENT = 300.0          # $ за людино-день для клієнта (rate card)
LEAD_NORM_DAYS = 2           # норма ліда на локацію


def load_roster(path):
    with open(path, encoding="utf-8") as f:
        return {r["name"]: r for r in csv.DictReader(f)}


def margin(days, team, roster):
    revenue = days * RATE_CLIENT
    per_person = days / max(1, len(team))
    cost = 0.0
    for n in team:
        r = roster[n]
        cost += per_person * float(r["speed_factor"] or 1) * float(r["rate_per_day"])
    lead = roster.get("Ярік")
    if lead and "Ярік" not in team:
        cost += LEAD_NORM_DAYS * float(lead["rate_per_day"])
    return revenue, cost, (revenue - cost) / revenue * 100


if __name__ == "__main__":
    days = float(sys.argv[1]) if len(sys.argv) > 1 else 28
    names = sys.argv[2].split(",") if len(sys.argv) > 2 else ["Світлана", "Марія", "Олександр"]
    roster = load_roster(Path(__file__).parent / "data" / "roster.csv")
    rev, cost, m = margin(days, names, roster)
    print(f"Виручка ${rev:,.0f}, собівартість ${cost:,.0f}, маржа {m:.1f}%")
