from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Interest

EXPERIENCE_FORM = {
    "title": "New Role",
    "description": "Doing something new.",
    "thumbnail": "",
    "started_at": "2026-01-01T00:00",
    "ended_at": "",
}


class BaseTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            started_at=timezone.now(),
        )
        self.interest = Interest.objects.create(
            name="Gaming",
            category="fun",
            description="I play games whenever I have the time.",
        )
        self.regular = User.objects.create_user("regular", password="pw12345!")
        self.editor = User.objects.create_user("editor", password="pw12345!")
        self.editor.groups.add(Group.objects.create(name="Editor"))
        self.owner = User.objects.create_superuser("owner", password="pw12345!")

        self.create_url = reverse("main:create_experience")
        self.update_url = reverse("main:update_experience", args=[self.experience.id])
        self.delete_url = reverse("main:delete_experience", args=[self.experience.id])
        self.star_url = reverse("main:toggle_star_experience", args=[self.experience.id])

    def login_as(self, user):
        self.client.force_login(user)


class MainTest(BaseTest):
    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_nonexistent_page_returns_404(self):
        self.assertEqual(self.client.get("/halaman-yang-tidak-ada/").status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page_is_public(self):
        response = self.client.get(reverse("main:show_experience"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")

class ExperienceAccessTest(BaseTest):
    # --- pengunjung tanpa login: redirect ke login ---
    def test_anonymous_redirected_to_login(self):
        for url in (self.create_url, self.update_url, self.delete_url, self.star_url):
            response = self.client.post(url, EXPERIENCE_FORM)
            self.assertEqual(response.status_code, 302)
            self.assertTrue(response.url.startswith("/login/"))
        self.assertFalse(Experience.objects.filter(title="New Role").exists())
        self.assertEqual(self.experience.starred_by.count(), 0)

    # --- user biasa: 403 untuk create/update/delete ---
    def test_regular_user_forbidden(self):
        self.login_as(self.regular)
        self.assertEqual(self.client.post(self.create_url, EXPERIENCE_FORM).status_code, 403)
        self.assertEqual(self.client.post(self.update_url, EXPERIENCE_FORM).status_code, 403)
        self.assertEqual(self.client.post(self.delete_url).status_code, 403)
        self.assertTrue(Experience.objects.filter(id=self.experience.id).exists())
        self.assertFalse(Experience.objects.filter(title="New Role").exists())

    # --- editor: hanya boleh update ---
    def test_editor_can_update_only(self):
        self.login_as(self.editor)
        response = self.client.post(self.update_url, EXPERIENCE_FORM)
        self.assertEqual(response.status_code, 302)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "New Role")

        self.assertEqual(self.client.post(self.create_url, EXPERIENCE_FORM).status_code, 403)
        self.assertEqual(self.client.post(self.delete_url).status_code, 403)
        self.assertTrue(Experience.objects.filter(id=self.experience.id).exists())

    # --- superuser: create, update, delete ---
    def test_owner_can_create_update_delete(self):
        self.login_as(self.owner)
        self.assertEqual(self.client.post(self.create_url, EXPERIENCE_FORM).status_code, 302)
        self.assertTrue(Experience.objects.filter(title="New Role").exists())

        data = dict(EXPERIENCE_FORM, title="Updated Title")
        self.assertEqual(self.client.post(self.update_url, data).status_code, 302)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Updated Title")

        self.assertEqual(self.client.post(self.delete_url).status_code, 302)
        self.assertFalse(Experience.objects.filter(id=self.experience.id).exists())

    def test_role_flags_and_modal_by_role(self):
        list_url = reverse("main:show_experience")

        response = self.client.get(list_url)  # anonim
        self.assertContains(response, 'const CAN_EDIT = "false"')
        self.assertContains(response, 'const IS_SUPERUSER = "false"')
        self.assertNotContains(response, 'id="add-experience-modal"')

        self.login_as(self.editor)
        response = self.client.get(list_url)
        self.assertContains(response, 'const CAN_EDIT = "true"')
        self.assertContains(response, 'const IS_SUPERUSER = "false"')
        self.assertNotContains(response, 'id="add-experience-modal"')

        self.login_as(self.owner)
        response = self.client.get(list_url)
        self.assertContains(response, 'const CAN_EDIT = "true"')
        self.assertContains(response, 'const IS_SUPERUSER = "true"')
        self.assertContains(response, 'id="add-experience-modal"')

class ExperienceAjaxTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.ajax_create_url = reverse("main:create_experience_ajax")

    def test_create_requires_post(self):
        self.login_as(self.owner)
        self.assertEqual(self.client.get(self.ajax_create_url).status_code, 405)

    def test_create_forbidden_for_non_owner(self):
        for user in (None, self.regular, self.editor):
            if user:
                self.login_as(user)
            response = self.client.post(self.ajax_create_url, EXPERIENCE_FORM)
            self.assertEqual(response.status_code, 403)
            self.assertIn("message", response.json())
        self.assertFalse(Experience.objects.filter(title="New Role").exists())

    def test_owner_creates_experience(self):
        self.login_as(self.owner)
        response = self.client.post(self.ajax_create_url, EXPERIENCE_FORM)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Experience.objects.filter(pk=response.json()["pk"]).exists())

    def test_invalid_input_returns_400(self):
        self.login_as(self.owner)
        response = self.client.post(self.ajax_create_url, dict(EXPERIENCE_FORM, title="   "))
        self.assertEqual(response.status_code, 400)
        self.assertIn("title", response.json()["errors"])

    def test_end_date_before_start_date_rejected(self):
        self.login_as(self.owner)
        data = dict(EXPERIENCE_FORM, ended_at="2025-01-01T00:00")
        response = self.client.post(self.ajax_create_url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("ended_at", response.json()["errors"])

    def test_xss_payload_rejected(self):
        self.login_as(self.owner)
        payload = '<img src="x" onerror="alert(\'XSS!\')">'
        response = self.client.post(self.ajax_create_url, dict(EXPERIENCE_FORM, title=payload))
        self.assertEqual(response.status_code, 400)
        self.assertIn("title", response.json()["errors"])
        self.assertFalse(Experience.objects.filter(description="Doing something new.").exists())

    def test_html_tags_are_stripped(self):
        self.login_as(self.owner)
        data = dict(EXPERIENCE_FORM, title="<b>Bold</b> Role", description="Hello <i>world</i>")
        response = self.client.post(self.ajax_create_url, data)
        self.assertEqual(response.status_code, 201)
        saved = Experience.objects.get(pk=response.json()["pk"])
        self.assertEqual(saved.title, "Bold Role")
        self.assertEqual(saved.description, "Hello world")
    
class StarTest(BaseTest):
    def test_toggle_star_experience(self):
        self.login_as(self.regular)
        self.client.post(self.star_url)
        self.assertEqual(self.experience.starred_by.count(), 1)
        self.client.post(self.star_url)  # klik lagi = unstar
        self.assertEqual(self.experience.starred_by.count(), 0)

    def test_one_star_per_user(self):
        self.login_as(self.regular)
        self.client.post(self.star_url)
        self.login_as(self.editor)
        self.client.post(self.star_url)
        self.assertEqual(self.experience.starred_by.count(), 2)

    def test_get_does_not_toggle_star(self):
        self.login_as(self.regular)
        self.client.get(self.star_url)
        self.assertEqual(self.experience.starred_by.count(), 0)

    def test_toggle_star_interest(self):
        url = reverse("main:toggle_star_interest", args=[self.interest.id])
        self.login_as(self.regular)
        self.client.post(url)
        self.assertEqual(self.interest.starred_by.count(), 1)
        self.client.post(url)
        self.assertEqual(self.interest.starred_by.count(), 0)


class InterestTest(BaseTest):
    def test_interest_page_is_public(self):
        response = self.client.get(reverse("main:show_interest"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "interest.html")

    def test_interest_data_loaded_via_json(self):
        response = self.client.get(reverse("main:get_interest_json"))
        self.assertContains(response, self.interest.name)

    def test_empty_interest_json(self):
        Interest.objects.all().delete()
        response = self.client.get(reverse("main:get_interest_json"))
        self.assertEqual(response.json(), [])

    def test_create_delete_interest_permissions(self):
        create_url = reverse("main:create_interest")
        delete_url = reverse("main:delete_interest", args=[self.interest.id])
        data = {"name": "Reading", "category": "exploring", "description": ""}

        response = self.client.post(create_url, data)  # anonim
        self.assertTrue(response.url.startswith("/login/"))

        self.login_as(self.editor)  # editor tidak boleh create/delete interest
        self.assertEqual(self.client.post(create_url, data).status_code, 403)
        self.assertEqual(self.client.post(delete_url).status_code, 403)

        self.login_as(self.owner)
        self.assertEqual(self.client.post(create_url, data).status_code, 302)
        self.assertTrue(Interest.objects.filter(name="Reading").exists())
        self.assertEqual(self.client.post(delete_url).status_code, 302)
        self.assertFalse(Interest.objects.filter(id=self.interest.id).exists())


class JsonApiTest(BaseTest):
    def test_experience_json_content(self):
        response = self.client.get(reverse("main:get_experience_json"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        fields = response.json()[0]["fields"]
        self.assertEqual(fields["title"], self.experience.title)
        self.assertTrue(fields["is_ongoing"])
        self.assertEqual(fields["ended_label"], "Present")

    def test_completed_experience_json(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        fields = self.client.get(reverse("main:get_experience_json")).json()[0]["fields"]
        self.assertFalse(fields["is_ongoing"])
        self.assertNotEqual(fields["ended_label"], "Present")

    def test_empty_experience_json(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:get_experience_json"))
        self.assertEqual(response.json(), [])

    def test_experience_json_star_fields(self):
        self.experience.starred_by.add(self.regular)
        url = reverse("main:get_experience_json")

        fields = self.client.get(url).json()[0]["fields"]  # anonim
        self.assertEqual(fields["star_count"], 1)
        self.assertFalse(fields["is_starred"])

        self.login_as(self.regular)
        fields = self.client.get(url).json()[0]["fields"]
        self.assertTrue(fields["is_starred"])

        self.login_as(self.editor)
        fields = self.client.get(url).json()[0]["fields"]
        self.assertFalse(fields["is_starred"])

    def test_experience_json_search(self):
        Experience.objects.create(
            title="Zebra Internship",
            description="Stripes.",
            started_at=timezone.now(),
        )
        url = reverse("main:get_experience_json")
        results = self.client.get(url, {"title": "zebra"}).json()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["fields"]["title"], "Zebra Internship")
        self.assertEqual(self.client.get(url, {"title": "tidak-ada"}).json(), [])

    def test_interest_json_star_fields(self):
        self.interest.starred_by.add(self.regular)
        url = reverse("main:get_interest_json")

        response = self.client.get(url)  # anonim
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        fields = response.json()[0]["fields"]
        self.assertEqual(fields["star_count"], 1)
        self.assertFalse(fields["is_starred"])

        self.login_as(self.regular)
        fields = self.client.get(url).json()[0]["fields"]
        self.assertTrue(fields["is_starred"])