import requests

BASE_URL = "http://localhost:8088/action"
HEADERS = {"X-Username": "Steve", "Content-Type": "application/json"}

MEAL_DATA = {
    "position": {"pos_x": 100, "pos_y": 64, "pos_z": 200},
    "meal_name": "COOKED_BEEF"
}


class TestMealAction:
    def test_add_meal_success(self):
        response = requests.post(
            f"{BASE_URL}/meal",
            json=MEAL_DATA,
            headers=HEADERS
        )
        assert response.status_code == 200
        assert response.json() == {"status": "created"}

    def test_add_meal_missing_username(self):
        response = requests.post(
            f"{BASE_URL}/meal",
            json=MEAL_DATA,
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 400

    def test_add_meal_empty_username(self):
        headers = {"X-Username": "", "Content-Type": "application/json"}
        response = requests.post(
            f"{BASE_URL}/meal",
            json=MEAL_DATA,
            headers=headers
        )
        assert response.status_code == 400

    def test_add_meal_invalid_data(self):
        data = {"position": {"pos_x": "invalid", "pos_y": 64, "pos_z": 200}, "meal_name": "BREAD"}
        response = requests.post(
            f"{BASE_URL}/meal",
            json=data,
            headers=HEADERS
        )
        assert response.status_code == 422