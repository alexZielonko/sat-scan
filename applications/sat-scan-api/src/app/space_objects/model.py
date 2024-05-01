from app import db

class SpaceObject(db.Model):
  __tablename__ = 'space_objects_catalog'

  sat_id = db.Column(db.String(128), nullable=False, primary_key=True)
  sat_catalog_number = db.Column(db.String(128), nullable=False)
  sat_name = db.Column(db.String(128), nullable=False)
  file_id = db.Column(db.String(128), nullable=False)
  launch_country = db.Column(db.String(128), nullable=False)
  launch_site = db.Column(db.String(128), nullable=False)
  launch_date = db.Column(db.String(128), nullable=False)
  launch_year = db.Column(db.String(128), nullable=False)
  launch_number = db.Column(db.String(128), nullable=False)
  launch_piece = db.Column(db.String(128), nullable=False)
  object_type = db.Column(db.String(128), nullable=False)
  object_name = db.Column(db.String(128), nullable=False)
  object_id = db.Column(db.String(128), nullable=False)
  object_number = db.Column(db.String(128), nullable=False)

  date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
  date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                          onupdate=db.func.current_timestamp())
