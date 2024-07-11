from flask import Flask, request, jsonify, abort, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import getenv, environ
import platform
import json
app = Flask(__name__)
 

#localhost to use port 8889 if os is Mac, else use port 3306
if platform.system() == 'Darwin':
    DB_INFO = {'user' : 'root', 'password' : 'root', 'port':'8889'}
else:
    DB_INFO = {'user' : 'root', 'password' : '', 'port':'3306'}

# set db credentials to github workflow's if workflow is running
if getenv('GITHUB_WORKFLOW'):
    DB_INFO["password"] = environ["DBPASSWORD"]
    DB_INFO["user"] = environ["DBUSER"]
    DB_INFO["port"] = environ["DBPORT"]
 
# For window users, please uncomment this:
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{DB_INFO["user"]}:{DB_INFO["password"]}' + \
                                        f'@localhost:{DB_INFO["port"]}/lms_ljps'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100, 'pool_recycle': 280}

db = SQLAlchemy(app)

CORS(app)

import Role as Role
import Skill as Skill
import Course as Course
import SkillRole as SkillRole 
import SkillCourse as SkillCourse
import StaffSkill as StaffSkill
import LearningJourney as LearningJourney
import Registration as Registration
 

# View Role
@app.route("/roles", methods=["GET"])
def role():
    roles_info = Role.get_all_roles().json
    staff_id = session['staff_id']
    return render_template("hrRoles.html", roles_info=roles_info, staff_id=staff_id)

# Display Add Role page
@app.route("/displayAddRole")
def display_add_role():
    staff_id = session['staff_id']
    return render_template("hrAddRoles.html", staff_id=staff_id)

# Add Role
@app.route("/addRole", methods=["POST"])
def add_role():
    role_name = request.json.get('role_name', None)
    role = Role.add_a_role(role_name)
    return role

# Display Asssign Skill to Role Page
@app.route("/assign_skills_to_role/<int:role_id>")
def assign_skills_to_role(role_id):
    # staff_id = define_staff_id()
    staff_id = session['staff_id']
    try:
        role_info = Role.find_by_role_id(role_id).json

        #This part is for the displaying of assigned skills 
        #Getting the records with the specific role_id from the skill_role table in ljps database 
        assigned_info = SkillRole.get_assigned_skills_by_id(role_id).json
        
        # code to check if any skill is assigned to role
        code = assigned_info['code']
        
        if code == 200:
            #Creating a dict with value stored as list so that the skill info can be stored in the list
            skills_assigned = {"skills_assigned":[]}
            assigned_skill_id = []
            #Looping through the records retrieved from the skill_role table 
            for item in assigned_info["data"]["skill_role"]:
                #Get the info of a particular skill
                skill_info = Skill.find_by_skill_id(item["skill_id"]).json
                #Stored the info of this skill in the "skills_assigned" dict 
                skills_assigned["skills_assigned"].append(skill_info["data"])   
                assigned_skill_id.append(skill_info["data"]["skill_id"])
            
            #Get all the available skills 
            available_skills = Skill.get_all_skills().json
            skills_unassigned = {"skills_unassigned":[]}
            for element in available_skills["data"]["skills"]:
                if assigned_skill_id.count(element["skill_id"]) == 0:
                    skills_unassigned["skills_unassigned"].append(element)
                    
            return render_template("hrRolesSkills.html", skills_unassigned=skills_unassigned, skills_assigned=skills_assigned, assigned_info=assigned_info,role_info=role_info, staff_id=staff_id)

        else:
            #Get all the available skills 
            available_skills = Skill.get_all_skills().json
            skills_unassigned = {"skills_unassigned":[]}
            for element in available_skills["data"]["skills"]:
                skills_unassigned["skills_unassigned"].append(element)
                    
            return render_template("hrRolesSkills.html", skills_unassigned=skills_unassigned, assigned_info=assigned_info, role_info=role_info, staff_id=staff_id)
    
    except Exception as e:
        print(e)
        abort(500)
        
# Delete Assignment of a Skill to a Role 
@app.route("/delete_skill_role/<int:role_id>/<int:skill_id>", methods=["DELETE"])
def delete_skill_role(role_id, skill_id):
    return SkillRole.delete_skill_role(role_id, skill_id)

