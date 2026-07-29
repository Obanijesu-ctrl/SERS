from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from app.extensions import db
from app.models.energy import Community, EnergySource, RoutingLog
from app.routing_engine import route_community

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@login_required
def home():
    communities = Community.query.all()
    # Route every community fresh each time the dashboard loads, so the
    # page always reflects a live decision (this simulates the automated
    # routing cycle described in the SRS).
    latest_logs = {c.id: route_community(c) for c in communities}
    return render_template(
        "dashboard.html", communities=communities, latest_logs=latest_logs
    )


@dashboard_bp.route("/community/<int:community_id>")
@login_required
def community_detail(community_id):
    community = Community.query.get_or_404(community_id)
    history = (
        RoutingLog.query.filter_by(community_id=community.id)
        .order_by(RoutingLog.timestamp.desc())
        .limit(20)
        .all()
    )
    return render_template("community.html", community=community, history=history)


@dashboard_bp.route("/source/<int:source_id>/toggle", methods=["POST"])
@login_required
def toggle_source(source_id):
    source = EnergySource.query.get_or_404(source_id)
    source.is_active = not source.is_active
    db.session.commit()
    flash(
        f"{source.source_type.title()} source for "
        f"{source.community.name} is now "
        f"{'ACTIVE' if source.is_active else 'INACTIVE'}.",
        "success",
    )
    return redirect(url_for("dashboard.community_detail", community_id=source.community_id))
