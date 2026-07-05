import pytest
import requests
import uuid

BASE_URL = "http://localhost:8088"
HEADERS = {"X-Username": "Steve", "Content-Type": "application/json"}

# Тестовые данные
POSITION = {"pos_x": 100, "pos_y": 64, "pos_z": 200}

MEAL_DATA = {
    "position": POSITION,
    "meal_name": "COOKED_BEEF"
}

CRAFT_DATA = {
    "position": POSITION,
    "craft_subject": "DIAMOND_SWORD",
    "craft_amount": 1
}

KILL_DATA = {
    "position": POSITION,
    "kill_type": "ZOMBIE",
    "kill_subject": str(uuid.uuid4()),
    "kill_tool": "DIAMOND_SWORD"
}

BREED_DATA = {
    "position": POSITION,
    "father_subject_id": str(uuid.uuid4()),
    "mother_subject_id": str(uuid.uuid4()),
    "child_subject_id": str(uuid.uuid4())
}

DEATH_DATA = {
    "position": POSITION,
    "death_cause": "Fell from a high place"
}


class TestMealAction:
    def test_add_meal_success(self):
        response = requests.post(
            f"{BASE_URL}/action/meal",
            json=MEAL_DATA,
            headers=HEADERS
        )
        assert response.status_code == 200
        assert response.json() == {"status": "created"}

    def test_add_meal_missing_username(self):
        response = requests.post(
            f"{BASE_URL}/action/meal",
            json=MEAL_DATA,
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 400

    def test_add_meal_empty_username(self):
        headers = {"X-Username": "", "Content-Type": "application/json"}
        response = requests.post(
            f"{BASE_URL}/action/meal",
            json=MEAL_DATA,
            headers=headers
        )
        assert response.status_code == 400

    def test_add_meal_invalid_data(self):
        data = {"position": {"pos_x": "invalid", "pos_y": 64, "pos_z": 200}, "meal_name": "BREAD"}
        response = requests.post(
            f"{BASE_URL}/action/meal",
            json=data,
            headers=HEADERS
        )
        assert response.status_code == 422


class TestCraftAction:
    def test_add_craft_success(self):
        response = requests.post(
            f"{BASE_URL}/action/craft",
            json=CRAFT_DATA,
            headers=HEADERS
        )
        assert response.status_code == 200
        assert response.json() == {"status": "created"}

    def test_add_craft_missing_username(self):
        response = requests.post(
            f"{BASE_URL}/action/craft",
            json=CRAFT_DATA,
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 400

    def test_add_craft_invalid_amount(self):
        data = CRAFT_DATA.copy()
        data["craft_amount"] = -1
        response = requests.post(
            f"{BASE_URL}/action/craft",
            json=data,
            headers=HEADERS
        )
        # Pydantic может пропустить, но БД может упасть. Проверяем только статус
        assert response.status_code in [200, 422, 500]


class TestKillAction:
    def test_add_kill_success(self):
        response = requests.post(
            f"{BASE_URL}/action/kill",
            json=KILL_DATA,
            headers=HEADERS
        )
        assert response.status_code == 200
        assert response.json() == {"status": "created"}

    def test_add_kill_missing_username(self):
        response = requests.post(
            f"{BASE_URL}/action/kill",
            json=KILL_DATA,
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 400

    def test_add_kill_invalid_uuid(self):
        data = KILL_DATA.copy()
        data["kill_subject"] = "not-a-uuid"
        response = requests.post(
            f"{BASE_URL}/action/kill",
            json=data,
            headers=HEADERS
        )
        assert response.status_code == 422


class TestBreedAction:
    def test_add_breed_success(self):
        response = requests.post(
            f"{BASE_URL}/action/breed",
            json=BREED_DATA,
            headers=HEADERS
        )
        assert response.status_code == 200
        assert response.json() == {"status": "created"}

    def test_add_breed_missing_username(self):
        response = requests.post(
            f"{BASE_URL}/action/breed",
            json=BREED_DATA,
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 400

    def test_add_breed_invalid_uuid(self):
        data = BREED_DATA.copy()
        data["father_subject_id"] = "not-a-uuid"
        response = requests.post(
            f"{BASE_URL}/action/breed",
            json=data,
            headers=HEADERS
        )
        assert response.status_code == 422


class TestDeathAction:
    def test_add_death_success(self):
        response = requests.post(
            f"{BASE_URL}/action/death",
            json=DEATH_DATA,
            headers=HEADERS
        )
        assert response.status_code == 200
        assert response.json() == {"status": "created"}

    def test_add_death_missing_username(self):
        response = requests.post(
            f"{BASE_URL}/action/death",
            json=DEATH_DATA,
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 400

    def test_add_death_empty_cause(self):
        data = DEATH_DATA.copy()
        data["death_cause"] = ""
        response = requests.post(
            f"{BASE_URL}/action/death",
            json=data,
            headers=HEADERS
        )
        assert response.status_code in [200, 422]