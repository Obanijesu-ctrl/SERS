"""
Seeds a minimal demo dataset so the app is immediately usable after
`flask run` 

Default login (created only if it doesn't already exist):
    username: admin
    password: admin123
"""
from app.extensions import db
from app.models.user import User
from app.models.energy import Community, EnergySource


def seed_defaults():
    if not User.query.filter_by(username="admin").first():
        admin = User(username="admin", email="admin@sers.local", role="admin")
        admin.set_password("admin123")
        db.session.add(admin)

    if Community.query.count() == 0:
        kiyovu = Community(name="Kiyovu Cell", district="Nyarugenge, Kigali", demand_kw=40.0)
        agatare = Community(name="Agatare Cell", district="Nyarugenge, Kigali", demand_kw=55.0)
        db.session.add_all([kiyovu, agatare])
        db.session.flush()  # get IDs before creating sources

        db.session.add_all([
            EnergySource(community_id=kiyovu.id, source_type="solar",
                         output_kw=45.0, capacity_kw=60.0),
            EnergySource(community_id=kiyovu.id, source_type="battery",
                         output_kw=30.0, capacity_kw=30.0, charge_pct=85.0),
            EnergySource(community_id=kiyovu.id, source_type="grid",
                         output_kw=100.0, capacity_kw=100.0),

            EnergySource(community_id=agatare.id, source_type="solar",
                         output_kw=20.0, capacity_kw=60.0),
            EnergySource(community_id=agatare.id, source_type="battery",
                         output_kw=15.0, capacity_kw=30.0, charge_pct=15.0),
            EnergySource(community_id=agatare.id, source_type="grid",
                         output_kw=100.0, capacity_kw=100.0),
        ])

    db.session.commit()
