from django.test import TestCase
from django.core.urlresolvers import reverse
import Cookie


'''
All tests can be run by executing from terminal:
python manage.py test questionnaire
'''

# patient id's for testing in MiHIN server 4/2016
PATIENT_ID_CLARK = '11034584' #age 5
PATIENT_ID_DIANA = '18791962' #age 8
PATIENT_NAME_DIANA = 'Diana Prince'
PATIENT_NAME_CLARK = 'Clark Kent'
PATIENT_ID_BEATRICE = '18791983' #age 14
PATIENT_ID_TOBIAS = '18792004' #age 15
PATIENT_ID_UNDERAGE = 'Patient-13244' #dob 2016-01-08
PATIENT_ID_INVALID = '19999999' #assume does not exist!
PATIENT_ID_AGE2 = 'Patient-22774' #dob 2013-12-29
PATIENT_ID_AGE12 = 'Patient-12611' #dob 2004-02-27
PATIENT_ID_AGE13 = 'Patient-20090' #dob 2003-02-23
PATIENT_ID_AGE18 = 'Patient-17877' #dob 1998-04-01
PATIENT_ID_AGE19 = 'Patient-17458' #dob 1997-02-04
MAIN_PAGE = "Select a patient"
INVALID_ID_MSG = "appears to be invalid"
ABOUT_MSG = "Usage Information"
HISTORY_RESPONSES_MSG = "Your past responses:"

# class Model_Tests_1(TestCase):
#     def test_model_placeholder(self):
#         test_value = False
#         self.assertTrue(test_value,"Add model tests when models available")

