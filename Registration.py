from flask import Flask, jsonify, request
from app import db

class Registration(db.Model):
    __tablename__ = 'registration'
    __table_args__ = {'extend_existing': True}

    reg_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.String(20), nullable=False)
    staff_id = db.Column(db.Integer, nullable=False)
    reg_status = db.Column(db.String(20), nullable=False)
    completion_status = db.Column(db.String(20), nullable=False)

    def __init__(self, reg_id, course_id, staff_id, reg_status, completion_status):
        self.reg_id = reg_id
        self.course_id = staff_id
        self.staff_id = course_id
        self.reg_status = reg_status
        self.completion_status = completion_status

    def json(self):
        dto = {
            'reg_id': self.reg_id,
            'course_id': self.course_id,
            'staff_id': self.staff_id,
            'reg_status': self.reg_status,
            'completion_status': self.completion_status
        }
        return dto
    
    
def get_completion_reg_status(staff_id, course_id):
    try:
        registration_details = Registration.query.filter_by(staff_id=staff_id, course_id=course_id).all()
        
        #print(registration_details)
        
        if len(registration_details):
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "reg_detail": [reg_detail.json() for reg_detail in registration_details]
                    }
                }
            ) 
        
        return jsonify(
            {
                "code": 201,
                "completion_status": "Not Started",
                "reg_status": "Not Registered"
            }
        )
        
        
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "Retrieving registration details error: " + str(e)
            }
        )
    
    