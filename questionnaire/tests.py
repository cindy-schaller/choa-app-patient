from django.test import TestCase
from django.core.urlresolvers import reverse

# Create your tests here
class TesterTests1(TestCase):
    def testTF(self):
        test_value = True
        self.assertFalse(test_value,"This should always fail 1")

    def testFT1(self):
        test_value = False
        self.assertTrue(test_value,"This should always fail 2")

class TesterTests2(TestCase):
    def testTF(self):
        test_value = True
        self.assertFalse(test_value,"This should always fail 3")

    def testFT1(self):
        test_value = False
        self.assertTrue(test_value,"This should always fail 4")

class ViewTests(TestCase):
    def test_index_view_exists(self):
        """
        test basic view
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Questionnaire")
