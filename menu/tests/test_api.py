"""
Menu module API tests.
"""

import pytest
from django.urls import reverse
from rest_framework import status

MENUS_URL = reverse("menu:menus-list")


def get_menu_detail_url(menu_id):
    """Create and return an menu detail URL."""
    return reverse("menu:menus-detail", args=[menu_id])


def get_menu_dish_list_url(menu_id):
    """Create and return an menu dishes list URL."""
    return reverse("menu:menu-dishes-list", kwargs={"menu_pk": menu_id})


def get_dish_detail_url(dish_id):
    """Create and return an dish detail URL."""
    return reverse("menu:dishes-detail", args=[dish_id])


def get_dish_upload_image_url(dish_id):
    """Create and return an dish upload iamge URL."""
    return reverse("menu:dishes-upload-image", args=[dish_id])


@pytest.mark.django_db
class TestPublicMenuAPI:
    """Tests of public menu API's"""

    def test_cannot_create_menu(self, api_client):
        """Test of creating menu with unauthorized - error."""
        response = api_client.post(MENUS_URL, data={})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_cannot_update_menu(self, api_client, menu_factory):
        """Test of updating menu with unauthorized - error."""
        menu = menu_factory()

        response = api_client.post(get_menu_detail_url(menu.id), data={})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_cannot_delete_menu(self, api_client, menu_factory):
        """Test of deleting menu with unauthorized - error."""
        menu = menu_factory()

        response = api_client.delete(get_menu_detail_url(menu.id))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_cannot_list_empty_menus(self, api_client, menu_factory):
        """Test of retrieving empty menus."""
        menu_factory()

        response = api_client.get(MENUS_URL)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0

    def test_can_list_non_empty_menus(self, api_client, dish_factory):
        """Test of retrieving non empty menus."""
        dish = dish_factory()

        response = api_client.get(MENUS_URL)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

        response_menu_data = response.data[0]
        assert dish.menu.id == response_menu_data["id"]

    def test_cannot_retrive_empty_menu(self, api_client, menu_factory):
        """Test of retrieving empty menu - error."""
        menu = menu_factory()

        response = api_client.get(get_menu_detail_url(menu.id))

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_can_retrive_non_empty_menu(self, api_client, dish_factory):
        """Test of retrieving non-empty menu."""
        dish = dish_factory()

        response = api_client.get(get_menu_detail_url(dish.menu.id))

        assert response.status_code == status.HTTP_200_OK
        assert dish.menu.id == response.data["id"]


@pytest.mark.django_db
class TestPrivateMenuAPI:
    """Tests of private menu API's"""

    def test_can_list_empty_menus(self, api_auth_client, menu_factory):
        "Test of listing empty menus."
        auth_api_client = api_auth_client()
        menu = menu_factory()

        response = auth_api_client.get(MENUS_URL)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

        response_menu_data = response.data[0]
        assert menu.id == response_menu_data["id"]

    def test_can_list_non_empty_menus(self, api_auth_client, dish_factory):
        "Test of listing non empty menus."
        auth_api_client = api_auth_client()
        dish_factory()

        response = auth_api_client.get(MENUS_URL)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_can_create_menu(self, api_auth_client, menu_model):
        auth_api_client = api_auth_client()
        payload = {"name": "TestMenu1", "description": "TestMenu1Desc"}

        response = auth_api_client.post(MENUS_URL, data=payload)

        assert response.status_code == status.HTTP_201_CREATED

        menus = menu_model.objects.all()
        assert len(menus) == 1

        menu = menus.first()
        assert menu.name == payload["name"]
        assert menu.description == payload["description"]

    def test_can_update_menu(self, api_auth_client, menu_factory):
        "Test of updating menu."
        auth_api_client = api_auth_client()
        menu = menu_factory()

        payload = {"name": "UpdatedMenuName1"}

        response = auth_api_client.patch(get_menu_detail_url(menu.id), data=payload)
        menu.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert menu.id == response.data["id"]
        assert menu.name == payload["name"]

    def test_can_delete_menu(self, api_auth_client, menu_factory, menu_model):
        "Test of deleting menu."
        auth_api_client = api_auth_client()
        menu = menu_factory()

        response = auth_api_client.delete(get_menu_detail_url(menu.id))

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not menu_model.objects.filter(id=menu.id).first()


