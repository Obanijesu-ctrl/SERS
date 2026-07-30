from datetime import datetime
from app.extensions import db


class Community(db.Model):
    """A served community / cell (e.g. Kiyovu, Agatare) in Kigali."""
    __tablename__ = "communities"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    district = db.Column(db.String(120), default="Kigali")
    demand_kw = db.Column(db.Float, default=50.0)  # current household/community demand

    sources = db.relationship(
        "EnergySource", backref="community", cascade="all, delete-orphan"
    )
    logs = db.relationship(
        "RoutingLog", backref="community", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Community {self.name}>"


class EnergySource(db.Model):
    """
    One power source feeding a community: solar, battery, or grid.
    `is_active` lets an operator manually take a source offline
    (e.g. for maintenance) — the routing engine will skip inactive sources.
    """
    __tablename__ = "energy_sources"

    SOURCE_TYPES = ("solar", "battery", "grid")

    id = db.Column(db.Integer, primary_key=True)
    community_id = db.Column(db.Integer, db.ForeignKey("communities.id"), nullable=False)
    source_type = db.Column(db.String(20), nullable=False)  # solar | battery | grid
    output_kw = db.Column(db.Float, default=0.0)     # current available output
    capacity_kw = db.Column(db.Float, default=100.0)  # max rated output
    charge_pct = db.Column(db.Float, default=100.0)   # relevant for battery only
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<EnergySource {self.source_type} @ community {self.community_id}>"


class RoutingLog(db.Model):
    """
    An immutable record of a routing decision made by the engine.
    Used to populate the dashboard's activity feed and demo the
    "automated routing" requirement from the SRS.
    """
    __tablename__ = "routing_logs"

    id = db.Column(db.Integer, primary_key=True)
    community_id = db.Column(db.Integer, db.ForeignKey("communities.id"), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    selected_source = db.Column(db.String(20), nullable=False)
    reason = db.Column(db.String(255))
    solar_output_kw = db.Column(db.Float)
    battery_charge_pct = db.Column(db.Float)
    grid_available = db.Column(db.Boolean)

    def __repr__(self):
        return f"<RoutingLog {self.selected_source} @ {self.timestamp}>"
