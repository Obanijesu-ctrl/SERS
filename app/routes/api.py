from flask import Blueprint, jsonify
from flask_login import login_required

from app.models.energy import Community
from app.routing_engine import route_community

api_bp = Blueprint("api", __name__)


@api_bp.route("/communities")
@login_required
def list_communities():
    communities = Community.query.all()
    return jsonify([
        {
            "id": c.id,
            "name": c.name,
            "district": c.district,
            "demand_kw": c.demand_kw,
            "sources": [
                {
                    "type": s.source_type,
                    "output_kw": s.output_kw,
                    "charge_pct": s.charge_pct,
                    "is_active": s.is_active,
                }
                for s in c.sources
            ],
        }
        for c in communities
    ])


@api_bp.route("/communities/<int:community_id>/route", methods=["POST"])
@login_required
def trigger_routing(community_id):
    community = Community.query.get_or_404(community_id)
    log = route_community(community)
    return jsonify({
        "community": community.name,
        "selected_source": log.selected_source,
        "reason": log.reason,
        "timestamp": log.timestamp.isoformat(),
    })
