"""
Smart Energy Routing Engine
============================
This module implements the decision logic described in the SERS SRS:
given a community's current solar output, battery charge, and grid
availability, pick the source that meets demand at the lowest cost /
highest reliability, and log the decision.

Priority rules (simple, explainable — matches the "automated routing
between solar, battery, and grid" requirement):

  1. SOLAR   - if solar output alone can cover demand, use it (free, renewable).
  2. BATTERY - else if battery charge is above the safety floor, draw from
               battery (still free, avoids grid cost).
  3. GRID    - else fall back to the grid, if available.
  4. NONE    - if nothing can cover demand, flag a supply shortfall.

Sources marked `is_active = False` (manually disabled by an operator)
are skipped entirely, regardless of their output/charge.
"""
from app.extensions import db
from app.models.energy import EnergySource, RoutingLog

BATTERY_SAFETY_FLOOR_PCT = 20.0  # never drain battery below this


def route_community(community):
    """
    Decide which source should supply `community` right now.
    Returns the RoutingLog entry created (also persisted to the DB).
    """
    sources = {s.source_type: s for s in community.sources if s.is_active}
    demand = community.demand_kw

    solar = sources.get("solar")
    battery = sources.get("battery")
    grid = sources.get("grid")

    selected, reason = None, None

    if solar and solar.output_kw >= demand:
        selected, reason = "solar", (
            f"Solar output ({solar.output_kw:.1f}kW) covers demand ({demand:.1f}kW)."
        )
    elif battery and battery.charge_pct > BATTERY_SAFETY_FLOOR_PCT:
        selected, reason = "battery", (
            f"Solar insufficient; battery charge ({battery.charge_pct:.0f}%) "
            f"above safety floor ({BATTERY_SAFETY_FLOOR_PCT:.0f}%)."
        )
    elif grid:
        selected, reason = "grid", (
            "Solar and battery unavailable/insufficient; routing to grid."
        )
    else:
        selected, reason = "none", "No active source can currently meet demand."

    log = RoutingLog(
        community_id=community.id,
        selected_source=selected,
        reason=reason,
        solar_output_kw=solar.output_kw if solar else 0,
        battery_charge_pct=battery.charge_pct if battery else 0,
        grid_available=bool(grid),
    )
    db.session.add(log)
    db.session.commit()
    return log