# Assign a Skill to a Role 
@app.route("/add_skill_role/<int:role_id>/<int:skill_id>", methods=["POST"])
def add_skill_role(role_id, skill_id):
    skill_role = SkillRole.create_new_record(role_id, skill_id)
    return skill_role

# Display Edit a Skill Page
@app.route("/edit_role/<int:role_id>")
def edit_role(role_id):
    #roles_info = get_all_roles().json
    # staff_id = define_staff_id()
    staff_id = session['staff_id']
    roles_info = Role.find_by_role_id(role_id)
    #return render_template("hrEditRoles.html", roles_info=roles_info)
    #print(roles_info.json)
    return render_template("hrEditRoles.html", roles_info=roles_info.json["data"], staff_id=staff_id)

# Edit a Role  
@app.route("/update_role/<int:role_id>", methods=['PUT'])
def update_role(role_id):
    return Role.updateRole(role_id)

# Delete a Role 
@app.route("/delete_role/<int:role_id>", methods=['PUT'])
def delete_role(role_id):
    return Role.deleteRole(role_id)

# Make Deleted Role Available
@app.route("/makeRoleAvailable/<int:role_id>", methods=['PUT'])
def makeRoleAvailable(role_id):
    return Role.makeRoleAvailable(role_id)

# View Skills
@app.route("/skills", methods=['GET'])
def retrieve_skills():
    try:
        # Retrieve data based on skill_id
        # skill = get_all_skills().json["data"]["skills"]
        skill_info = Skill.get_all_skills().json
        # staff_id = define_staff_id()
        staff_id = session['staff_id']
        return render_template("hrSkills.html", skill_info=skill_info, staff_id=staff_id)

    except Exception as e:
        print(e)
        abort(500)

# Display Add Skills Page
@app.route("/create_skill")
def create_skill():
    # staff_id = define_staff_id()
    staff_id = session['staff_id']
    
    return render_template("hrAddSkills.html", staff_id=staff_id)  

# Add Skill
@app.route("/add_skill", methods=["POST"])
def add_skill():
    skill_name = request.json.get('skill_name', None)
    skill = Skill.add_a_skill(skill_name)
    # print(skill)
    return skill 

# Edit Skill Page
@app.route("/edit_skill/<int:skill_id>")
def edit_skill(skill_id):
    skills_info = Skill.find_by_skill_id(skill_id)
    # staff_id = define_staff_id()
    staff_id = session['staff_id']
    return render_template("hrEditSkill.html", skill=skills_info.json["data"], staff_id=staff_id)

# Update Skill
@app.route("/update_skill/<int:skill_id>", methods=['PUT'])
def update_skill(skill_id):
    return Skill.updateSkill(skill_id)

# Delete skill
@app.route("/delete_skill/<int:skill_id>", methods=['PUT'])
def deleteSkill(skill_id):
    return Skill.deleteSkill(skill_id)

# Make Deleted Skill Available
@app.route("/make_skill_available/<int:skill_id>", methods=['PUT'])
def make_skill_available(skill_id):
    return Skill.makeSkillAvailable(skill_id)

# View Course Page
@app.route("/course", methods=["GET"])
def course():
    try:
        # staff_id = define_staff_id()
        staff_id = session['staff_id']
        course_info = Course.get_active_courses().json
        # print(course_info)
        
        return render_template("hrCourses.html", course_info=course_info, staff_id=staff_id)
    #To be confirm 
    except Exception as e:
        print(e)
        abort(500)

