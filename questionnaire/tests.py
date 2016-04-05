from django.test import TestCase
from django.core.urlresolvers import reverse
import Cookie

'''
All tests can be run by executing from terminal:
python manage.py test questionnaire
'''

# class Model_Tests_1(TestCase):
#     def test_model_placeholder(self):
#         test_value = False
#         self.assertTrue(test_value,"Add model tests when models available")
#
# class Model_Tests_2(TestCase):
#     def test_model_placeholder(self):
#         test_value = False
#         self.assertTrue(test_value,"Add model tests when models available")
#
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
        self.assertContains(response, "Healthy Habits Tracker")

    # edge cases
    # def test_child_under_min_age_view(self):
    #     """
    #     test respond view when patient is <2 years old
    #     """
    #     response = self.client.get(reverse('respond'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, "Patient is younger than 2")
    #
    # def test_child_over_max_age_view(self):
    #     """
    #     test respond view when patient is >18 years old
    #     """
    #     response = self.client.get(reverse('respond'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, "Patient is older than 18")
    #
    # def test_child_age_2_view(self):
    #     """
    #     test respond view when patient is 2 years old (edge case)
    #     """
    #     response = self.client.get(reverse('respond'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, "My child eats")
    #
    # def test_child_age_12_view(self):
    #     """
    #     test respond view when patient is <2 years old
    #     """
    #     response = self.client.get(reverse('respond'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, "My child eats")
    #
    # def test_adolescent_age_13_view(self):
    #     """
    #     test respond view when patient is <2 years old
    #     """
    #     response = self.client.get(reverse('respond'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, "I eat")
    #
    # def test_adolescent_age_17_view(self):
    #     """
    #     test respond view when patient is <2 years old
    #     """
    #     response = self.client.get(reverse('respond'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, "I eat")

    def test_child_view(self):
        """
        test respond view when patient is child
        set cookie to userID for Diana age 8
        """
        C = Cookie.SimpleCookie()
        C["userId"]= 18791962
        self.client.cookies=C
        response = self.client.get(reverse('respond'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['patientName'], 'Diana Prince')

    def test_adolescent_view(self):
        """
        test respond view when patient is adolescent
        set cookie to userID for Tobias age 15
        """
        C = Cookie.SimpleCookie()
        C["userId"] = 18792004
        self.client.cookies=C
        response = self.client.get(reverse('respond'))
        patient_name = response.context['patientName']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['patientName'], 'Tobias Eaton')

    def test_badID_view(self):
        """
        test respond view when patient is adolescent
        set cookie to userID for Tobias age 15
        """
        C = Cookie.SimpleCookie()
        C["userId"] = 18799999
        self.client.cookies = C
        response = self.client.get(reverse('respond'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Error Page")


