import json

import requests
import uuid

BASE_URL = "http://localhost:8088"
HEADERS = {"X-Username": "AllahPrimarchOfChaos", "Content-Type": "application/json"}

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
    "pray_text": "Мы уже высалидились на одну из планет Ультрамар и начали уничтожать всех кого видим, особенно фанатичных ультрамаринов и преверженцев ничтожному Империуму. Более того на планету также наподают некросы, но мы не будем им противиться. Мы соберем всех овец и свиней и отправимся на другую планету подальше отсюда. Аллаху Акбар"
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
        response = requests.get(
            f"{BASE_URL}/action/pray",
            json=PRAY_DATA,
            headers=HEADERS
        )

        # Выводим результат в консоль
        print("\n" + "=" * 50)
        print("📿 РЕЗУЛЬТАТ МОЛИТВЫ")
        print("=" * 50)
        print(f"📤 Отправлено: {json.dumps(PRAY_DATA, ensure_ascii=False, indent=2)}")
        print(f"📥 Статус: {response.status_code}")

        if response.status_code == 200:
            response_data = response.json()
            pray_response = response_data.get("pray_respond")
            print(f"🙏 Ответ божества:\n{pray_response}")
        else:
            print(f"❌ Ошибка: {response.text}")
        print("=" * 50 + "\n")

        # Ассерты
        assert response.status_code == 200
        assert "pray_respond" in response.json()
        assert len(response.json()["pray_respond"]) > 0