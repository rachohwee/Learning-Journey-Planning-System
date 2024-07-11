from flask import Flask, request, jsonify, abort, render_template
from app import db

class Course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.String(20), primary_key=True, nullable=False)
    course_name = db.Column(db.String(50), nullable=False)
    course_desc = db.Column(db.String(255), nullable=True)
    course_status = db.Column(db.String(15), nullable=True)
    course_type = db.Column(db.String(10), nullable=True)
    course_category = db.Column(db.String(50), nullable=False)

    def __init__(self, course_id, course_name, course_desc, course_status, course_type, course_category):
        self.course_id = course_id
        self.course_name = course_name 
        self.course_desc = course_desc
        self.course_status = course_status
        self.course_type = course_type
        self.course_category = course_category


    def json(self):
        return {
            "course_id": self.course_id, 
            "course_name": self.course_name, 
            "course_desc": self.course_desc, 
            "course_status": self.course_status, 
            "course_type": self.course_type, 
            "course_category": self.course_category
        }

def get_all_courses(): # get all courses that are "Active". | Active courses to be displayed only.
    try:
        #Retrieve all courses that are ACTIVE from the course table and store it as a list in the courselist
        courselist = Course.query.all()

        print(courselist)
        #Check if the doctorlist is empty 
        
        if len(courselist):
            #The doctorlist is not empty 
            return jsonify(
                {   
                    #Return the corresponding HTTP status code 200 and list of doctors in the JSON representation
                    "code" : 200,
                    "data" : {
                        "courses": [course.json() for course in courselist]
                    }
                }
            )

        #The doctorlist is empty 
        return jsonify(
            {
                #Return an error message in JSON and HTTP status code 404 - Not Found
                "code": 404,
                "message": "There are no courses."
            }
        )

    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "course.py internal error: " + str(e)
            }
        )

def get_active_courses(): # get all courses that are "Active". | Active courses to be displayed only.
    try:
        #Retrieve all courses that are ACTIVE from the course table and store it as a list in the courselist
        courselist = Course.query.filter_by(course_status='Active').all()

        print(courselist)
        #Check if the doctorlist is empty 
        
        if len(courselist):
            #The doctorlist is not empty 
            return jsonify(
                {   
                    #Return the corresponding HTTP status code 200 and list of doctors in the JSON representation
                    "code" : 200,
                    "data" : {
                        "courses": [course.json() for course in courselist]
                    }
                }
            )

        #The doctorlist is empty 
        return jsonify(
            {
                #Return an error message in JSON and HTTP status code 404 - Not Found
                "code": 404,
                "message": "There are no courses."
            }
        )

    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "course.py internal error: " + str(e)
            }
        )

def find_by_course_id(course_id):
    try:
        #Check if the course_id already exists in the role table 
        course = Course.query.filter_by(course_id=course_id).first()
        if course:
            #The course_id exist 
            return jsonify(
                {
                    #Return course's information in JSON with HTTP status code 200 - Ok
                    "code": 200,
                    "data": course.json()
                }
            )
            
        #The course_id does not exist 
        return jsonify(
            {
                #Return course_id and error message in JSON with HTTP status code 404 - Not Found 
                "code": 404,
                "data": {
                    "course_id": course_id
                },
                "message": "Course not found."
            }
        )
    
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "Find Course ID internal error: " + str(e)
            }
        )
