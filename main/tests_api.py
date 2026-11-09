import uuid

from django.contrib.auth.models import Group, User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Interest, Experience


class InterestAPITest(APITestCase):

    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner",
            password="test-password",
            email="owner@example.com",
        )

        self.visitor = User.objects.create_user(
            username="visitor",
            password="test-password",
        )

        self.editor = User.objects.create_user(
            username="editor",
            password="test-password",
        )

        self.editor.groups.add(
            Group.objects.create(name="Editor")
        )

        self.interest = Interest.objects.create(
            name="Gaming",
            category="fun",
            description="I play games whenever I have the time.",
        )

        self.list_url = reverse("api:interest-list")

        self.detail_url = reverse(
            "api:interest-detail",
            args=[self.interest.id],
        )

        self.star_url = reverse(
            "api:interest-star",
            args=[self.interest.id],
        )

        self.payload = {
            "name": "Reading",
            "category": "exploring",
            "description": "Reading books in my free time.",
        }


    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data[0]["id"],
            self.interest.id,
        )

        self.assertFalse(response.data[0]["is_starred"])

        self.assertNotIn("fields", response.data[0])

        detail_response = self.client.get(self.detail_url)

        self.assertEqual(
            detail_response.status_code,
            status.HTTP_200_OK,
        )


    def test_search_and_empty_results(self):
        response = self.client.get(
            self.list_url,
            {"name": "GAMING"},
        )

        self.assertEqual(len(response.data), 1)

        response = self.client.get(
            self.list_url,
            {"name": "not-found"},
        )

        self.assertEqual(response.data, [])


    def test_missing_interest(self):
        url = reverse(
            "api:interest-detail",
            args=[999999999],
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )


    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)

            response = self.client.post(
                self.list_url,
                self.payload,
                format="json",
            )

            self.assertEqual(
                response.status_code,
                status.HTTP_403_FORBIDDEN,
            )

            response = self.client.patch(
                self.detail_url,
                {"name": "Changed"},
                format="json",
            )

            self.assertEqual(
                response.status_code,
                status.HTTP_403_FORBIDDEN,
            )

            response = self.client.delete(self.detail_url)

            self.assertEqual(
                response.status_code,
                status.HTTP_403_FORBIDDEN,
            )

        self.assertEqual(Interest.objects.count(), 1)


    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            Interest.objects.filter(
                pk=response.data["id"]
            ).exists()
        )


    def test_validation(self):
        self.client.force_authenticate(user=self.owner)

        invalid_payloads = [
            {"name": "   "},
            {"name": '<img src="x" onerror="alert(1)">'},
            {"category": "invalid-category"},
        ]

        for changes in invalid_payloads:
            response = self.client.post(
                self.list_url,
                {**self.payload, **changes},
                format="json",
            )

            self.assertEqual(
                response.status_code,
                status.HTTP_400_BAD_REQUEST,
            )

        self.assertEqual(Interest.objects.count(), 1)


    def test_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.patch(
            self.detail_url,
            {"name": "Updated Gaming"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.interest.refresh_from_db()

        self.assertEqual(
            self.interest.description,
            "I play games whenever I have the time.",
        )

        response = self.client.put(
            self.detail_url,
            {"name": "Incomplete"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        response = self.client.put(
            self.detail_url,
            {
                "name": "Updated Interest",
                "category": "fun",
                "description": "Updated description.",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        response = self.client.delete(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertEqual(response.content, b"")

        self.assertFalse(
            Interest.objects.filter(
                pk=self.interest.id
            ).exists()
        )


    def test_star_requires_login_and_toggles(self):
        response = self.client.post(self.star_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.client.force_authenticate(user=self.visitor)

        response = self.client.post(self.star_url)

        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)

        response = self.client.post(self.star_url)

        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)


    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.post(
            self.list_url,
            {
                **self.payload,
                "star_count": 99,
                "is_starred": True,
                "starred_by_names": "forged",
                "starred_by": [self.visitor.id],
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])


    def test_editor_can_update_but_cannot_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)

        response = self.client.patch(
            self.detail_url,
            {"name": "Editor Updated"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        response = self.client.delete(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )


    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.delete(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )


    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)

        self.assertTrue(
            client.login(
                username="owner",
                password="test-password",
            )
        )

        response = client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.assertEqual(Interest.objects.count(), 1)


    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)

        client.login(
            username="owner",
            password="test-password",
        )

        page = client.get(
            self.list_url,
            HTTP_ACCEPT="text/html",
        )

        self.assertEqual(
            page.status_code,
            status.HTTP_200_OK,
        )

        token = client.cookies["csrftoken"].value

        response = client.post(
            self.list_url,
            self.payload,
            format="json",
            HTTP_X_CSRFTOKEN=token,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

class ExperienceAPITest(APITestCase):

    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner",
            password="test-password",
            email="owner@example.com",
        )

        self.visitor = User.objects.create_user(
            username="visitor",
            password="test-password",
        )

        self.editor = User.objects.create_user(
            username="editor",
            password="test-password",
        )

        self.editor.groups.add(
            Group.objects.create(name="Editor")
        )

        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            started_at="2026-01-01T00:00:00Z",
        )

        self.list_url = reverse("api:experience-list")

        self.detail_url = reverse(
            "api:experience-detail",
            args=[self.experience.id],
        )

        self.star_url = reverse(
            "api:experience-star",
            args=[self.experience.id],
        )

        self.payload = {
            "title": "New Experience",
            "description": "Learning something new.",
            "thumbnail": None,
            "started_at": "2026-02-01T00:00:00Z",
            "ended_at": None,
        }

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data[0]["id"],
            str(self.experience.id),
        )

        self.assertEqual(
            response.data[0]["title"],
            "Asisten Dosen PBP",
        )

        self.assertFalse(response.data[0]["is_starred"])
        self.assertEqual(response.data[0]["star_count"], 0)

        detail_response = self.client.get(self.detail_url)

        self.assertEqual(
            detail_response.status_code,
            status.HTTP_200_OK,
        )

    def test_search_and_empty_results(self):
        response = self.client.get(
            self.list_url,
            {"title": "ASISTEN"},
        )

        self.assertEqual(len(response.data), 1)

        response = self.client.get(
            self.list_url,
            {"title": "not-found"},
        )

        self.assertEqual(response.data, [])

    def test_missing_experience(self):
        url = reverse(
            "api:experience-detail",
            args=[uuid.uuid4()],
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)

            response = self.client.post(
                self.list_url,
                self.payload,
                format="json",
            )

            self.assertEqual(
                response.status_code,
                status.HTTP_403_FORBIDDEN,
            )

            response = self.client.patch(
                self.detail_url,
                {"title": "Changed"},
                format="json",
            )

            self.assertEqual(
                response.status_code,
                status.HTTP_403_FORBIDDEN,
            )

            response = self.client.delete(self.detail_url)

            self.assertEqual(
                response.status_code,
                status.HTTP_403_FORBIDDEN,
            )

        self.experience.refresh_from_db()

        self.assertEqual(
            self.experience.title,
            "Asisten Dosen PBP",
        )

        self.assertEqual(Experience.objects.count(), 1)

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            Experience.objects.filter(
                pk=response.data["id"]
            ).exists()
        )

    def test_editor_can_update_but_cannot_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)

        response = self.client.patch(
            self.detail_url,
            {"title": "Editor Updated"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.experience.refresh_from_db()

        self.assertEqual(
            self.experience.title,
            "Editor Updated",
        )

        response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        response = self.client.delete(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.assertTrue(
            Experience.objects.filter(
                pk=self.experience.id
            ).exists()
        )

    def test_owner_can_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.patch(
            self.detail_url,
            {"title": "Updated Experience"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.experience.refresh_from_db()

        self.assertEqual(
            self.experience.title,
            "Updated Experience",
        )

        response = self.client.put(
            self.detail_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        response = self.client.delete(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Experience.objects.filter(
                pk=self.experience.id
            ).exists()
        )

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)

        invalid_payloads = [
            {"title": "   "},
            {"title": '<img src="x" onerror="alert(1)">'},
            {"description": "   "},
            {"description": "<script></script>"},
        ]

        for changes in invalid_payloads:
            response = self.client.post(
                self.list_url,
                {**self.payload, **changes},
                format="json",
            )

            self.assertEqual(
                response.status_code,
                status.HTTP_400_BAD_REQUEST,
            )

        self.assertEqual(Experience.objects.count(), 1)

    def test_html_tags_are_stripped(self):
        self.client.force_authenticate(user=self.owner)

        payload = {
            **self.payload,
            "title": "<b>Bold</b> Experience",
            "description": "Hello <i>world</i>",
        }

        response = self.client.post(
            self.list_url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        saved = Experience.objects.get(
            pk=response.data["id"]
        )

        self.assertEqual(saved.title, "Bold Experience")
        self.assertEqual(saved.description, "Hello world")

    def test_end_date_before_start_date_rejected(self):
        self.client.force_authenticate(user=self.owner)

        payload = {
            **self.payload,
            "ended_at": "2025-01-01T00:00:00Z",
        }

        response = self.client.post(
            self.list_url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertIn("ended_at", response.data)

        self.assertEqual(Experience.objects.count(), 1)

    def test_star_requires_login_and_toggles(self):
        response = self.client.post(self.star_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.client.force_authenticate(user=self.visitor)

        response = self.client.post(self.star_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)

        response = self.client.post(self.star_url)

        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)

        payload = {
            **self.payload,
            "star_count": 99,
            "is_starred": True,
            "is_ongoing": False,
        }

        response = self.client.post(
            self.list_url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])
        self.assertTrue(response.data["is_ongoing"])

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)

        self.assertTrue(
            client.login(
                username="owner",
                password="test-password",
            )
        )

        response = client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.assertEqual(Experience.objects.count(), 1)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)

        self.assertTrue(
            client.login(
                username="owner",
                password="test-password",
            )
        )

        page = client.get(
            reverse("main:show_experience"),
        )

        self.assertEqual(
            page.status_code,
            status.HTTP_200_OK,
        )

        token = client.cookies["csrftoken"].value

        response = client.post(
            self.list_url,
            self.payload,
            format="json",
            HTTP_X_CSRFTOKEN=token,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )