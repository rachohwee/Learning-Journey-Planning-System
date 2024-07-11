from flask import jsonify
from app import db

class SkillRole (db.Model):
    __tablename__ = 'skill_role'

    sr_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_id = db.Column(db.Integer, nullable=False)
    skill_id = db.Column(db.Integer, nullable=False)

    def __init__(self, sr_id, role_id, skill_id):
        self.sr_id = sr_id
        self.role_id = role_id
        self.skill_id = skill_id

    def json(self):
        dto = {
            'sr_id': self.sr_id,
            'role_id': self.role_id,
            'skill_id': self.skill_id
        }
        return dto


def get_assigned_skills_by_id(role_id):
    try:
        # Get all the records with a specific role_id from the skill_role table
        skillrolelist = SkillRole.query.filter_by(role_id=role_id).all()

        if len(skillrolelist):
            # There is at least one record with the specific role_id from the skill_role table
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "skill_role": [skillrole.json() for skillrole in skillrolelist]
                    }
                }
            )
        # There is no record with the specific role_id from the skill_role table
        return jsonify(
            {
                # Return an error message in JSON and HTTP status code 404 - Not Found
                "code": 404,
                "message": "No skill is assigned to this role."
            }
        )

    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "Get Assigned Skills by Role ID internal error: " + str(e)
            }
        )


def get_sr_id(role_id, skill_id):
    try:
        # Get the record with a specific role_id and skill_id from the skill_role table
        skillrole = SkillRole.query.filter_by(
            role_id=role_id, skill_id=skill_id).first()

        if skillrole:
            # There is a record with the specific role_id and skill_id from the skill_role table
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "skill_role": skillrole.json()
                    }
                }
            )

        # No record with the specific role_id and skill_id from the skill_role table
        return jsonify(
            {
                # Return an error message in JSON and HTTP status code 404 - Not Found
                "code": 404,
                "message": "There is no assignment between this skill and role"
            }
        )

    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "Get Assignment ID internal error: " + str(e)
            }
        )


def create_new_record(role_id, skill_id):
    try:
        skill_role_info = get_sr_id(role_id, skill_id).json

        #print(skill_role_info)

        if skill_role_info["code"] == 200:
            # There is an assignment between the role and skill
            # Return sr_id and an error message in JSON with HTTP status code 400 - Bad Request
            return jsonify(
                {
                    "code": 400,
                    "data": {
                        "sr_id": skill_role_info["data"]["skill_role"]["sr_id"]
                    },
                    "message": "The skill is assigned to the role already."
                }
            ), 400

        if skill_role_info["code"] == 404:

            all_assigned_skills = get_assigned_skills_by_id(role_id).json

            #print(all_assigned_skills)

            if all_assigned_skills["code"] == 200 or all_assigned_skills["code"] == 404:
                if all_assigned_skills["code"] == 200 and len(all_assigned_skills["data"]["skill_role"]) == 5:
                    return jsonify(
                        {
                            "code": 400,
                            "data": {
                                "role_id": role_id,
                                "skill_id": skill_id
                            },
                            "message": "Unable to assign the selected skill to role as each role can only have a maximum of 5 skills "
                        }
                    ), 400

                skillrole = SkillRole(
                    sr_id=None, role_id=role_id, skill_id=skill_id)

                try:
                    # Add  to the skill_role table
                    db.session.add(skillrole)
                    # Commit the changes
                    db.session.commit()
                except:
                    # Return role_id & skill_id and an error message in JSON with HTTP status code 500 - Internal Server error if an exception occurs.
                    return jsonify(
                        {
                            "code": 500,
                            "data": {
                                "role_id": role_id,
                                "skill_id": skill_id
                            },
                            "message": "An error occurred while creating the assignment of the skill to the role."
                        }
                    ), 500

                # If there is no exception, return the JSON representation of the doctor added with HTTP status code 201 - created.
                return jsonify(
                    {
                        "code": 201,
                        "data": skillrole.json()
                    }
                ), 201

        if skill_role_info["code"] == 500:
            return skill_role_info

       
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "Assign Skill to a Role internal error: " + str(e)
            }
        ), 500


def delete_skill_role(role_id, skill_id):
    try:
        skill_role_info = get_sr_id(role_id, skill_id).json

        if skill_role_info["code"] == 200:

            sr_id = skill_role_info["data"]["skill_role"]["sr_id"]
       
            # Check if the role_id already exists in the role table
            skillrole = SkillRole.query.filter_by(sr_id=sr_id).first()

            if skillrole:
                try:

                    db.session.delete(skillrole)
                    db.session.commit()

                    # If there is no exception, return role's information in JSON with HTTP status code 200 - Ok
                    return jsonify(
                        {
                            "code": 200,
                            "message": "Role have been deleted successfully"
                        }
                    ), 200

                except:
                    # Return role_id and an error message in JSON with HTTP status code 500 - Internal Server error if an exception occurs.
                    return jsonify(
                        {
                            "code": 500,
                            "data": {
                                "role_id": sr_id
                            },
                            "message": "An error occurred while deleting the role"
                        }
                    ), 500

            # The role_id does not exist
            return jsonify(
                {
                    # Return role_id and error message in JSON with HTTP status code 404 - Not Found
                    "code": 404,
                    "data": {
                        "role_id": sr_id
                    },
                    "message": "Role id not found"
                }
            ), 404

        if skill_role_info["code"] == 404 or skill_role_info["code"] == 500:
             return skill_role_info

    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "Delete Assignment of a Skill to a Role internal error: " + str(e)
            }
        ), 500