class View_Index_Tests(TestCase):
    """
    test main view
    """
    def test_view_exists(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<title>Questionnaire</title>")

    # not implemented
    # def test_has_login(self):
    #     response = self.client.get(reverse('index'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, "Username")
    #     self.assertContains(response, "Password")
    #     self.assertContains(response, "Login")
    #
    # def test_footer_found(self):
    #     response = self.client.get(reverse('respond'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, "Terms of Use")
    #     self.assertContains(response, "Privacy Statement")
    #     self.assertContains(response, "FAQs")
    #     self.assertContains(response, "Support")

class View_About_Tests(TestCase):
    """
    test about view
    """
    def test_view_exists(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, ABOUT_MSG)

class View_Messages_Tests(TestCase):
    """
    test Messages view
    """
    def test_no_id(self):
        response = self.client.get(reverse('messages'),follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, MAIN_PAGE)

    def test_badID(self):
        """
        test respond view when patient is adolescent
        set cookie to userID for Tobias age 15
        """
        C = Cookie.SimpleCookie()
        C["userId"] = 19999999
        self.client.cookies = C
        response = self.client.get(reverse('messages'),follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, INVALID_ID_MSG)

    def test_patient_found(self):
        """
        test respond view when valid patient chosen
        """
        C = Cookie.SimpleCookie()
        C["userId"]= PATIENT_ID_DIANA
        C["serverId"] = "MiHIN"
        self.client.cookies=C
        response = self.client.get(reverse('messages'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "messages")  # find narrower check for with and without messages but valid

class View_History_Tests(TestCase):
    """
    test History view
    """
    def test_no_id(self):
        """
        test respond view when no id is set yet, i.e. no login has occurred
        """
        response = self.client.get(reverse('history'),follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, MAIN_PAGE)

    def test_badID(self):
        """
        test respond view when patient is adolescent
        set cookie to userID for Tobias age 15
        """
        C = Cookie.SimpleCookie()
        C["userId"] = PATIENT_ID_INVALID
        C["serverId"] = "MiHIN"
        self.client.cookies = C
        response = self.client.get(reverse('history'),follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, INVALID_ID_MSG)

    def test_patient_found(self):
        """
        test respond view when valid patient chosen
        """
        C = Cookie.SimpleCookie()
        C["userId"]= PATIENT_ID_DIANA
        self.client.cookies=C
        response = self.client.get(reverse('history'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, HISTORY_RESPONSES_MSG)

class View_Respond_Tests(TestCase):

    def test_no_id(self):
        """
        test respond view when no id is set yet, i.e. no login has occurred
        """
        response = self.client.get(reverse('respond'),follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, MAIN_PAGE)

    def test_badID(self):
        """
        test respond view when patient is adolescent
        set cookie to userID for Tobias age 15
        """
        C = Cookie.SimpleCookie()
        C["userId"] = 19999999
        C["serverId"] = "MiHIN"
        self.client.cookies = C
        response = self.client.get(reverse('respond'),follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, INVALID_ID_MSG)

    def test_patient_found(self):
        """
        test respond view when valid patient chosen
        """
        C = Cookie.SimpleCookie()
        C["userId"]= PATIENT_ID_CLARK
        self.client.cookies=C
        response = self.client.get(reverse('respond'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['patientName'], PATIENT_NAME_CLARK)

    # not implemented
    # def test_footer_found_child(self):
    #     """
    #     test respond view footer items
    #     """
    #     C = Cookie.SimpleCookie()
    #     C["userId"] = PATIENT_ID_DIANA
    #     self.client.cookies = C
    #     response = self.client.get(reverse('respond'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, "Terms of Use")
    #     self.assertContains(response, "Privacy Statement")
    #     self.assertContains(response, "FAQs")
    #     self.assertContains(response, "Support")

    def test_child_questionnaire(self):
        """
        test respond view when patient is child
        set cookie to userID for Diana age 8
        """
        C = Cookie.SimpleCookie()
        C["userId"]= PATIENT_ID_DIANA
        self.client.cookies=C
        response = self.client.get(reverse('respond'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "My child eats")

    def test_teen_questionnaire(self):
        """
        test respond view when patient is adolescent
        set cookie to userID for Tobias age 15
        """
        C = Cookie.SimpleCookie()
        C["userId"] = PATIENT_ID_TOBIAS
        self.client.cookies=C
        response = self.client.get(reverse('respond'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "I eat")

    def test_child_name_shown(self):
        """
        test respond view when patient is adolescent
        set cookie to userID for Tobias age 15
        """
        C = Cookie.SimpleCookie()
        C["userId"] = PATIENT_ID_DIANA
        self.client.cookies = C
        response = self.client.get(reverse('respond'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Diana")

    def test_teen_name_shown(self):
        """
        test respond view when patient is adolescent
        set cookie to userID for Tobias age 15
        """
        C = Cookie.SimpleCookie()
        C["userId"] = PATIENT_ID_TOBIAS
        self.client.cookies=C
        response = self.client.get(reverse('respond'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tobias")

# age edge cases - not implemented
#     def test_below_min_age(self):
#         """
#         test respond view when patient is <2 years old
#         """
#         C = Cookie.SimpleCookie()
#         C["userId"] = PATIENT_ID_UNDERAGE
#         self.client.cookies = C
#         response = self.client.get(reverse('respond'))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "Patient is younger than 2")
#         # self.assertEqual(response.context['patientName'], 'Aaron Daryl Conner')
#
#
#     def test_over_max_age_view(self):
#         """
#         test respond view when patient is >18 years old
#         """
#         C = Cookie.SimpleCookie()
#         C["userId"] = PATIENT_ID_AGE19
#         self.client.cookies = C
#         response = self.client.get(reverse('respond'))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "Patient is older than 18")
#
    def test_child_age_2(self):
        """
        test respond view when patient is 2 years old (edge case)
        """
        C = Cookie.SimpleCookie()
        C["userId"] = PATIENT_ID_AGE2
        C["serverId"] = "MiHIN"
        self.client.cookies = C
        response = self.client.get(reverse('respond'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "My child eats")

    def test_child_age_12(self):
        """
        test respond view when patient is 12 years old
        """
        C = Cookie.SimpleCookie()
        C["userId"] = PATIENT_ID_AGE12
        C["serverId"] = "MiHIN"
        self.client.cookies = C
        response = self.client.get(reverse('respond'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "My child eats")

    def test_teen_age_13(self):
        """
        test respond view when patient is 13 years old
        """
        C = Cookie.SimpleCookie()
        C["userId"] = PATIENT_ID_AGE13
        C["serverId"] = "MiHIN"
        self.client.cookies = C
        response = self.client.get(reverse('respond'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "I eat")

    def test_teen_age_18(self):
        """
        test respond view when patient is <2 years old
        """
        C = Cookie.SimpleCookie()
        C["userId"] = PATIENT_ID_AGE18
        C["serverId"] = "MiHIN"
        self.client.cookies = C
        response = self.client.get(reverse('respond'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "I eat")

# test all child questions
    '''
    checks to see if the text is on the page but does not
    verify that it is correctly located or that radio buttons are there
    '''
    def test_child_question1_onpage(self):
        C = Cookie.SimpleCookie()
        C["userId"] = PATIENT_ID_DIANA
        self.client.cookies = C
        response = self.client.get(reverse('respond'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "My child eats veggies and fruits:")
        self.assertContains(response, "0-1 times a day")
        self.assertContains(response, "1-2 times a day")
        self.assertContains(response, "3-4 times a day")
        self.assertContains(response, "5 or more times a day")

    def test_child_question2_onpage(self):
        C = Cookie.SimpleCookie()
        C["userId"] = PATIENT_ID_DIANA
        self.client.cookies = C
        response = self.client.get(reverse('respond'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "My child is active:")
        self.assertContains(response, "Not very often")
        self.assertContains(response, "Less than 30 minutes a day")
        self.assertContains(response, "30-60 minutes a day")
        self.assertContains(response, "More than 60 minutes a day")

    def test_child_question3_onpage(self):
        C = Cookie.SimpleCookie()
        C["userId"] = PATIENT_ID_DIANA
        self.client.cookies = C
        response = self.client.get(reverse('respond'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "My child drinks 100\x25 fruit juice:")
        self.assertContains(response, "More than 3 cups a day")
        self.assertContains(response, "2 cups a day")
        self.assertContains(response, "1 cup a day")
        self.assertContains(response, "Not very often")

    def test_child_question4_onpage(self):
        C = Cookie.SimpleCookie()
        C["userId"] = PATIENT_ID_DIANA
        self.client.cookies = C
        response = self.client.get(reverse('respond'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "My child has sweet drinks (soda, sweet tea, sports drinks, other fruit drinks):")
        self.assertContains(response, "More than 3 cups a day")
        self.assertContains(response, "2 cups a day")
        self.assertContains(response, "1 cup a day")
        self.assertContains(response, "Not very often")

    def test_child_question5_onpage(self):
        C = Cookie.SimpleCookie()
        C["userId"] = PATIENT_ID_DIANA
        self.client.cookies = C
        response = self.client.get(reverse('respond'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "My child eats foods like brownies, muffins, cakes or cookies:")
        self.assertContains(response, "Not very often")
        self.assertContains(response, "1-2 times per week")
        self.assertContains(response, "3-4 times per week")
        self.assertContains(response, "5 or more times a week")

    def test_child_question6_onpage(self):
        C = Cookie.SimpleCookie()
        C["userId"] = PATIENT_ID_DIANA
        self.client.cookies = C
        response = self.client.get(reverse('respond'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "My child watches television, plays video games, spends (non-school related) time on a computer, tablet or cell phone:")
        self.assertContains(response, "Not very often")
        self.assertContains(response, "1-2 hours a day")
        self.assertContains(response, "3-4 hours a day")
        self.assertContains(response, "5 or more hours a day")

    def test_child_question7_onpage(self):
        C = Cookie.SimpleCookie()
        C["userId"] = PATIENT_ID_DIANA
        self.client.cookies = C
        response = self.client.get(reverse('respond'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "If you and your child could work on one healthy habit, which would it be?")
        self.assertContains(response, "Make half your plate veggies and fruits")
        self.assertContains(response, "Limit screen time")
        self.assertContains(response, "Be more active")
        self.assertContains(response, "Drink more water and limit sugary drinks")

    def test_child_question8_onpage(self):
        C = Cookie.SimpleCookie()
        C["userId"] = PATIENT_ID_DIANA
        self.client.cookies = C
        response = self.client.get(reverse('respond'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "How important is it to you that your child works on this healthy habit?")
        self.assertContains(response, "NOT AT ALL")
        self.assertContains(response, "VERY")

    def test_child_question9_onpage(self):
        C = Cookie.SimpleCookie()
        C["userId"]= PATIENT_ID_DIANA
        self.client.cookies=C
        response = self.client.get(reverse('respond'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "How confident are you that your child can improve on this healthy habit?")
        self.assertContains(response, "NOT AT ALL")
        self.assertContains(response, "VERY")

# test all adolescent questions
    '''
    checks to see if the text is on the page but does not
    verify that it is correctly located or that radio buttons are there
    '''
    def test_teen_question1_onpage(self):
        C = Cookie.SimpleCookie()
        C["userId"] = PATIENT_ID_TOBIAS
        self.client.cookies = C
        response = self.client.get(reverse('respond'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "I eat veggies and fruits:")
        self.assertContains(response, "0-1 times a day")
        self.assertContains(response, "1-2 times a day")
        self.assertContains(response, "3-4 times a day")
        self.assertContains(response, "5 or more times a day")

    def test_teen_question2_onpage(self):
        C = Cookie.SimpleCookie()
        C["userId"] = PATIENT_ID_TOBIAS
        self.client.cookies = C
        response = self.client.get(reverse('respond'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "I eat out:")
        self.assertContains(response, "More than 4 times a week")
        self.assertContains(response, "3-4 times a week")
        self.assertContains(response, "1-2 times a week")
        self.assertContains(response, "0-1 times a week")

    def test_teen_question3_onpage(self):
        C = Cookie.SimpleCookie()
        C["userId"] = PATIENT_ID_TOBIAS
        self.client.cookies = C
        response = self.client.get(reverse('respond'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "I am active:")
        self.assertContains(response, "Not very often")
        self.assertContains(response, "Less than 30 minutes a day")
        self.assertContains(response, "30-60 minutes a day")
        self.assertContains(response, "More than 60 minutes a day")

    def test_teen_question4_onpage(self):
        C = Cookie.SimpleCookie()
        C["userId"] = PATIENT_ID_TOBIAS
        self.client.cookies = C
        response = self.client.get(reverse('respond'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "I have sweet drinks (soda, sweet tea, sports drinks, 100\x25 fruit juice, other fruit drinks):")
        self.assertContains(response, "3 or more cups a day")
        self.assertContains(response, "2 cups a day")
        self.assertContains(response, "1 cup a day")
        self.assertContains(response, "Not very often")

    def test_teen_question5_onpage(self):
        C = Cookie.SimpleCookie()
        C["userId"] = PATIENT_ID_TOBIAS
        self.client.cookies = C
        response = self.client.get(reverse('respond'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "I eat foods like brownies, muffins, cakes or cookies:")
        self.assertContains(response, "Not very often")
        self.assertContains(response, "1 time a day")
        self.assertContains(response, "2 times a day")
        self.assertContains(response, "3 or more times a day")

    def test_teen_question6_onpage(self):
        C = Cookie.SimpleCookie()
        C["userId"] = PATIENT_ID_TOBIAS
        self.client.cookies = C
        response = self.client.get(reverse('respond'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "I watch television, play video games, spend (non-school related) time on a computer, tablet or cell phone:")
        self.assertContains(response, "Not very often")
        self.assertContains(response, "1 hour a day")
        self.assertContains(response, "1-2 hours a day")
        self.assertContains(response, "3-4 hours a day")
        self.assertContains(response, "5 or more hours a day")

    def test_teen_question7_onpage(self):
        C = Cookie.SimpleCookie()
        C["userId"] = PATIENT_ID_TOBIAS
        self.client.cookies = C
        response = self.client.get(reverse('respond'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "If you could work on one healthy habit, which would it be?")
        self.assertContains(response, "Make half your plate veggies and fruits")
        self.assertContains(response, "Limit screen time")
        self.assertContains(response, "Be more active")
        self.assertContains(response, "Drink more water and limit sugary drinks")

    def test_teen_question8_onpage(self):
        C = Cookie.SimpleCookie()
        C["userId"] = PATIENT_ID_TOBIAS
        self.client.cookies = C
        response = self.client.get(reverse('respond'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "How important is it to you to work on this healthy habit?")
        self.assertContains(response, "NOT AT ALL")
        self.assertContains(response, "VERY")

    def test_teen_question9_onpage(self):
        C = Cookie.SimpleCookie()
        C["userId"] = PATIENT_ID_TOBIAS
        self.client.cookies = C
        response = self.client.get(reverse('respond'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "How confident are you that you can improve this healthy habit?")
        self.assertContains(response, "NOT AT ALL")
        self.assertContains(response, "VERY")


