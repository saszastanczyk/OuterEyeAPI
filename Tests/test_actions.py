import requests
import uuid

BASE_URL = "http://localhost:8088"
HEADERS = {"X-Username": "Steve", "Content-Type": "application/json"}

# Тестовые данные
POSITION = {
    "pos_x": 100,
    "pos_y": 64,
    "pos_z": 200
}

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
    "kill_name": "Zombie Steve",
    "kill_tool": "DIAMOND_SWORD"
}

BREED_DATA = {
    "position": POSITION,
    "father_subject_id": str(uuid.uuid4()),
    "mother_subject_id": str(uuid.uuid4()),
    "child_subject_id": str(uuid.uuid4()),
    "child_type": "COW"
}

DEATH_DATA = {
    "position": POSITION,
    "death_cause": "Fell from a high place"
}

PRAY_DATA = {
    "position": POSITION,
    "pray_text": "О Аллах, я очень хочу насвая, дай мне насвай, я убит горем после того, как потрахал барана и прыгнул со скалы. Я даже разбился насмерть и воскрес. Сжалься надо мной. Сам имам Коляка, которого все мусульмане почитают как святого сказал, что я глубоко несчастен."
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


class TestCraftAction:
    def test_add_craft_success(self):
        response = requests.post(
            f"{BASE_URL}/action/craft",
            json=CRAFT_DATA,
            headers=HEADERS
        )
        assert response.status_code == 200
        assert response.json() == {"status": "created"}


class TestKillAction:
    def test_add_kill_success(self):
        response = requests.post(
            f"{BASE_URL}/action/kill",
            json=KILL_DATA,
            headers=HEADERS
        )
        assert response.status_code == 200
        assert response.json() == {"status": "created"}


class TestBreedAction:
    def test_add_breed_success(self):
        response = requests.post(
            f"{BASE_URL}/action/breed",
            json=BREED_DATA,
            headers=HEADERS
        )
        assert response.status_code == 200
        assert response.json() == {"status": "created"}


class TestDeathAction:
    def test_add_death_success(self):
        response = requests.post(
            f"{BASE_URL}/action/death",
            json=DEATH_DATA,
            headers=HEADERS
        )
        assert response.status_code == 200
        assert response.json() == {"status": "created"}


class TestPrayAction:
    def test_add_pray_success(self):
        response = requests.post(
            f"{BASE_URL}/action/pray",
            json=PRAY_DATA,
            headers=HEADERS
        )
        assert response.status_code == 200
        assert response.json() == {"status": "created"}