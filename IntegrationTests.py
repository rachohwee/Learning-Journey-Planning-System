import unittest
import unittest.mock
import flask_testing
import json
from Role import Role
from Course import Course
from Skill import Skill
from StaffSkill import StaffSkill
from SkillRole import SkillRole
from SkillCourse import SkillCourse
from LearningJourney import LearningJourney
from LearningJourney import LearningJourneyCourse
from app import app, db

class TestApp(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://" 
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True

    def create_app(self):
        return app

    def setUp(self):
        app.config['SECRET_KEY'] = 'sekrit!'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

# Sprint 1 - SkillCourse Testing
class TestSkillsCourse(TestApp):
    def testAssignSkillsToCourse(self):
        with unittest.mock.patch("app.session", dict()) as session:
            client = app.test_client()
            client.get("/login/admin")
            c1 = Course(course_id="COR001", course_name="Systems Thinking and Design", course_desc="This foundation module aims to introduce students to the fundamental concepts and underlying principles of systems thinking,", course_status="Active", course_type="Internal", course_category="Core")
            sk1 = Skill(skill_id=1, skill_name="Leadership", is_skill_deleted=False)
            sk2 = Skill(skill_id=2, skill_name="Analytics", is_skill_deleted=False)
            staff_id = session.get('staff_id')
            sc1 = SkillCourse(sc_id=1, skill_id=1, course_id="COR001")
            db.session.add(c1)
            db.session.add(sk1)
            db.session.add(sk2)
            db.session.add(sc1)
            db.session.commit()
            self.client.get("/assign_skills_to_course/" + str(c1.course_id), content_type='application/json')
            self.assert_template_used('hrCoursesSkills.html')
            self.assert_context('staff_id', staff_id)
            self.assert_context('skills_unassigned', 
            {'skills_unassigned': [{'is_skill_deleted': False, 'skill_id': 2, 'skill_name': 'Analytics'}]}
            )
            self.assert_context('skills_assigned',
            {'skills_assigned': [{'is_skill_deleted': False, 'skill_id': 1, 'skill_name': 'Leadership'}]}
            )
            self.assert_context('assigned_info', 
            {'code': 200, 'data': {'skill_course': [{'course_id': 'COR001', 'sc_id': 1, 'skill_id': 1}]}}
            )
            self.assert_context('course_info', 
            {'code': 200, 'data': {'course_category': 'Core', 'course_desc': 'This foundation module aims to introduce students to the fundamental concepts and underlying principles of systems thinking,', 'course_id': 'COR001', 'course_name': 'Systems Thinking and Design', 'course_status': 'Active', 'course_type': 'Internal'}}
            )
    
    def testAddSkillCourse(self):
        with unittest.mock.patch("app.session", dict()) as session:
            client = app.test_client()
            client.get("/login/admin")
            c1 = Course(course_id="COR001", course_name="Systems Thinking and Design", course_desc="This foundation module aims to introduce students to the fundamental concepts and underlying principles of systems thinking,", course_status="Active", course_type="Internal", course_category="Core")
            sk1 = Skill(skill_id=1, skill_name="Leadership", is_skill_deleted=False)
            sk2 = Skill(skill_id=2, skill_name="Analytics", is_skill_deleted=False)
            sc1 = SkillCourse(sc_id=1, skill_id=1, course_id="COR001")
            db.session.add(c1)
            db.session.add(sk1)
            db.session.add(sk2)
            db.session.add(sc1)
            db.session.commit()
            req = self.client.post("/add_skill_course/" + str(sk2.skill_id) + "/"+ str(c1.course_id), content_type='application/json')
            req = req.json
            self.assertEqual(req['code'], 201)
            self.assertEqual(req['data'], 
            {'course_id': c1.course_id, 
            'sc_id': 2, 
            'skill_id': sk2.skill_id})

    def testRemoveAssignedSC(self):
        with unittest.mock.patch("app.session", dict()) as session:
            client = app.test_client()
            client.get("/login/admin")
            c1 = Course(course_id="COR001", course_name="Systems Thinking and Design", course_desc="This foundation module aims to introduce students to the fundamental concepts and underlying principles of systems thinking,", course_status="Active", course_type="Internal", course_category="Core")
            sk1 = Skill(skill_id=1, skill_name="Leadership", is_skill_deleted=False)
            sk2 = Skill(skill_id=2, skill_name="Analytics", is_skill_deleted=False)
            sc1 = SkillCourse(sc_id=1, skill_id=1, course_id="COR001")
            sc2 = SkillCourse(sc_id=2, skill_id=2, course_id="COR001")
            db.session.add(c1)
            db.session.add(sk1)
            db.session.add(sk2)
            db.session.add(sc1)
            db.session.add(sc2)
            db.session.commit()
            req = self.client.delete("/remove_skill_course/" + str(sk2.skill_id) + "/"+ str(c1.course_id), content_type='application/json')
            req = req.json
            self.assertEqual(req['code'], 200)
            self.assertEqual(req['data'], 
            {'course_id': c1.course_id, 
            'sc_id': 2, 
            'skill_id': sk2.skill_id
            })

# Sprint 2 - View All Roles in the Organisation

class TestViewAllRolesInOrg(TestApp):
    def testSelectRole(self):
        with unittest.mock.patch("app.session", dict()) as session:
            client = app.test_client()
            client.get("/login/staff")
            r1 = Role(role_id=1, role_name='Software Developer', is_role_deleted=False)
            r2 = Role(role_id=2, role_name='Software Engineer', is_role_deleted=True)
            db.session.add(r1)
            db.session.add(r2)
            db.session.commit()
            self.client.get("/selectRole", content_type='application/json')
            self.assert_template_used('LJ_Roles.html')

            self.assert_context('roles_available', 
            {'roles_available': [{'is_role_deleted': False, 'role_id': 1, 'role_name': 'Software Developer'}]}
            )
            self.assert_context('all_roles',
            {'code': 200,
            'data': 
                {'roles': 
                [{'is_role_deleted': False, 'role_id': 1, 'role_name': 'Software Developer'},
                    {'is_role_deleted': True, 'role_id': 2, 'role_name': 'Software Engineer'}]
                }      
            })

    def testAddSkillCourse(self):
        with unittest.mock.patch("app.session", dict()) as session:
            client = app.test_client()
            client.get("/login/admin")
            c1 = Course(course_id="COR001", course_name="Systems Thinking and Design", course_desc="This foundation module aims to introduce students to the fundamental concepts and underlying principles of systems thinking,", course_status="Active", course_type="Internal", course_category="Core")
            sk1 = Skill(skill_id=1, skill_name="Leadership", is_skill_deleted=False)
            sk2 = Skill(skill_id=2, skill_name="Analytics", is_skill_deleted=False)
            sc1 = SkillCourse(sc_id=1, skill_id=1, course_id="COR001")
            db.session.add(c1)
            db.session.add(sk1)
            db.session.add(sk2)
            db.session.add(sc1)
            db.session.commit()
            req = self.client.post("/add_skill_course/" + str(sk2.skill_id) + "/"+ str(c1.course_id), content_type='application/json')
            req = req.json
            self.assertEqual(req['code'], 201)
            self.assertEqual(req['data'], 
            {'course_id': c1.course_id, 
            'sc_id': 2, 
            'skill_id': sk2.skill_id})
# Sprint 2 - Set Learning Journey
class TestSelectRole(TestApp):
    def testRetrieveAcquriedSkillFromRoleAndStaff(self):
        with unittest.mock.patch("app.session", dict()) as session:
            client = app.test_client()
            client.get("/login/staff")
            r1 = Role(role_id=1, role_name='Software Developer', is_role_deleted=False)
            sk1 = Skill(skill_id=1, skill_name="Leadership", is_skill_deleted=False)
            staff_id = session.get('staff_id')
            skr1 = SkillRole(skill_id=1, role_id=1, sr_id=1)
            db.session.add(r1)
            db.session.add(skr1)
            db.session.add(sk1)
            db.session.commit()
            self.client.get("/selectSkill/" + str(r1.role_id),
                                content_type='application/json')
            self.assert_template_used('LJ_Skills.html')
            self.assert_context('staff_id', staff_id)
            self.assert_context('error', {})
            self.assert_context('skills',  [{
                'is_skill_deleted': sk1.is_skill_deleted, 
                'skill_id': sk1.skill_id, 
                'skill_name': sk1.skill_name, 
                'acquired': False
            }])
            self.assert_context('role_name', r1.role_name)
            self.assert_context('role_id', r1.role_id)
    
    def testRetrieveNotAcquiredSkillFromRoleAndStaff(self):
        with unittest.mock.patch("app.session", dict()) as session:
            client = app.test_client()
            client.get("/login/staff")
            r1 = Role(role_id=1, role_name='Software Developer', is_role_deleted=False)
            sk1 = Skill(skill_id=1, skill_name="Leadership", is_skill_deleted=False)
            skr1 = SkillRole(skill_id=1, role_id=1, sr_id=1)
            db.session.add(r1)
            db.session.add(skr1)
            db.session.add(sk1)
            db.session.commit()
            self.client.get("/selectSkill/" + str(r1.role_id),
                                content_type='application/json')
            self.assert_template_used('LJ_Skills.html')
            self.assert_context('error', {})
            self.assert_context('staff_id', session.get('staff_id'))
            self.assert_context('skills',  [{
                'is_skill_deleted': sk1.is_skill_deleted, 
                'skill_id': sk1.skill_id, 
                'skill_name': sk1.skill_name, 
                'acquired': False
            }])
            self.assert_context('role_name', r1.role_name)
            self.assert_context('role_id', r1.role_id)

    def testNoSkillsAssignedToRole(self):
        with unittest.mock.patch("app.session", dict()) as session:
            client = app.test_client()
            client.get("/login/staff")
            r1 = Role(role_id=1, role_name='Software Developer', is_role_deleted=False)
            db.session.add(r1)
            db.session.commit()
            self.client.get("/selectSkill/" + str(r1.role_id),
                                content_type='application/json')
            self.assert_template_used('LJ_Skills.html')
            self.assert_context('staff_id', session.get('staff_id'))
            self.assert_context('error', {
                'code': 404, 
                'message': 'No skills have been assigned to the role - Software Developer'
            })
            self.assert_context('skills',  [])
            self.assert_context('role_name', r1.role_name)
            self.assert_context('role_id', r1.role_id)
           

class TestSelectSkill(TestApp):
    def testRetrieveCoursesFromSkillandCourse(self):
        with unittest.mock.patch("app.session", dict()) as session:
            print(self)
            client = app.test_client()
            client.get("/login/staff")
            r1 = Role(role_id=1, role_name='Software Developer', is_role_deleted=False)
            sk1 = Skill(skill_id=1, skill_name="Leadership", is_skill_deleted=False)
            c1 = Course(course_id="COR001", course_name="Systems Thinking and Design", course_desc="This foundation module aims to introduce students to the fundamental concepts and underlying principles of systems thinking,", course_status="Active", course_type="Internal", course_category="Core")
            sc1 = SkillCourse(sc_id=1, skill_id=1, course_id="COR001")
            db.session.add(r1)
            db.session.add(c1)
            db.session.add(sk1)
            db.session.add(sc1)
            db.session.commit()
            self.client.get("/selectCourse/" + str(r1.role_id) + '/' + str(sk1.skill_id),content_type='application/json')
            self.assert_template_used('LJ_Courses.html')
            self.assert_context('staff_id', session.get('staff_id'))
            self.assert_context('error', {})
            self.assert_context("course_details_of_skill_list",  [{
                'course_category': c1.course_category, 
                'course_desc': c1.course_desc, 
                'course_id': c1.course_id, 
                'course_name': c1.course_name, 
                'course_status': c1.course_status, 
                'course_type': c1.course_type, 
                'completion_status': "Not Started", 
            }])
            
    def testNoSkillsAssignedToCourse(self):
        with unittest.mock.patch("app.session", dict()) as session:
            client = app.test_client()
            client.get("/login/staff")
            r1 = Role(role_id=3, role_name='Data Analyst', is_role_deleted=False)
            sk1 = Skill(skill_id=6, skill_name="", is_skill_deleted=False)
            c1 = Course(course_id="MGT001", course_name="People Management", course_desc="enable learners to manage team performance and development through effective communication, conflict resolution and negotiation skills.", course_status="Active", course_type="Internal", course_category="Management")
            db.session.add(c1)
            db.session.add(r1)
            db.session.add(sk1)
            db.session.commit()
            self.client.get("/selectCourse/" + str(r1.role_id) + '/' + str(sk1.skill_id),content_type='application/json')
            self.assert_template_used('LJ_Courses.html')
            self.assert_context('staff_id', session.get('staff_id'))
            self.assert_context('error', { 
                'message': 'There are no courses available for this skill. Please select another skill.'
            })
            
# Sprint 3 - Add Courses to add to Exisiting Learning Journey
class TestAddCoursesForExistingLearningJourney(TestApp):
    def testSuccessfulGetCoursesForExistingLearningJourney(self):
        with unittest.mock.patch("app.session", dict()) as session:
            client = app.test_client()
            client.get("/login/staff")
            r1 = Role(role_id=1, role_name='Software Developer', is_role_deleted=False)
            s1 = Skill(skill_id=1, skill_name="Leadership", is_skill_deleted=False)
            lj1 = LearningJourney(lj_id=1, staff_id=session.get('staff_id'), role_id=1, skill_id=1, is_learningjourney_completed=False)
            c1 = Course(course_id="COR001", course_name="Systems Thinking and Design", course_desc="This foundation module aims to introduce students to the fundamental concepts and underlying principles of systems thinking,", course_status="Active", course_type="Internal", course_category="Core")
            c2 = Course(course_id="MGT001", course_name="People Management", course_desc="enable learners to manage team performance and development through effective communication, conflict resolution and negotiation skills.", course_status="Active", course_type="Internal", course_category="Management")
            sc1 =  SkillCourse(sc_id=1, skill_id=1, course_id="COR001")
            sc2 =  SkillCourse(sc_id=2, skill_id=1, course_id="MGT001")
            ljc1 = LearningJourneyCourse(ljc_id=1, lj_id=1, course_id="COR001", completion_status="Not Started", reg_status="Not Started")
            db.session.add(r1)
            db.session.add(s1)
            db.session.add(c1)
            db.session.add(c2)
            db.session.add(sc1)
            db.session.add(sc2)
            db.session.add(lj1)
            db.session.add(ljc1)
            db.session.commit()
            self.client.get("/getCoursesFromLj/" + str(lj1.lj_id),
                                content_type='application/json')
            self.assert_template_used('LJ_AddCourse.html')
            self.assert_context('staff_id', lj1.staff_id)
            self.assert_context('lj_id', lj1.lj_id)
            self.assert_context('error', [])
            self.assert_context('display_course_list',  [ 
                {
                'course_category': c1.course_category, 
                'course_desc': c1.course_desc, 
                'course_id': c1.course_id, 
                'course_name': c1.course_name, 
                'course_status': c1.course_status, 
                'course_type': c1.course_type, 
                'inLj': True
                },
                {
                'course_category': c2.course_category, 
                'course_desc': c2.course_desc, 
                'course_id': c2.course_id, 
                'course_name': c2.course_name, 
                'course_status': c2.course_status, 
                'course_type': c2.course_type, 
                'inLj': False,
                'completion_status': "Not Started",
                "reg_status": "Not Registered"
                }
            ])
            self.assert_context('position', 1)
    
    # /add_course_to_lj success
    def testAddCourseToExistingLearningJourneySuccess(self):
        with unittest.mock.patch("app.session", dict()) as session:
            client = app.test_client()
            client.get("/login/staff")
            lj1 = LearningJourney(lj_id=1, staff_id=session.get('staff_id'), role_id=1, skill_id=1, is_learningjourney_completed=False)
            c1 = Course(course_id="COR001", course_name="Systems Thinking and Design", course_desc="This foundation module aims to introduce students to the fundamental concepts and underlying principles of systems thinking,", course_status="Active", course_type="Internal", course_category="Core")
            c2 = Course(course_id="MGT001", course_name="People Management", course_desc="enable learners to manage team performance and development through effective communication, conflict resolution and negotiation skills.", course_status="Active", course_type="Internal", course_category="Management")
            db.session.add(c1)
            db.session.add(c2)
            db.session.add(lj1)
            db.session.commit()
            req = self.client.post("/add_course_to_lj", json={
                "lj_id":lj1.lj_id,
                "selected_course_id":c1.course_id+','+c2.course_id}, 
                content_type='application/json')
            req = req.json
            self.assertEqual(req['code'], 200)
            self.assertEqual(req['message'], 'Courses has been Successfully Added to Learning Journey')

    # /add_course_to_lj fail
    def testAddCourseToExistingLearningJourneyFail(self):
        with unittest.mock.patch("app.session", dict()) as session:
            client = app.test_client()
            client.get("/login/staff")
            lj1 = LearningJourney(lj_id=1, staff_id=session.get('staff_id'), role_id=1, skill_id=1, is_learningjourney_completed=False)
            c1 = Course(course_id="COR001", course_name="Systems Thinking and Design", course_desc="This foundation module aims to introduce students to the fundamental concepts and underlying principles of systems thinking,", course_status="Active", course_type="Internal", course_category="Core")
            c2 = Course(course_id="MGT001", course_name="People Management", course_desc="enable learners to manage team performance and development through effective communication, conflict resolution and negotiation skills.", course_status="Active", course_type="Internal", course_category="Management")
            db.session.add(c1)
            db.session.add(c2)
            db.session.add(lj1)
            db.session.commit()
            req = self.client.post("/add_course_to_lj", json={"lj_id":lj1.lj_id,"selected_course_id":""}, content_type='application/json')
            req = req.json
            self.assertEqual(req['code'], 400)
            self.assertEqual(req['message'], 'Please select at least one course to save into your learning journey.')
            
# Sprint 3 - View Saved Learning Journey Courses
class TestSelectSavedLearningJourney(TestApp):
    def testRetrieveSavedLearningJourneyCourses(self):
        with unittest.mock.patch("app.session", dict()) as session:
            print(self)
            client = app.test_client()
            client.get("/login/staff")
            staff_id = session.get('staff_id')
            r1 = Role(role_id=1, role_name='Software Developer', is_role_deleted=False)
            sk1 = Skill(skill_id=1, skill_name="Leadership", is_skill_deleted=False)
            c1 = Course(course_id="COR001", course_name="Systems Thinking and Design", course_desc="This foundation module aims to introduce students to the fundamental concepts and underlying principles of systems thinking,", course_status="Active", course_type="Internal", course_category="Core")
            lj1 = LearningJourney(lj_id=1, staff_id=staff_id, role_id=1, skill_id=1, is_learningjourney_completed=False)
            ljc1 = LearningJourneyCourse(ljc_id=1, lj_id=1, course_id="COR001", completion_status="Not Started", reg_status="Not Registered")
            db.session.add(r1)
            db.session.add(c1)
            db.session.add(sk1)
            db.session.add(lj1)
            db.session.add(ljc1)
            db.session.commit()
            self.client.get("/selectSavedLearningJourney/" + str(lj1.lj_id),content_type='application/json')
            self.assert_template_used('LJ_SavedCourses.html')
            self.assert_context('staff_id', staff_id)
            self.assert_context('error', {})
            self.assert_context('role_name', r1.role_name)
            self.assert_context('skill_name', sk1.skill_name)
            self.assert_context("course_data",  [({
                'completion_status': ljc1.completion_status,
                'course_id': ljc1.course_id, 
                'lj_id': ljc1.lj_id,
                'ljc_id': ljc1.ljc_id, 
                'reg_status': ljc1.reg_status,
            },
            {
                'course_category': c1.course_category, 
                'course_desc': c1.course_desc, 
                'course_id': c1.course_id, 
                'course_name': c1.course_name, 
                'course_status': c1.course_status, 
                'course_type': c1.course_type 
            })])
            self.assert_context('learningjourneycourses', {
                'code': 200,
                'data': {
                    'learning_journey_course': [{
                        'completion_status': ljc1.completion_status,
                        'course_id': ljc1.course_id, 
                        'lj_id': ljc1.lj_id,
                        'ljc_id': ljc1.ljc_id, 
                        'reg_status': ljc1.reg_status,
                    }]
                }
            })
            self.assert_context('lj_id', lj1.lj_id)
            self.assert_context('position', 1)
            
# Sprint 3 - View My Saved Learning Journeys
class TestViewAllLJ(TestApp):
    def testRetrieveAllLJ(self): #success
        with unittest.mock.patch("app.session", dict()) as session:
            print(self)
            client = app.test_client()
            client.get("/login/staff")
            r1 = Role(role_id=1, role_name='Software Developer', is_role_deleted=False)
            sk1 = Skill(skill_id=1, skill_name="Leadership", is_skill_deleted=False)
            c1 = Course(course_id="COR001", course_name="Systems Thinking and Design", course_desc="This foundation module aims to introduce students to the fundamental concepts and underlying principles of systems thinking,", course_status="Active", course_type="Internal", course_category="Core")
            lj1 = LearningJourney(lj_id=1, staff_id=session.get('staff_id'), role_id=1, skill_id=1, is_learningjourney_completed=False)
            ljc1 = LearningJourneyCourse(ljc_id=1, lj_id=1, course_id="COR001", completion_status="Not Started", reg_status="Not Registered")
            db.session.add(r1)
            db.session.add(c1)
            db.session.add(sk1)
            db.session.add(lj1)
            db.session.add(ljc1)
            db.session.commit()
            self.client.get("/my_learning_journey/" + str(session.get('staff_id')),content_type='application/json')
            self.assert_template_used('LJ_myLJ.html')
            self.assert_context('staff_id', session.get('staff_id'))
            self.assert_context("new_learningjourney",  [({
                'is_learningjourney_completed': lj1.is_learningjourney_completed,
                'lj_id': lj1.lj_id,
                'role_id': lj1.role_id, 
                'skill_id': lj1.skill_id,
                'staff_id': lj1.staff_id,
                'role_name': r1.role_name,
                'skill_name': sk1.skill_name,
                'course_count': 1,
                'completion_status': ljc1.completion_status,
                'counter': 1
            })])
            
    def testRetrieveAllLJ_butNoLJ(self): #failure - No LJ saved
        with unittest.mock.patch("app.session", dict()) as session:
            client = app.test_client()
            client.get("/login/staff")
            db.session.commit()
            self.client.get("/my_learning_journey/" + str(session.get('staff_id')),content_type='application/json')
            self.assert_template_used('LJ_myLJ.html')
            self.assert_context('staff_id', session.get('staff_id'))
            self.assert_context('error', { 
                'message': 'This staff has no learning journey.'
            })
            
# Sprint 3 - Remove Courses from Exisiting Learning Journey
class TestRemoveCoursesFromExistingLearningJourney(TestApp):
    def testRemoveACourseFromExistingLJ(self):
        with unittest.mock.patch("app.session", dict()) as session:
            client = app.test_client()
            client.get("/login/staff") 
            staff_id = session.get('staff_id')
            r1 = Role(role_id=1, role_name='Software Developer', is_role_deleted=False)
            sk1 = Skill(skill_id=1, skill_name="Leadership", is_skill_deleted=False)
            c1 = Course(course_id="COR001", course_name="Systems Thinking and Design", course_desc="This foundation module aims to introduce students to the fundamental concepts and underlying principles of systems thinking,", course_status="Active", course_type="Internal", course_category="Core")
            c2 = Course(course_id="MGT001", course_name="People Management", course_desc="enable learners to manage team performance and development through effective communication, conflict resolution and negotiation skills.", course_status="Active", course_type="Internal", course_category="Management")
            lj1 = LearningJourney(lj_id=1, staff_id=staff_id, role_id=1, skill_id=1, is_learningjourney_completed=False)
            ljc1 = LearningJourneyCourse(ljc_id=1, lj_id=1, course_id="COR001", completion_status="Not Started", reg_status="Not Registered")
            ljc2 = LearningJourneyCourse(ljc_id=2, lj_id=1, course_id="MGT001", completion_status="Not Started", reg_status="Not Registered")
            db.session.add(r1)
            db.session.add(c1)
            db.session.add(sk1)
            db.session.add(lj1)
            db.session.add(ljc1)
            db.session.add(ljc2)
            db.session.commit()
            req = self.client.delete("/delete_learning_journey_course/" + str(lj1.lj_id) + "/" + str(ljc1.ljc_id) , content_type='application/json')
            req = req.json
            self.assertEqual(req['code'], 200)
            self.assertEqual(req['message'], 'Course has been removed from Learning Journey.')

    def testRemoveACourseFromExistingLJourney_butOnlyOneCourse(self):
        with unittest.mock.patch("app.session", dict()) as session:
            client = app.test_client()
            client.get("/login/staff")
            staff_id = session.get('staff_id')
            r1 = Role(role_id=1, role_name='Software Developer', is_role_deleted=False)
            sk1 = Skill(skill_id=1, skill_name="Leadership", is_skill_deleted=False)
            c1 = Course(course_id="COR001", course_name="Systems Thinking and Design", course_desc="This foundation module aims to introduce students to the fundamental concepts and underlying principles of systems thinking,", course_status="Active", course_type="Internal", course_category="Core")
            c2 = Course(course_id="MGT001", course_name="People Management", course_desc="enable learners to manage team performance and development through effective communication, conflict resolution and negotiation skills.", course_status="Active", course_type="Internal", course_category="Management")
            lj1 = LearningJourney(lj_id=1, staff_id=staff_id, role_id=1, skill_id=1, is_learningjourney_completed=False)
            ljc1 = LearningJourneyCourse(ljc_id=1, lj_id=1, course_id="COR001", completion_status="Not Started", reg_status="Not Registered")
            db.session.add(r1)
            db.session.add(c1)
            db.session.add(sk1)
            db.session.add(lj1)
            db.session.add(ljc1)
            db.session.commit()
            req = self.client.delete("/delete_learning_journey_course/" + str(lj1.lj_id) + "/" + str(ljc1.ljc_id) , content_type='application/json')
            req = req.json
            self.assertEqual(req['code'], 400)
            self.assertEqual(req['message'], "Course can't be removed from Learning Journey as there is only one course left in the Learning Journey.")

# Sprint 3 - Delete Completed/New Learning Journey
class TestDeleteLearningJourney(TestApp):
    def testDeleteLJ(self):
        with unittest.mock.patch("app.session", dict()) as session:
            client = app.test_client()
            client.get("/login/admin")
            staff_id = session.get('staff_id')
            r1 = Role(role_id=1, role_name='Software Developer', is_role_deleted=False)
            sk1 = Skill(skill_id=1, skill_name="Leadership", is_skill_deleted=False)
            lj1 = LearningJourney(lj_id=1, staff_id=staff_id, role_id=1, skill_id=1, is_learningjourney_completed=False)
            db.session.add(r1)
            db.session.add(sk1)
            db.session.add(lj1)
            db.session.commit()
            req = self.client.delete("/delete_lj/" + str(lj1.lj_id), content_type='application/json')
            req = req.json
            self.assertEqual(req['code'], 200)
            self.assertEqual(req['data'], 
            {'is_learningjourney_completed': False,
                'lj_id': lj1.lj_id,
                'role_id': r1.role_id,
                'skill_id': sk1.skill_id,
                'staff_id': staff_id    
            })

if __name__ == '__main__':
    unittest.main()
 
 
