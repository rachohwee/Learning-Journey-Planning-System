from subprocess import check_output
from webbrowser import get
from flask import Flask, session, jsonify, request
from app import db

# Learning Journey Table
class LearningJourney(db.Model):
    __table_name__ = "learning_journey"

    lj_id = db.Column(db.Integer, primary_key=True, nullable=False)
    staff_id = db.Column(db.Integer, nullable=False)
    role_id = db.Column(db.Integer, nullable=False)
    skill_id = db.Column(db.Integer, nullable=False)
    is_learningjourney_completed = db.Column(db.Boolean, nullable=False)

    def __init__(self, lj_id, staff_id, role_id, skill_id, is_learningjourney_completed):
        self.lj_id = lj_id
        self.staff_id = staff_id
        self.role_id = role_id
        self.skill_id = skill_id
        self.is_learningjourney_completed = is_learningjourney_completed

    def json(self):
        return {
            "lj_id": self.lj_id, 
            "staff_id": self.staff_id, 
            "role_id": self.role_id, 
            "skill_id": self.skill_id, 
            "is_learningjourney_completed": self.is_learningjourney_completed
        }

# Learning Journey Course Table
class LearningJourneyCourse(db.Model):
    __table_name__ = "learning_journey_course"

    ljc_id = db.Column(db.Integer, primary_key=True, nullable=False)
    lj_id = db.Column(db.Integer, nullable=False)
    course_id = db.Column(db.String(20), nullable=False)
    completion_status = db.Column(db.String(20), nullable=False)
    reg_status = db.Column(db.String(20), nullable=False)

    def __init__(self, ljc_id, lj_id, course_id, completion_status, reg_status):
        self.ljc_id = ljc_id
        self.lj_id = lj_id
        self.course_id = course_id
        self.completion_status = completion_status
        self.reg_status = reg_status

    def json(self):
        return {"ljc_id": self.ljc_id, 
        "lj_id": self.lj_id, 
        "course_id": self.course_id, 
        "completion_status": self.completion_status, 
        "reg_status": self.reg_status
    }

# Save into the Learning Journey Table
def save_learning_journey(staff_id):
    try:
        role_id = request.json.get('role_id', None)
        skill_id = request.json.get('skill_id', None)
        selected_course_id = request.json.get('selected_course_id', None)

        if len(selected_course_id) == 0:
            return jsonify(
                {
                    "code": 400,
                    "message": "Please select at least one course to save into your learning journey."
                }
            ), 500

        selected_course_id = selected_course_id.split(",")

        # retrive those learning journey rows with the same staff, role, skill
        learning_journey_info = LearningJourney.query.filter_by(staff_id=staff_id, role_id=role_id, skill_id=skill_id).all()

        if (len(learning_journey_info)):
            for info in learning_journey_info:
                # retrive the id
                info_lj_id = info.lj_id
                # retrieve those learning journey course rows with the lj_id
                lj_course_info = LearningJourneyCourse.query.filter_by(
                    lj_id=info_lj_id)
                course_in_lj = []
                for ljc in lj_course_info:
                    course_in_lj.append(ljc.course_id)

                if len(course_in_lj) == len(selected_course_id):
                    for course_exist in course_in_lj:
                        for course_pick in selected_course_id:
                            if course_exist == course_pick:
                                return jsonify(
                                    {
                                        "code": 400,
                                        "message": "There is a saved learning journey with the same role, skill and course."

                                    }
                                ), 500

        learning_journey = LearningJourney(None, staff_id=staff_id, role_id=role_id, skill_id=skill_id, is_learningjourney_completed=False)

        db.session.add(learning_journey)
        db.session.commit()

        # get the id of the newly created learning journey
        lj_id = learning_journey.lj_id

        for course_id in selected_course_id:
            # print(course_id)
            learning_journey_course = LearningJourneyCourse(
                None, lj_id=lj_id, course_id=course_id, completion_status="Not Started", reg_status="Not Registered")

            db.session.add(learning_journey_course)
            db.session.commit()

        return jsonify(
            {
                "code": 200,
                "message": "Learning Journey has been saved."
            }
        )
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "skills.py internal error: " + str(e)
            }
        )


# find learning journey by staff_id
def get_lj_by_id(staff_id):
    try:
        ljlist = LearningJourney.query.filter_by(staff_id=staff_id).all()

        if len(ljlist):
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "learning_journey": [learningjourney.json() for learningjourney in ljlist]
                    }
                }
            )
        return jsonify(
            {
                "code": 404,
                "message": "This staff has no learning journey."
            }
        )
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "Get Learning Journeys by Staff ID internal error: " + str(e)
            }
        )

# Find learning journye by lj_id
def find_by_lj_id(lj_id):
    try:
        learningjourney = LearningJourney.query.filter_by(lj_id=lj_id).first()
        if learningjourney:
            return jsonify(
                {
                    "code": 200,
                    "data": learningjourney.json()
                }
            )
        return jsonify(
            { 
                "code": 404,
                "message": "Learning Journey not found."
            }
        )
    
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "Find Learning Journey ID internal error: " + str(e)
            }
        )

# retrieve all courses under a learning journey
def get_courses_under_learningjourney(lj_id):
    try:
        lj_course_list = LearningJourneyCourse.query.filter_by(lj_id=lj_id).all()
        if len(lj_course_list):
            return jsonify(
                {
                    "code": 200, 
                    "data": {
                        "learning_journey_course": [learningjourneycourse.json() for learningjourneycourse in lj_course_list]
                    }
                }
            )
        return jsonify(
            {
                "code": 404, 
                "message": "There is no course in this learning journey."
            }
        )
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "Get Learning Journeys by Staff ID internal error: " +str(e)
            }
        )

