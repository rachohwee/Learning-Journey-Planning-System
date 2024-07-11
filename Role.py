from flask import Flask, jsonify, request
from app import db

class Role(db.Model):
    __tablename__ = 'job_role'

    role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(256), nullable=False)
    is_role_deleted = db.Column(db.Boolean, nullable=False)

    def __init__(self, role_id, role_name, is_role_deleted):
        self.role_id = role_id
        self.role_name = role_name
        self.is_role_deleted = is_role_deleted

    def json(self):
        dto = {
            'role_id': self.role_id,
            'role_name': self.role_name,
            'is_role_deleted': self.is_role_deleted
        }
        return dto


def get_all_roles():
    try:
        rolelist = Role.query.all()

        # print(rolelist)

        if len(rolelist):
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "roles": [role.json() for role in rolelist]
                    }
                }
            )
        return jsonify(
            {
                # Return an error message in JSON and HTTP status code 404 - Not Found
                "code": 404,
                "message": "There are no roles created yet."
            }
        )

    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "View Role internal error: " + str(e)
            }
        )


def add_a_role(role_name):
    try:
        role_name = role_name.capitalize()
        if len(role_name) == 0:
            return jsonify(
                {
                    "code": 400,
                    "data": {
                        "role_name": role_name
                    },
                    "message": "Field required is empty. Unable to create role."
                }
            )
        if len(role_name) < 3:
             return jsonify(
                {
                    "code": 400,
                    "data": {
                        "role_name": role_name
                    },
                    "message": "Minimum character length for role name is 3. Unable to create role."
                }
            )
        if len(role_name) > 256:
            return jsonify(
                {
                    "code": 400,
                    "data": {
                        "role_name": role_name
                    },
                    "message": "Role name can only have a maximum of 256 characters. Unable to create role."
                }
            )
        role = Role.query.filter_by(role_name=role_name).first()
        if role:
            return jsonify(
                {
                    "code": 400,
                    "data": {
                        "role_name": role_name
                    },
                    "message": "Role already exists. Unable to create role."
                }
            )
        else:
            try:
                role = Role(None, role_name=role_name, is_role_deleted=False)
                db.session.add(role)
                db.session.commit()
            except:
                return jsonify(
                    {
                        "code": 500,
                        "data": {
                            "role_name": role_name
                        },
                        "message": "An error occurred while creating the role."
                    }
                )
            return jsonify(
                {
                    "code": 201,
                    "data": {
                        "role_name": role.json()
                    },
                    "message": "Role has been successfully created."
                }
            )
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "Add Role internal error: " + str(e)
            }
        )


def find_by_role_id(role_id):
    try:
        # Check if the role_id already exists in the role table
        role = Role.query.filter_by(role_id=role_id).first()

        if role:
            # The role_id exist
            return jsonify(
                {
                    # Return role's information in JSON with HTTP status code 200 - Ok
                    "code": 200,
                    "data": role.json()
                }
            )

        # The role_id does not exist
        return jsonify(
            {
                # Return role_id and error message in JSON with HTTP status code 404 - Not Found
                "code": 404,
                "data": {
                    "role_id": role_id
                },
                "message": "Role not found."
            }
        )

    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "Find Role ID internal error: " + str(e)
            }
        )