# Display Assign Skills to Course Page
@app.route("/assign_skills_to_course/<string:course_id>")
def assign_skills_to_course(course_id):
    course_info = Course.find_by_course_id(course_id).json

    #This part is for the displaying of assigned skills 

    #Getting the records with the specific role_id from the skill_course table in ljps database 
    assigned_info = SkillCourse.get_assigned_skills_by_id(course_id).json
    
    # print(assigned_info)
    
    # code to check if any skill is assigned to course - 200, 404, 500
    code = assigned_info['code']
    # staff_id = define_staff_id()
    staff_id = session['staff_id']

    if code == 200: 
        #Creating a dict with value stored as list so that the skill info can be stored in the list
        skills_assigned = {"skills_assigned":[]}
        assigned_skill_id = []
        #Looping through the records retrieved from the skill_course table 
        for item in assigned_info["data"]["skill_course"]:
            #Get the info of a particular skill
            skill_info = Skill.find_by_skill_id(item["skill_id"]).json
            #Stored the info of this skill in the "skills_assigned" dict
            #print(skill_info)
            is_skill_deleted = skill_info["data"]["is_skill_deleted"]
            if is_skill_deleted == False:
                skills_assigned["skills_assigned"].append(skill_info["data"])   
                assigned_skill_id.append(skill_info["data"]["skill_id"])
        
        #Get all the available skills 
        available_skills = Skill.get_all_skills().json
        #print(available_skills)
        skills_unassigned = {"skills_unassigned":[]}
        for element in available_skills["data"]["skills"]:
            if element["is_skill_deleted"] == False:
                if assigned_skill_id.count(element["skill_id"]) == 0:
                    skills_unassigned["skills_unassigned"].append(element)
                #print(skills_unassigned)
        #print(assigned_info)
        #print(skills_assigned)
        return render_template("hrCoursesSkills.html", staff_id=staff_id, skills_unassigned=skills_unassigned, skills_assigned=skills_assigned, assigned_info=assigned_info, course_info=course_info)
    
    else: # checking to see if there are skills assigned to a course
        skills_assigned = {"skills_assigned":[]}
        assigned_info = SkillCourse.get_assigned_skills_by_id(course_id).json
        
        # print(assigned_info)
        # print('we came here')
        
        assigned_skill_id = []
        
        #Get all the available skills 
        available_skills = Skill.get_all_skills().json
        skills_unassigned = {"skills_unassigned":[]}
        for element in available_skills["data"]["skills"]:
            if assigned_skill_id.count(element["skill_id"]) == 0:
                skills_unassigned["skills_unassigned"].append(element)
                #print(skills_unassigned)

        return render_template("hrCoursesSkills.html", staff_id=staff_id, skills_unassigned=skills_unassigned, skills_assigned=skills_assigned, assigned_info=assigned_info, course_info = course_info)
        
# Assign a Skill to a Course        
@app.route("/add_skill_course/<int:skill_id>/<string:course_id>", methods=["POST"])
def add_skill_course(skill_id, course_id):
    skill_course = SkillCourse.create_new_sc(skill_id, course_id)
    print(skill_course)
    return skill_course

#Delete Assignmnet of a Skill to a Course
@app.route("/remove_skill_course/<int:skill_id>/<string:course_id>", methods=["DELETE"])
def remove_skill_course(skill_id, course_id):
    removed_sc = SkillCourse.remove_assigned_sc(skill_id, course_id)
    return removed_sc

# Learning Journey [Skills] - Display skills of a chosen role
@app.route('/selectSkill/<int:role_id>')
def selectSkill(role_id):
    try:
        skills = SkillRole.get_assigned_skills_by_id(role_id).json
        role = Role.find_by_role_id(role_id).json
        role_name = role['data']['role_name']
        error = {}
        staff_id = session['staff_id']
        skill_detail_list = []
        if (skills['code'] == 200):
            skill_role=skills['data']['skill_role']
            for skill in skill_role:
                skill_details = Skill.find_by_skill_id(skill["skill_id"]).json

                # only get skills that are not deleted
                if(skill_details['data']['is_skill_deleted'] == False):
                    acquired = StaffSkill.isSkillAcquiredByStaff(staff_id, skill["skill_id"])
                    if type(acquired) == bool:
                        skill_details['data']['acquired'] = acquired
                        skill_detail_list.append(skill_details['data'])
                    else:
                        error = acquired    
                
            # print(skill_detail_list)        

        else:
            error = skills
        if len(skill_detail_list) == 0:
            error['message'] = "No skills have been assigned to the role - "+ role_name
    except Exception as e:
            error['message'] = e
    return render_template('LJ_Skills.html', staff_id=staff_id, error=error, skills=skill_detail_list, role_id=role_id, role_name=role_name)


