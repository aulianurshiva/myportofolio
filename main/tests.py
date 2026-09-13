from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Interest


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            started_at = timezone.now(),
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Present")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "No experiences added yet.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        response = self.client.get(reverse("main:show_experience"))
        self.assertNotContains(response, "Present")

class InterestTest(TestCase):
    def setUp(self):
        self.interest = Interest.objects.create(
            name="Gaming",
            category="fun",
            description="I play games whenever I have the time.",
        )

    def test_interest_url_is_accessible(self):
        response = self.client.get(reverse("main:show_interest"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "interest.html")

    def test_interest_model(self):
        self.assertEqual(str(self.interest), "Gaming")
        self.assertEqual(self.interest.category, "fun")

    def test_interest_page_shows_data(self):
        response = self.client.get(reverse("main:show_interest"))

        self.assertContains(response, self.interest.name)
        self.assertContains(response, self.interest.description)

    def test_empty_interest_page(self):
        Interest.objects.all().delete()
        response = self.client.get(reverse("main:show_interest"))

        self.assertContains(response, "Nothing added yet.")