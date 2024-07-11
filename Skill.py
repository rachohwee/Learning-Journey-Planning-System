from app import db
from distutils.log import error
from flask import Flask, request, jsonify, abort, render_template

# Table 1
class Skill(db.Model):
    __tablename__ = 'skill'

    skill_id = db.Column(db.Integer, primary_key=True, nullable=False)
    skill_name = db.Column(db.String(256), nullable=False)
    is_skill_deleted = db.Column(db.Boolean, nullable=False)

    def __init__(self, skill_id, skill_name, is_skill_deleted):
        self.skill_id = skill_id
        self.skill_name = skill_name
        self.is_skill_deleted = is_skill_deleted

    def json(self):
        return {
            "skill_id": self.skill_id, 
            "skill_name": self.skill_name, 
            "is_skill_deleted": self.is_skill_deleted
        }

# Retrieve all skill
def get_all_skills():
    try:
        # Retrieve all records from the skills table and store it as a list in the skill_list
        skill_list = Skill.query.all()
        print(len(skill_list))
        # Check if the skill_list is empty
        if len(skill_list):
            # The skill_list is not empty
            return jsonify(
                {
                    # Return the corresponding HTTP status code 200 and list of doctors in the JSON representation
                    "code": 200,
                    "data": {
                        "skills": [skill.json() for skill in skill_list]
                    }
                }
            )      
        return jsonify(
            {
                #Return an error message in JSON and HTTP status code 404 - Not Found
                "code": 404,
                "message": "There are no skills created yet."
            }
        )

    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "skill.py internal error: " + str(e)
            }
        )

# Add skill
def add_a_skill(skill_name):
    # print(skill_name)
    if (skill_name != ''):

        if (len(skill_name) <= 256 and len(skill_name) >= 3):
            try:
                # skill_name = skill_name.title()
                skill = Skill.query.filter_by(skill_name=skill_name).first()
                # print(skill)

                if skill:
                    #  if skill exists

                    # Return skill_name and an error message in JSON with HTTP status code 400 - Bad Request
                    return jsonify(
                        {
                            "code": 400,
                            "data": {
                                "skill_name": skill_name
                            },
                            "message": "Skill already exists. Unable to add skill."
                        }
                    )

                try:
                    #  if skill does not exists
                    skill = Skill(None, skill_name=skill_name,
                                  is_skill_deleted=False)
                    db.session.add(skill)
                    db.session.commit()

                except:
                    return jsonify(
                        {
                            "code": 500,
                            "data": {
                                "skill_name": skill_name
                            },
                            "message": "An error occurred creating the skill."
                        }
                    )

                return jsonify(
                    {
                        "code": 201,
                        "data": skill.json(),
                        "message": "Skill has been created."
                    }
                )

            except Exception as e:
                return jsonify(
                    {
                        "code": 500,
                        "message": "skills.py internal error: " + str(e)
                    }
                )

        elif (len(skill_name) < 3):
            return jsonify(
                        {
                            "code": 402,
                            "data": {
                                "skill_name": skill_name
                            },
                            "message": "Skill name must be more than 3 characters. Unable to create skill."
                        }
                    )
            
        elif (len(skill_name) > 256):
            return jsonify(
                        {
                            "code": 403,
                            "data": {
                                "skill_name": skill_name
                            },
                            "message": "Skill name must be less than 256 characters. Unable to create skill."
                        }
                    )

    else:
        return jsonify(
                    {
                        "code": 401,
                        "data": {
                            "skill_name": skill_name
                        },
                        "message": "Field required is empty. Unable to create skill."
                    }
                )

# Retrieve skill details based on ID
def find_by_skill_id(skill_id):
    try:
        #Check if the skill_id already exists in the skill table 
        skill = Skill.query.filter_by(skill_id=skill_id).first()
        if skill:
            #The skill_id exist 
            return jsonify(
                {
                    #Return skill's information in JSON with HTTP status code 200 - Ok
                    "code": 200,
                    "data": skill.json()
                }
            )
            
        #The skill_id does not exist 
        return jsonify(
            {
                #Return skill_id and error message in JSON with HTTP status code 404 - Not Found 
                "code": 404,
                "data": {
                    "skill_id": skill_id
                },
                "message": "Skill not found."
            }
        )
    
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "Find Skill ID internal error: " + str(e)
            }
        )

