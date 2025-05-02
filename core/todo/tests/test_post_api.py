import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth.models import User


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def common_user():
    user = User.objects.create_user(
        username="testuser",
        password="Ali_08582255",
    )
    return user


@pytest.mark.django_db
class TestTodoApi:
    def test_get_todo_response_annonymouse_401_status(self, api_client):
        url = reverse("todo:api:task-list")
        response = api_client.get(url)
        assert response.status_code == 401

    def test_get_todo_response_authorized_200_status(self, api_client, common_user):
        api_client.force_login(user=common_user)
        url = reverse("todo:api:task-list")
        response = api_client.get(url)
        assert response.status_code == 200

    def test_create_todo_respoonse_annonymouse_401_status(self, api_client):
        url = reverse("todo:api:task-list")
        data = {
            "title": "Test Todo",
            "complete": False,
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == 401

    def test_create_todo_response_authorized_201_status(self, api_client, common_user):
        url = reverse("todo:api:task-list")
        data = {
            "title": "Test Todo",
            "complete": False,
        }
        api_client.force_login(user=common_user)
        response = api_client.post(url, data, format="json")
        assert response.status_code == 201
        assert response.data["title"] == "Test Todo"

    def test_create_todo_invalid_data_response_400_status(
        self, api_client, common_user
    ):
        url = reverse("todo:api:task-list")
        data = {
            "title": "",
            "complete": False,
        }
        api_client.force_login(user=common_user)
        response = api_client.post(url, data, format="json")
        assert response.status_code == 400
        assert "title" in response.data

    def test_put_todo_response_authorized_200_status(self, api_client, common_user):
        url = reverse("todo:api:task-list")
        data = {
            "title": "Test Todo",
            "completed": False,
        }
        api_client.force_login(user=common_user)
        response = api_client.post(url, data, format="json")
        todo_id = response.data["id"]
        url = reverse("todo:api:task-detail", args=[todo_id])
        data = {
            "title": "Updated Todo",
            "complete": True,
        }
        response = api_client.put(url, data, format="json")
        assert response.status_code == 200
        assert response.data["title"] == "Updated Todo"

    def test_patch_todo_response_authorized_200_status(self, api_client, common_user):
        url = reverse("todo:api:task-list")
        data = {
            "title": "Test Todo",
            "complete": False,
        }
        api_client.force_login(user=common_user)
        response = api_client.post(url, data, format="json")
        todo_id = response.data["id"]
        url = reverse("todo:api:task-detail", args=[todo_id])
        data = {
            "complete": True,
        }
        response = api_client.patch(url, data, format="json")
        assert response.status_code == 200
        assert response.data["complete"] is True

    def test_put_todo_invalid_data_response_400_status(self, api_client, common_user):
        url = reverse("todo:api:task-list")
        data = {
            "title": "Test Todo",
            "complete": False,
        }
        api_client.force_login(user=common_user)
        response = api_client.post(url, data, format="json")
        todo_id = response.data["id"]
        url = reverse("todo:api:task-detail", args=[todo_id])
        data = {
            "title": "",
            "complete": True,
        }
        response = api_client.put(url, data, format="json")
        assert response.status_code == 400
        assert "title" in response.data

    def test_patch_todo_invalid_data_response_400_status(self, api_client, common_user):
        url = reverse("todo:api:task-list")
        data = {
            "title": "Test Todo",
            "complete": False,
        }
        api_client.force_login(user=common_user)
        response = api_client.post(url, data, format="json")
        todo_id = response.data["id"]
        url = reverse("todo:api:task-detail", args=[todo_id])
        data = {
            "complete": True,
            "title": "",
        }
        response = api_client.patch(url, data, format="json")
        assert response.status_code == 400
        assert "title" in response.data

    def test_delete_todo_response_authorized_204_status(self, api_client, common_user):
        url = reverse("todo:api:task-list")
        data = {
            "title": "Test Todo",
            "complete": False,
        }
        api_client.force_login(user=common_user)
        response = api_client.post(url, data, format="json")
        todo_id = response.data["id"]
        url = reverse("todo:api:task-detail", args=[todo_id])
        response = api_client.delete(url)
        assert response.status_code == 204