@pytest.mark.django_db
class TestPublicMenuDishAPI:
    """Tests of private menu dishes API's"""

    def test_cannot_create_menu_dish(self, api_client, menu_factory):
        """Test of creating menu dishes - error."""
        menu = menu_factory()

        response = api_client.post(get_menu_dish_list_url(menu.id), data={})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_cannot_retrive_empty_menu_dishes(self, api_client, menu_factory):
        """Test of retrieving empty menu dishes - error."""
        menu = menu_factory()

        response = api_client.get(get_menu_dish_list_url(menu.id))

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_can_retrive_non_empty_menu_dishes(self, api_client, dish_factory):
        """Test of retrieving non-empty menu dishes."""
        dish = dish_factory()

        response = api_client.get(get_menu_dish_list_url(dish.menu.id))

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

        response_menu_dish_data = response.data[0]
        assert dish.id == response_menu_dish_data["id"]


@pytest.mark.django_db
class TestPrivateMenuDishAPI:
    """Tests of private menu dishes API's"""

    def test_can_create_menu_dish(self, api_auth_client, menu_factory):
        """Test of creating menu dishes."""
        auth_api_client = api_auth_client()
        menu = menu_factory()
        payload = {
            "name": "TestDishName1",
            "description": "TestDishDescription1",
            "price": "20.55",
            "preparation_time": "00:00:30",
            "is_vegetarian": True,
        }

        response = auth_api_client.post(get_menu_dish_list_url(menu.id), data=payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == payload["name"]
        assert response.data["description"] == payload["description"]
        assert response.data["price"] == payload["price"]
        assert response.data["preparation_time"] == payload["preparation_time"]
        assert response.data["is_vegetarian"] == payload["is_vegetarian"]

    def test_can_retrive_empty_menu_dishes(self, api_auth_client, menu_factory):
        """Test of retrieving empty menu dishes."""
        auth_api_client = api_auth_client()
        menu = menu_factory()

        response = auth_api_client.get(get_menu_dish_list_url(menu.id))

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0

    def test_can_retrive_non_empty_menu_dishes(self, api_client, dish_factory):
        """Test of retrieving non-empty menu dishes."""
        dish = dish_factory()

        response = api_client.get(get_menu_dish_list_url(dish.menu.id))

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

        response_menu_dish_data = response.data[0]
        assert dish.id == response_menu_dish_data["id"]


@pytest.mark.django_db
class TestPublicDishAPI:
    """Tests of dish API's"""

    def test_cannot_retrieve_dish(self, api_client, dish_factory):
        """Test of retrieving dish - error."""
        dish = dish_factory()

        response = api_client.get(get_dish_detail_url(dish.id))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_cannot_update_dish(self, api_client, dish_factory):
        """Test of updating dish - error"""
        dish = dish_factory()

        response = api_client.patch(get_dish_detail_url(dish.id), data={})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_cannot_delete_dish(self, api_client, dish_factory):
        """Test of deleting dish - error"""
        dish = dish_factory()

        response = api_client.delete(get_dish_detail_url(dish.id))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_cannot_upload_dish_image(self, api_client, dish_factory):
        """Test of uploading dish iamge - error"""
        dish = dish_factory()

        response = api_client.post(get_dish_upload_image_url(dish.id))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestPrivateDishAPI:
    """Tests of dish API's"""

    def test_can_retrieve_dish(self, api_auth_client, dish_factory):
        """Test of retrieving dish."""
        auth_api_client = api_auth_client()
        dish = dish_factory()

        response = auth_api_client.get(get_dish_detail_url(dish.id))

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == dish.id

    def test_can_update_dish(self, api_auth_client, dish_factory):
        """Test of updating dish"""
        auth_api_client = api_auth_client()
        dish = dish_factory()
        payload = {"name": "NewTestDishName1"}

        response = auth_api_client.patch(get_dish_detail_url(dish.id), data=payload)
        dish.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == dish.id
        assert dish.name == payload["name"]

    def test_can_delete_dish(self, api_auth_client, dish_factory):
        """Test of deleting dish"""
        auth_api_client = api_auth_client()
        dish = dish_factory()

        response = auth_api_client.delete(get_dish_detail_url(dish.id))

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_can_upload_dish_image(
        self, api_auth_client, dish_factory, test_image_file
    ):
        """Test of uploading dish image"""
        auth_api_client = api_auth_client()
        dish = dish_factory()

        payload = {"image": test_image_file.file}
        response = auth_api_client.post(
            get_dish_upload_image_url(dish.id), data=payload, format="multipart"
        )

        assert response.status_code == status.HTTP_200_OK
        dish.refresh_from_db()
        dish.image.delete()

    def test_cannot_upload_dish_image(
        self, api_auth_client, dish_factory, test_image_file
    ):
        """Test of uploading dish iamge - error"""
        auth_api_client = api_auth_client()
        dish = dish_factory()

        payload = {"image": test_image_file.file}
        response = auth_api_client.post(
            get_dish_upload_image_url(dish.id), data=payload, format="multipart"
        )

        assert response.status_code == status.HTTP_200_OK
        dish.refresh_from_db()
        dish.image.delete()
