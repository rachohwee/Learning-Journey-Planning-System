from webbrowser import get
from flask import Flask, jsonify
from app import db
import json

class SkillCourse(db.Model):
    __tablename__ = 'skill_course'

    sc_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    skill_id = db.Column(db.Integer, nullable=False)
    course_id = db.Column(db.String(20), nullable=False)

    def __init__(self, sc_id, skill_id, course_id):
        self.sc_id = sc_id
        self.skill_id = skill_id
        self.course_id = course_id
    
    def json(self):
         return {
            "sc_id": self.sc_id, 
            "skill_id": self.skill_id, 
            "course_id": self.course_id
         }

def get_assigned_skills_by_id(course_id):
    try: 
        skillCourseList = SkillCourse.query.filter_by(course_id=course_id).all()
        if len(skillCourseList):
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "skill_course": [skillCourse.json() for skillCourse in skillCourseList]
                    }
                }
            ) 
        
        return jsonify(
            {
                "code": 404,
                "message": "No skill is assigned to this course."
            }
        )
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "Get assigned skills by Course ID internal error: " + str(e)
            }
        )

def get_sc_id(skill_id, course_id):
    try:
        skillCourse = SkillCourse.query.filter_by(course_id=course_id, skill_id=skill_id).first()

        if skillCourse:

            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "skill_course": skillCourse.json()
                    }
                }
            )
        return jsonify(
            {
                "code": 404,
                "message": "There is no assignment between this skill and course."
            }
        )
    except Exception as e:
        return jsonify (
            {
                "code": 500,
                "message": "Get assignment ID internal error: " +str(e)

            }
        )

def create_new_sc(skill_id, course_id):
    try:
        skillCourse = get_sc_id(skill_id, course_id).json
        #print(skillCourse)
        if skillCourse["code"] == 200:
            return jsonify(
                {
                    "code": 400,
                    "data": {
                        "sc_id": skillCourse["data"]["skill_course"]["sc_id"]
                    },
                    "message": "The skill is assigned to the course already."
                }
            ), 400

        skillCourse = SkillCourse(sc_id=None, skill_id=skill_id, course_id=course_id)

        try:
            db.session.add(skillCourse)
            db.session.commit()
        except:
            return jsonify(
                {
                    "code": 500,
                    "data": {                   
                        "skill_id": skill_id,
                        "course_id": course_id
                    },
                    "message": "An error occured while creating the assignment of the skill to the course."
                }
            ), 500
        
        return jsonify(
            {
                "code": 201,
                "data": skillCourse.json()
            }
        ), 201

    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "Create New Record internal error:" + str(e)
            }
        ), 500

def remove_assigned_sc(skill_id, course_id):
    try: 
        skillCourse = SkillCourse.query.filter_by(course_id=course_id, skill_id=skill_id).first()
        
        try:
            db.session.delete(skillCourse)
            db.session.commit()
        
        except:
            return jsonify(
                {
                    "code": 500,
                    "data": {             
                        "skill_id": skill_id,
                        "course_id": course_id
                    },
                    "message": "An error occured while removing the skill from the course."
                }
            ), 500
        
        return jsonify(
            {
                "code": 200,
                "data": skillCourse.json()          
            }
        ), 200

    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "Remove Record internal error:" + str(e)
            }
        ), 500
        
        
def get_courses_for_a_skill(skill_id):
    try: 
        course_of_skills = SkillCourse.query.filter_by(skill_id=skill_id).all()       
        #print(len(course_of_skills))

        if len(course_of_skills):
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "skill_course": [course_skill.json() for course_skill in course_of_skills]
                    }
                }
            ) 
        
        return jsonify(
            {
                "code": 404,
                "message": "There are no courses available for this skill. Please select another skill.",
            }
        )
        
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "Get assigned skills by Course ID internal error: " + str(e)
            }
        )
