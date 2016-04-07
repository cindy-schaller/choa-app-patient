from django.test import TestCase
from django.core.urlresolvers import reverse
import Cookie

'''
All tests can be run by executing from terminal:
python manage.py test questionnaire
'''

# patient id's for testing in MiHIN server 4/2016
PATIENT_ID_CLARK = '18791941' #age 10
PATIENT_ID_DIANA = '18791962' #age 8
PATIENT_NAME_DIANA = 'Diana Prince'
PATIENT_ID_BEATRICE = '18791983' #age 14
PATIENT_ID_TOBIAS = '18792004' #age 15
PATIENT_ID_UNDERAGE = 'Patient-13244' #dob 2016-01-08
PATIENT_ID_AGE2 = 'Patient-22774' #dob 2013-12-29
PATIENT_ID_AGE12 = 'Patient-12611' #dob 2004-02-27
PATIENT_ID_AGE13 = 'Patient-20090' #dob 2003-02-23
PATIENT_ID_AGE18 = 'Patient-17877' #dob 1998-04-01
PATIENT_ID_AGE19 = 'Patient-17458' #dob 1997-02-04

# class Model_Tests_1(TestCase):
#     def test_model_placeholder(self):
#         test_value = False
#         self.assertTrue(test_value,"Add model tests when models available")

class View_Index_Tests(TestCase):
    def test_index_view_exists(self):
        """
        test main view
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Questionnaire")

class View_About_Tests(TestCase):
    def test_index_view_exists(self):
        """
        test about view
        """
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A project of the Frogs")

class View_Respond_Tests(TestCase):

    def test_no_id_view(self):
        """
        test respond view when no id is set yet, i.e. no login has occurred
        """
        response = self.client.get(reverse('respond'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The user you've selected appears to be invalid.")

    def test_badID_view(self):
        """
        test respond view when patient is adolescent
        set cookie to userID for Tobias age 15
        """
        C = Cookie.SimpleCookie()
        C["userId"] = 19999999
        self.client.cookies = C
        response = self.client.get(reverse('respond'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The user you've selected appears to be invalid.")

    def test_patient_found(self):
        """
        test respond view when valid patient chosen
        """
        C = Cookie.SimpleCookie()
        C["userId"]= PATIENT_ID_DIANA
        self.client.cookies=C
        response = self.client.get(reverse('respond'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['patientName'], PATIENT_NAME_DIANA)

    def test_child_view(self):
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

    def test_adolescent_view(self):
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

# age edge cases
    def test_child_below_min_age(self):
        """
        test respond view when patient is <2 years old
        """
        C = Cookie.SimpleCookie()
        C["userId"] = PATIENT_ID_UNDERAGE
        self.client.cookies = C
        response = self.client.get(reverse('respond'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Patient is younger than 2")
        # self.assertEqual(response.context['patientName'], 'Aaron Daryl Conner')


    def test_child_over_max_age_view(self):
        """
        test respond view when patient is >18 years old
        """
        C = Cookie.SimpleCookie()
        C["userId"] = PATIENT_ID_AGE19
        self.client.cookies = C
        response = self.client.get(reverse('respond'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Patient is older than 18")

    def test_child_age_2_view(self):
        """
        test respond view when patient is 2 years old (edge case)
        """
        C = Cookie.SimpleCookie()
        C["userId"] = PATIENT_ID_AGE2
        self.client.cookies = C
        response = self.client.get(reverse('respond'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "My child eats")

    def test_child_age_12_view(self):
        """
        test respond view when patient is 12 years old
        """
        C = Cookie.SimpleCookie()
        C["userId"] = PATIENT_ID_AGE12
        self.client.cookies = C
        response = self.client.get(reverse('respond'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "My child eats")

    def test_adolescent_age_13_view(self):
        """
        test respond view when patient is 13 years old
        """
        C = Cookie.SimpleCookie()
        C["userId"] = PATIENT_ID_AGE13
        self.client.cookies = C
        response = self.client.get(reverse('respond'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "I eat")

    def test_adolescent_age_18_view(self):
        """
        test respond view when patient is <2 years old
        """
        C = Cookie.SimpleCookie()
        C["userId"] = PATIENT_ID_AGE18
        self.client.cookies = C
        response = self.client.get(reverse('respond'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "I eat")