# Learning Journey [Courses] - Display course details of a chosen skill
@app.route("/selectCourse/<int:role_id>/<int:skill_id>", methods=['GET'])
def retrieve_courses_of_skill(role_id, skill_id):
    try:
        error = {}
        # staff_id = define_staff_id()
        staff_id = session['staff_id']
        # print(role_id)

        course_of_skill = SkillCourse.get_courses_for_a_skill(skill_id).json
        # print(course_of_skill) 
        
        if course_of_skill['code'] == 200:
            skill_info = Skill.find_by_skill_id(skill_id).json
            skill_name = skill_info['data']['skill_name']

            course_skill_list = course_of_skill['data']['skill_course']
            # print(course_skill_list)

            if course_of_skill['code'] == 200:
                courseID_list = []
                for each_course in course_skill_list:
                    courseID_list.append(each_course['course_id'])
                # print(courseID_list)
        
                course_details_of_skill_list = []
                for each_courseID in courseID_list:
                    course_detail = Course.find_by_course_id(each_courseID).json  
                    # print(course_detail)
                    
                    reg_details = Registration.get_completion_reg_status(staff_id, each_courseID).json
                    # print(reg_details)
                    
                    # if code = 200 --> user has completed/currently taking this course under this skill
                    if reg_details['code'] == 200:
                        detail = reg_details['data']['reg_detail']
                        comp_status = detail[0]['completion_status']
                        # print(status)
                        reg_status = detail[0]['reg_status']

                        course_detail['data']['completion_status'] = comp_status
                        course_detail['data']['reg_status'] = reg_status
                        
                    # if code = 201 --> user HAS NOT started taking this course under this skill
                    elif reg_details['code'] == 201:
                        status = reg_details['completion_status']
                        course_detail['data']['completion_status'] = status
                
                    # print(course_detail)
                    course_info = course_detail['data']
                    # print(course_info)
                    course_details_of_skill_list.append(course_info)
                    
                # print(course_details_of_skill_list)
            
                
            return render_template('LJ_Courses.html', staff_id=staff_id, course_of_skill=course_of_skill, course_details_of_skill_list=course_details_of_skill_list, role_id=role_id, skill_id=skill_id, course_detail=course_detail, skill_name=skill_name, error=error)

        else:
            error['message'] = course_of_skill['message']
            # print(len(error))
            
            # print(error)
            
            return render_template('LJ_Courses.html', staff_id=staff_id, error=error)
            
    except Exception as e:
        print(e)
        abort(500)

# Save Learning Journey
@app.route("/save_learning_journey", methods=["POST"])
def save_learning_journey():
    staff_id = session['staff_id']
    return LearningJourney.save_learning_journey(staff_id)

# Delete Learning Journey Course
@app.route("/delete_learning_journey_course/<int:lj_id>/<int:ljc_id>", methods=["DELETE"])
def delete_learning_journey_course(lj_id, ljc_id):
    return LearningJourney.delete_ljc_by_id(lj_id, ljc_id)

@app.route("/selectRole")
def selectRole():
    staff_id = session['staff_id']
    roles_available = {"roles_available": []}
    all_roles = Role.get_all_roles().json
    for role in all_roles["data"]["roles"]:
        # print(role)
        if role["is_role_deleted"] == 0:
            roles_available["roles_available"].append(role)   
    return render_template("LJ_Roles.html", staff_id=staff_id, roles_available=roles_available, all_roles=all_roles)