def updateRole(role_id):
    try:
        # Check if the role_id already exists in the role table
        role = Role.query.filter_by(role_id=role_id).first()

        if role:
            # Get all the data from the request recieved and store into the respective variables
            role_name = request.json.get('role_name', None)

            try:
                existing_role = Role.query.filter_by(
                    role_name=role_name).first()

                if not (existing_role):

                    # Check if the variable is not equal to "None" before updating the value of the respective attribute in the database

                    if role_name != None:
                        if len(role_name) == 0:
                            return jsonify(
                                {
                                    "code": 400,
                                    "data": {
                                        "role_id": role_id
                                    },
                                    "message": "Field required is empty. Unable to update role."
                                }
                            ), 400

                        if len(role_name) < 3:
                            return jsonify(
                                {
                                    "code": 400,
                                    "data": {
                                        "role_id": role_id
                                    },
                                    "message": "Minimum character length for role name is 3. Unable to update role."
                                }
                            ), 400
                        
                        if len(role_name) > 255:
                            return jsonify(
                                {
                                    "code": 400,
                                    "data": {
                                        "role_id": role_id 
                                    },
                                    "message": "Role name can only have a maximum of 256 characters. Unable to update role."
                                }
                            ), 400


                        role.role_name = role_name

                        # Commit the changes 
                        db.session.commit()

                    # If there is no exception, return role's information in JSON with HTTP status code 200 - Ok
                    return jsonify(
                        {
                            "code": 200,
                            "data": role.json()
                        }
                    ), 200
                else:
                    return jsonify(
                        {
                            "code": 400,
                            "data": {
                                "role_id": role_id
                            },
                            "message": "Role name already exists. Unable to update role."
                        }
                    ), 400

            except:
                # Return role_id and an error message in JSON with HTTP status code 500 - Internal Server error if an exception occurs.
                return jsonify(
                    {
                        "code": 500,
                        "data": {
                            "role_id": role_id
                        },
                        "message": "An error occurred while updating the name of the role."
                    }
                ), 500

        # The role_id does not exist 
        return jsonify(
            {
                # Return role_id and error message in JSON with HTTP status code 404 - Not Found 
                "code": 404,
                "data": {
                    "role_id": role_id
                },
                "message": "Role id not found."
            }
        ), 404
    
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "Update Role Name internal error: " + str(e)
            }
        ), 500

def deleteRole(role_id):
    try:
        # Check if the role_id already exists in the role table 
        role = Role.query.filter_by(role_id=role_id).first()
    
        if role:
            try:   

                if (role.is_role_deleted == False):
                    role.is_role_deleted = True

                    db.session.commit()
                    
                    # If there is no exception, return role's information in JSON with HTTP status code 200 - Ok
                    return jsonify(
                        {
                            "code": 200,
                            "message": "Role have been deleted successfully."
                        }
                    ), 200

            except:
                # Return role_id and an error message in JSON with HTTP status code 500 - Internal Server error if an exception occurs.
                return jsonify(
                    {
                        "code": 500,
                        "data": {
                            "role_id": role_id
                        },
                        "message": "An error occurred while deleting the role."
                    }
                ), 500

        # The role_id does not exist 
        return jsonify(
            {
                # Return role_id and error message in JSON with HTTP status code 404 - Not Found 
                "code": 404,
                "data": {
                    "role_id": role_id
                },
                "message": "Role id not found."
            }
        ), 404
    
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "Delete Role internal error: " + str(e)
            }
        ), 500


def makeRoleAvailable(role_id):
    try:
        role = Role.query.filter_by(role_id=role_id).first()
        if role:
            try: 
                if role.is_role_deleted == True:
                    role.is_role_deleted = False
                    db.session.commit() 
                    return jsonify(
                        {
                            "code": 200,
                            "message": "Deleted Role has been made Available."
                        }
                    )
                else:
                    return jsonify(
                        {
                            "code": 404,
                            "message": "Role is already made available."
                        }
                    )
            except:
                # Return role_id and an error message in JSON with HTTP status code 500 - Internal Server error if an exception occurs.
                return jsonify(
                    {
                        "code": 500,
                        "data": {
                            "role_id": role_id
                        },
                        "message": "An error occurred while making deleted role available."
                    }
                )
        # The role_id does not exist 
        return jsonify(
            {
                # Return role_id and error message in JSON with HTTP status code 404 - Not Found 
                "code": 404,
                "data": {
                    "role_id": role_id
                },
                "message": "Role not found."
            }
        )
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "Delete Role internal error: " + str(e)
            }
        )