def delete_ljc_by_id(lj_id, ljc_id):
    try:

        # Get all the records with a particular lj_id in the Learning Journey Course table
        ljlist = LearningJourneyCourse.query.filter_by(lj_id=lj_id).all()

        # print(len(ljlist))

        if len(ljlist) > 1:
            try:
                ljc = LearningJourneyCourse.query.filter_by(
                    ljc_id=ljc_id).first()

                if ljc:
                    try:
                        db.session.delete(ljc)
                        db.session.commit()

                        return jsonify(
                            {
                                "code": 200,
                                "message": "Course has been removed from Learning Journey."
                            }
                        ), 200

                    except:
                        return jsonify(
                            {
                                "code": 500,
                                "data": {
                                    "ljc_id": ljc_id
                                },
                                "message": "An error occurred while removing the course from the learning journey"
                            }
                        ), 500

                # The ljc_id does not exist
                return jsonify(
                    {
                        "code": 404,
                        "data": {
                            "ljc_id": ljc_id
                        },
                        "message": "Learning Journey Course not found."
                    }
                ), 404

            except Exception as e:
                return jsonify(
                    {
                        "code": 500,
                        "message": "Delete Learning Journey Course internal error: " + str(e)
                    }
                ), 500

        if len(ljlist) == 1:
            return jsonify(
                {
                    "code": 400,
                    "data": {
                        "ljc_id": ljc_id
                    },
                    "message": "Course can't be removed from Learning Journey as there is only one course left in the Learning Journey."
                }
            ), 400
        
        return jsonify(
            {
                "code": 404,
                "message": "There is no course assigned to this learning journey."
            }
        )

    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "Delete Learning Joruney Course internal error: " + str(e)
            }
        ), 500


def get_learning_journey_details(lj_id):
    try:
        # Check if the role_id already exists in the role table
        lj_details = LearningJourney.query.filter_by(lj_id=lj_id).first()

        if lj_details:
            # The role_id exist
            return jsonify(
                {
                    # Return role's information in JSON with HTTP status code 200 - Ok
                    "code": 200,
                    "data": lj_details.json()
                }
            )

        # The role_id does not exist
        return jsonify(
            {
                "code": 404,
                "data": {
                    "lj_id": lj_id
                },
                "message": "Learning Journey not found."
            }
        )

    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "Get Learning Details by lj_id internal error: " + str(e)
            }
        )

#get all courses not added into learning journey
def getLJCoursesNotYetAdded(lj_id):
    try:
        lj = LearningJourney.query.filter_by(lj_id=lj_id).first()
        lj_course_list = LearningJourneyCourse.query.filter_by(lj_id=lj_id)
        if len(lj_course_list):
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "course": [course.json() for course in lj_course_list]
                    }
                }
            )
        return jsonify(
            {
                "code": 404,
                "message": "There are no course in this learning journey."
            }
        )
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": "Get Courses by Learning Journey and Skill ID internal error: " +str(e)
        })

def get_single_course_by_lj(lj_id, course_id):
    try:
        course = LearningJourneyCourse.query.filter_by(lj_id=lj_id, course_id=course_id).first()
        if course:
            return jsonify(
                {
                    "code": 200,
                    "data": course.json()
                }
            )
        return jsonify(
        {
            # Return role_id and error message in JSON with HTTP status code 404 - Not Found
            "code": 404,
            "data": {
                "lj_id": lj_id,
                "course_id": course_id
            },
            "message": "Course not found in Learning Journey."
        })
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "LearningJourney.py isCourseInLj internal error: " + str(e)
            }
        )

def isCourseInLJ(lj_id, course_id):
    try:
        acquried = LearningJourneyCourse.query.filter_by(lj_id=lj_id, course_id=course_id).first()
        if acquried:
           return True
        return False
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "LearningJourney.py is course in Learning Journey internal error: " + str(e)
            }
        )

def add_course_to_lj(lj_id, selected_course_id, completion_status, reg_status):
    try:
        if len(selected_course_id) == 0:
            return jsonify(
                {
                    "code": 400,
                    "message": "Please select at least one course to save into your learning journey."
                }
            ), 500

        selected_course_id = selected_course_id.split(",")
        index = 0 
        for course_id in selected_course_id:
            learning_journey_course = LearningJourneyCourse(
                None, lj_id=lj_id, course_id=course_id, completion_status=completion_status[index], reg_status=reg_status[index])
            db.session.add(learning_journey_course)
            db.session.commit()
            index += 1

        return jsonify(
            {
                "code": 200,
                "message": "Courses has been Successfully Added to Learning Journey"
            }
        )
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "LearningJoruney.py internal error: " + str(e)
            }
        )

def delete_lj(lj_id):
    try:
        lj_getting_deleted = LearningJourney.query.filter_by(lj_id=lj_id).first()
        print(lj_getting_deleted)
        
        try:
            db.session.delete(lj_getting_deleted)
            db.session.commit()
        
        except:
            return jsonify(
            {
                "code": 500,
                "data": {             
                    "lj_id": lj_id
                },
                "message": "An error occured while deleting the learning journey."
            }
        ), 500

        return jsonify(
            {
                "code": 200,
                "data": lj_getting_deleted.json()          
            }
        ), 200
    
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "Delete learning journey internal error:" + str(e)
            }
        ), 500
 