# View Saved Learning Journey Course
@app.route("/selectSavedLearningJourney/<int:lj_id>", methods=['GET'])
def selectSavedLearningJourney(lj_id):
    try:
        staff_id = session['staff_id']

        staff_lj = LearningJourney.get_lj_by_id(staff_id).json
        staff_all_lj = staff_lj['data']['learning_journey']

        staff_lj_id = []
        for each_lj in staff_all_lj:
            staff_lj_id.append(each_lj['lj_id'])
        # print(staff_lj_id)

        lj_id = lj_id
        # print(lj_id)
        error = {}
        learningjourney = LearningJourney.find_by_lj_id(lj_id).json
        if learningjourney['code']==200:
        # print(learningjourney)
            skill_id = learningjourney['data']['skill_id']
            skill_name = Skill.find_by_skill_id(skill_id).json
            skill_name = skill_name['data']['skill_name']
            # print(skill_name)
            role_id = learningjourney['data']['role_id']
            role_name = Role.find_by_role_id(role_id).json
            role_name = role_name['data']['role_name']
            
            position = staff_lj_id.index(lj_id)
            position = position + 1
            # print(position)
            

            learningjourneycourses = LearningJourney.get_courses_under_learningjourney(lj_id).json
            # print(learningjourneycourses)

            if learningjourneycourses['code']==200:
                saved_course_list = learningjourneycourses['data']['learning_journey_course']
                # print(saved_course_list)

                courseID_list = []
                for each_saved_course in saved_course_list:
                    courseID_list.append(each_saved_course['course_id'])
                    # print(courseID_list)
                
                course_details_of_saved_learning_journey = []
                for each_courseID in courseID_list:
                    saved_course_detail = Course.find_by_course_id(each_courseID).json
                    # print(saved_course_detail)
                    saved_course_info = saved_course_detail['data']
                    # print(saved_course_info)
                    course_details_of_saved_learning_journey.append(saved_course_info)
                
                # print(course_details_of_saved_learning_journey)
                
                course_data = zip(saved_course_list,course_details_of_saved_learning_journey)
                course_data = list(course_data)
                # print(course_data)
                return render_template('LJ_SavedCourses.html', staff_id=staff_id, role_name=role_name, skill_name=skill_name, course_data=course_data, learningjourneycourses=learningjourneycourses,error=error, lj_id=lj_id, position=position)
            else:
                error['message'] = learningjourneycourses['message']
                return render_template('LJ_SavedCourses.html',error=error)
        else:
            error['message'] = learningjourney['message']
            return render_template('LJ_SavedCourses.html',error=error)
    except Exception as e:
        print(e)
        abort(500)
    

# View all Saved Learning Journey
@app.route("/my_learning_journey/<int:staff_id>", methods=["GET"])
def my_learning_journey(staff_id):
    
    try:
        staff_id = session['staff_id']
        error = {}
        learningjourney = LearningJourney.get_lj_by_id(staff_id).json
        # print(learningjourney)
    
        if learningjourney['code'] == 200:
        
            new_learningjourney = learningjourney['data']['learning_journey']
            # print(new_learningjourney)
            
            counter = 1
            for each_lj in new_learningjourney:
                roleID = each_lj['role_id']
                role = Role.find_by_role_id(roleID).json
                each_lj['role_name'] = role['data']['role_name']
                # print(role)
                
                skillID = each_lj['skill_id']
                skill = Skill.find_by_skill_id(skillID).json
                each_lj['skill_name'] = skill['data']['skill_name']
                # print(skill)
                
                ljID = each_lj['lj_id']
                course = LearningJourney.get_courses_under_learningjourney(ljID).json
                # print(course)
                ljcourse_info = course['data']['learning_journey_course']
                
                length = len(ljcourse_info)
                if length == 1:
                    # print(ljcourse_info)
                    course_name_list = []
                    ljcourse_id = ljcourse_info[0]['course_id']
                    ljcourse_status = ljcourse_info[0]['completion_status']
                    course_info = Course.find_by_course_id(ljcourse_id).json
                    course_name_list.append(course_info['data']['course_name'])
                    each_lj['course_count'] = len(course_name_list)
                    each_lj['completion_status'] = ljcourse_status
                    # print(ljcourse_id)
                
                else:
                    # print(ljcourse_info)
                    course_name_list = []
                    for each_ljcourse in ljcourse_info:
                        # print(each_ljcourse)
                        ljcourse_id = each_ljcourse['course_id']
                        course_info = Course.find_by_course_id(ljcourse_id).json
                        each_lj['completion_status'] = each_ljcourse['completion_status']
                        
                        course_name_list.append(course_info['data']['course_name'])
                    # print(course_name_list)
                    each_lj['course_count'] = len(course_name_list)
            
                each_lj['counter'] = counter
                counter += 1
            
            # print(new_learningjourney)

            return render_template('LJ_myLJ.html', learningjourney=learningjourney,new_learningjourney=new_learningjourney, error=error, staff_id=staff_id)
        
        else:
            error['message'] = learningjourney['message']
            # print(error)
            
            return render_template('LJ_myLJ.html',error=error, staff_id=staff_id)
    
    except Exception as e:
        print(e)
        abort(500)

