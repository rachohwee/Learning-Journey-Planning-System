from flask import jsonify
from app import db

class StaffSkill(db.Model):
    __tablename__ = 'staff_skill'

    sk_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    skill_id = db.Column(db.Integer, nullable=False)
    staff_id = db.Column(db.Integer, nullable=False)

    def __init__(self, sk_id, skill_id, staff_id):
        self.sk_id = sk_id
        self.skill_id = skill_id 
        self.staff_id = staff_id

    def json(self):
        dto = {
            'sk_id': self.sk_id,
            'skill_id': self.skill_id,
            'staff_id': self.staff_id
        }
        return dto

def isSkillAcquiredByStaff(staff_id, skill_id):
    try:
        acquried = StaffSkill.query.filter_by(skill_id=skill_id, staff_id=staff_id).first()
        if acquried:
           return True
        return False
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "StaffSkill.py skill acquired by staff internal error: " + str(e)
            }
        )