# Update Skill Name
def updateSkill(skill_id):

    try:
        # Check if the skill_id already exists in the skill table
        skill = Skill.query.filter_by(skill_id=skill_id).first()

        if skill:
            skill_name = request.json.get('skill_name', None)

            try:
                existing_skill = Skill.query.filter_by(skill_name=skill_name).first()

                if not(existing_skill):
                    
                    if skill_name != None:
                        if len(skill_name) == 0:
                            return jsonify(
                                {
                                    "code": 400,
                                    "data": {
                                        "skill_id": skill_id
                                    },
                                    "message": "Field required is empty. Unable to save edit."
                                }
                            ), 500

                        if len(skill_name) < 3:
                            return jsonify(
                                {
                                    "code": 400,
                                    "data": {
                                        "skill_id": skill_id
                                    },
                                    "message": "Minimum character length for Skill Name is 3."
                                }
                            ), 500

                        if len(skill_name) > 255:
                            return jsonify(
                                {
                                    "code": 400,
                                    "data": {
                                        "skill_id": skill_id
                                    },
                                    "message": "Skill name can only have a maximum of 256 characters."
                                }
                            ), 500
                        

                        skill.skill_name = skill_name

                        # Commit the changes
                        db.session.commit()

                    # If there is no exception, return doctor's information in JSON with HTTP status code 200 - Ok
                    return jsonify(
                        {
                            "code": 200,
                            "data": skill.json()
                        }
                    )
                else:
                    return jsonify(
                        {
                            "code": 400,
                            "data": {
                                "skill_id": skill_id
                            },
                            "message": "Skill name already exist. Unable to update skill."
                        }
                    ), 500

            except:
                
                return jsonify(
                    {
                        "code": 500,
                        "data": {
                            "skill_id": skill_id
                        },
                        "message": "An error occurred while updating the skill."
                    }
                )
        # Skill id doesnt exist
        return jsonify(
            {
                "code": 404,
                "data": {
                    "skill_id": skill_id
                },
                "message": "Skill id not found."
            }
        )

    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "skills-app.py internal error: " + str(e)
            }
        )

# Delete Skill
def deleteSkill(skill_id):
    try:
        skill = Skill.query.filter_by(skill_id=skill_id).first()
        if skill:
            try:
                if (skill.is_skill_deleted == False):
                    skill.is_skill_deleted = True

                db.session.commit()

                return jsonify(
                    {
                        "code": 200,
                        "data": skill.json()
                    }
                )
            except:
                return jsonify(
                    {
                        "code": 500,
                        "data": {
                            "skill_id": skill_id
                        },
                        "message": "An error occurred while updating the skill."
                    }
                )

        return jsonify(
            {
                "code": 404,
                "data": {
                    "skill_id": skill_id
                },
                "message": "Skill not found."
            }
        )

    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "ljps.py internal error: " + str(e)
            }
        )
        
def makeSkillAvailable(skill_id):
    try:
        skill = Skill.query.filter_by(skill_id=skill_id).first()
        if skill:
            try: 
                if skill.is_skill_deleted == True:
                    skill.is_skill_deleted = False
                    db.session.commit() 
                    return jsonify(
                        {
                            "code": 200,
                            "message": "Deleted skill has been made available"
                        }
                    )
                else:
                    return jsonify(
                        {
                            "code": 404,
                            "message": "Skill is already made available."
                        }
                    )
            except:
                return jsonify(
                    {
                        "code": 500,
                        "data": {
                            "skill_id": skill_id
                        },
                        "message": "An error occurred while making deleted skill available"
                    }
                )
        # Skill_id don't exist 
        return jsonify(
            {
                "code": 404,
                "data": {
                    "skill_id": skill_id
                },
                "message": "Skill not found"
            }
        )
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "Making Deleted skill available has an internal error: " + str(e)
            }
        )