# Get Courses for Users to Add in Learning Journey        
@app.route("/getCoursesFromLj/<int:lj_id>", methods=["GET"])
def getCoursesFromLj(lj_id):
    try:
        staff_id = session['staff_id']

        staff_lj = LearningJourney.get_lj_by_id(staff_id).json
        staff_all_lj = staff_lj['data']['learning_journey']
        staff_lj_id = []
        for each_lj in staff_all_lj:
            staff_lj_id.append(each_lj['lj_id'])
        position = staff_lj_id.index(lj_id)
        position = position + 1

        lj_details = LearningJourney.get_learning_journey_details(lj_id).json
        lj_skill = lj_details['data']['skill_id']
        courses = SkillCourse.get_courses_for_a_skill(lj_skill).json
        lj_courses = LearningJourney.get_courses_under_learningjourney(lj_id).json
        error = []
        if (lj_details['code'] != 200):
            error.append(lj_details['message'])
        if courses['code'] != 200:
            error.append(courses['message'])
        if lj_courses['code'] != 200:
            error.append(lj_courses['message'])
    
        display_course_list = []
        #only get courses that are active
        for course in courses['data']['skill_course']:
            course_details = Course.find_by_course_id(course['course_id']).json
            if course_details['code'] != 200:
                error.append(course_details['message'])
            if course_details['data']['course_status'] == 'Active':
                course_details_list = course_details['data']
                isCourseInLj = LearningJourney.isCourseInLJ(lj_id, course_details_list['course_id'])
                if type(isCourseInLj) == bool:
                    course_details_list['inLj'] = isCourseInLj
                    if isCourseInLj == False:
                        reg_details = Registration.get_completion_reg_status(staff_id, course_details['data']['course_id']).json
                        if reg_details['code'] == 500:
                            error.append(reg_details['message'])
                        else: 
                            if reg_details['code'] == 201:
                                course_details_list['completion_status'] = reg_details['completion_status']
                                course_details_list['reg_status'] = reg_details['reg_status']
                            else:
                                course_details_list['completion_status'] = reg_details['data']['reg_detail'][0]['completion_status']
                                course_details_list['reg_status'] = reg_details['data']['reg_detail'][0]['reg_status']
                            if len(course_details_list['completion_status']) == 0:
                                course_details_list['completion_status'] = "Not Started"
                    display_course_list.append(course_details_list)
                else:
                    error.append(isCourseInLj['message'])
        return render_template('LJ_AddCourse.html', lj_id=lj_id, staff_id=staff_id, error=error, display_course_list=display_course_list, position=position)
    except Exception as e:
        print(e)
        abort(500)

#Get Courses for Users to Add in Learning Journey
@app.route("/add_course_to_lj", methods=["POST"])
def add_course_to_lj():
    try:
        staff_id = session['staff_id']
        lj_id = request.json.get('lj_id', None)
        selected_course_id = request.json.get('selected_course_id', None)
        selected_course = selected_course_id.split(",")
        selected_reg = []
        selected_completion = []
        for course_id in selected_course:
            completion_status = "Not Started"
            reg_status = "Not Registered"
            reg_details = Registration.get_completion_reg_status(staff_id, course_id).json
            if reg_details['code'] == 500:
                return reg_details
            else: 
                if reg_details['code'] == 201:
                    completion_status = reg_details['completion_status']
                    reg_status = reg_details['reg_status']
                else:
                    completion_status = reg_details['data']['reg_detail'][0]['completion_status']
                    reg_status = reg_details['data']['reg_detail'][0]['reg_status']
                if(len(completion_status) == 0 ):
                    completion_status = "Not Started"
            selected_reg.append(reg_status)
            selected_completion.append(completion_status)
        print(selected_reg)
        print(selected_completion)
        return LearningJourney.add_course_to_lj(lj_id, selected_course_id, selected_completion, selected_reg)
    except Exception as e:
        print(e)
        abort(500)

# Delete Completed Learning Journeys 
@app.route("/delete_lj/<int:lj_id>", methods=["DELETE"])
def delete_lj(lj_id):
    # print(lj_id)
    return LearningJourney.delete_lj(lj_id)

#Login Page
@app.route("/")
def index():
    return render_template('login.html')

# Login Redirect
@app.route("/login/<string:role>", methods=['GET'])
def login(role):
    #change staff id here to test
    if role == "admin":
        session['staff_id'] = 150126
        return redirect(url_for('role'))
    else:
        session['staff_id'] = 130001
        return redirect(url_for('retrieve_skills'))
   
if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='0.0.0.0',port=5000, debug=True)