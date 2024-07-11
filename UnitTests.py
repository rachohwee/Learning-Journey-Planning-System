import unittest
import unittest.mock
from unittest import mock
from Role import Role
from Skill import Skill
from StaffSkill import StaffSkill
from SkillCourse import SkillCourse
from Course import Course
from LearningJourney import LearningJourney
from Registration import Registration
from SkillRole import SkillRole

class testRole(unittest.TestCase):
    def test_json(self):
        r1 = Role(role_id=None, role_name='Frontend Developer', is_role_deleted=False)
        self.assertEquals({
            'role_id': r1.role_id,
            'role_name': r1.role_name,
            'is_role_deleted': r1.is_role_deleted
        }, r1.json())
        
class testSkill(unittest.TestCase):   
    def test_json(self):
        s1 = Skill(skill_id=None, skill_name='Leadership', is_skill_deleted=False)
        self.assertEquals({
            'skill_id': s1.skill_id,
            'skill_name': s1.skill_name,
            'is_skill_deleted': s1.is_skill_deleted
        }, s1.json())

class testCourse(unittest.TestCase):   
    def test_json(self):
        c1 = Course(course_id='COR001', course_name='Systems Thinking and Design', course_desc='This foundation module aims to introduce students ...', course_status='Active', course_type='Internal', course_category='Core')
        self.assertEquals({
            'course_id': c1.course_id,
            'course_name': c1.course_name,
            'course_desc': c1.course_desc,
            'course_status': c1.course_status,
            'course_type': c1.course_type,
            'course_category': c1.course_category,
        }, c1.json())

class testStaffSKill(unittest.TestCase):
    def setup(self):
        self.s1 = Skill(1, 'Leadership', False)
        self.sk1 = StaffSkill(None, 1, 13001)

    def test_json(self):
        s1 = Skill(skill_id=None, skill_name='Leadership', is_skill_deleted=False)
        sk1 = StaffSkill(sk_id=None, skill_id=s1.skill_id, staff_id=13001)
        self.assertEquals({
            'sk_id': sk1.sk_id,
            'skill_id': sk1.skill_id,
            'staff_id': sk1.staff_id
        }, sk1.json())

class testSkillCourse(unittest.TestCase):
    def test_json(self):
        s1 = Skill(skill_id=None, skill_name='Leadership', is_skill_deleted=False)
        c1 = Course(course_id='COR001', course_name='Systems Thinking and Design', course_desc='This foundation module aims to introduce students ...', course_status='Active', course_type='Internal', course_category='Core')
        sc1 = SkillCourse(sc_id=None, skill_id=s1.skill_id, course_id=c1.course_id)
        
        self.assertEquals({
            'sc_id': sc1.sc_id,
            'skill_id': sc1.skill_id,
            'course_id': sc1.course_id
        }, sc1.json())
        
class testLearningJourney(unittest.TestCase):
    def test_json(self):
        s1 = Skill(skill_id=None, skill_name='Leadership', is_skill_deleted=False)
        r1 = Role(role_id=None, role_name='Frontend Developer', is_role_deleted=False)
        lj1 = LearningJourney(lj_id=None, staff_id=13001, role_id=r1.role_id,  skill_id=s1.skill_id, is_learningjourney_completed=True)
        
        self.assertEquals({
            'lj_id': lj1.lj_id,
            'staff_id': lj1.staff_id,
            'role_id': lj1.role_id,
            'skill_id': lj1.skill_id,
            'is_learningjourney_completed': lj1.is_learningjourney_completed
        }, lj1.json())
        
class testRegistration(unittest.TestCase):
    def test_json(self):
        c1 = Course(course_id=None, course_name="Systems Thinking and Design", 
        course_desc="This foundation module aims to introduce students to the fundamental concepts and underlying principles of systems thinking,", 
        course_status="Active", course_type="Internal", course_category="Core", )
        rg1 = Registration(reg_id=None, course_id=c1.course_id, staff_id=13001, reg_status='Registered', 
        completion_status='Completed')
        self.assertEquals({
            'reg_id': rg1.reg_id,
            'course_id': rg1.course_id,
            'staff_id': rg1.staff_id,
            'reg_status': rg1.reg_status,
            'completion_status': rg1.completion_status
        }, rg1.json())
        
class testSkillRole(unittest.TestCase):
    def test_json(self):
        s1 = Skill(skill_id=None, skill_name='Leadership', is_skill_deleted=False)
        r1 = Role(role_id=None, role_name='Frontend Developer', is_role_deleted=False)
        skr1 = SkillRole(sr_id=None, role_id=r1.role_id, skill_id=s1.skill_id)
        self.assertEquals({
            'sr_id': skr1.sr_id,
            'role_id': skr1.role_id,
            'skill_id': skr1.skill_id
        }, skr1.json())
    
        

        
        
if __name__ == "__main__":
    unittest.main()