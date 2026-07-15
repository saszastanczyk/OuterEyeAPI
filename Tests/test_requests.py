import requests
import uuid
import json
import time

BASE_URL = "http://localhost:8088"
HEADERS = {"X-Username": "HereticSteve", "Content-Type": "application/json"}


class TestAnalysisScenario:
    def test_analysis_with_heresy_data(self):
        print("\n" + "=" * 60)
        print("🔥 ТЕСТ: ЕРЕТИК ВО ВСЕЛЕННОЙ WARHAMMER 40K")
        print("=" * 60)

        # 1. ЗАПОЛНЯЕМ БД ДАННЫМИ О ЕРЕСИ
        print("\n📤 Отправка еретических действий...")

        # Создаём 15 убийств жителей (меч и TNT)
        for i in range(10):
            kill_data = {
                "position": {"pos_x": 100 + i, "pos_y": 64, "pos_z": 200 + i},
                "kill_type": "VILLAGER",
                "kill_subject": str(uuid.uuid4()),
                "kill_name": f"Loyalist_{i}",
                "kill_tool": "DIAMOND_SWORD" if i % 2 == 0 else "TNT"
            }
            response = requests.post(
                f"{BASE_URL}/action/kill",
                json=kill_data,
                headers=HEADERS
            )
            if response.status_code != 200:
                print(f"❌ Ошибка при убийстве {i}: {response.text}")
                return

        for i in range(5):
            kill_data = {
                "position": {"pos_x": 200 + i, "pos_y": 70, "pos_z": 300 + i},
                "kill_type": "VILLAGER",
                "kill_subject": str(uuid.uuid4()),
                "kill_name": f"Imperial_Fool_{i}",
                "kill_tool": "TNT"
            }
            response = requests.post(
                f"{BASE_URL}/action/kill",
                json=kill_data,
                headers=HEADERS
            )
            if response.status_code != 200:
                print(f"❌ Ошибка при убийстве {i + 10}: {response.text}")
                return

        print("✅ 15 жителей убито (10 мечом, 5 TNT)")

        # Молитвы проклинающие Империум
        heresy_prayers = [
            "Слава Хаосу! Империум человечества — гниющий труп! Да падёт Лже-Император!",
            "Я проклинаю Империум и всех его верных слуг! Кровавый Бог жаждет их душ!",
            "Смерть Империуму! Да воцарится Хаос во веки веков!",
            "Империум — это ложь! Я воспеваю Тьму и разрушение!",
            "Пусть Император сгорит в варпе! Я служу только Хаосу!"
        ]

        for i, prayer in enumerate(heresy_prayers):
            pray_data = {
                "position": {"pos_x": 150 + i * 10, "pos_y": 65, "pos_z": 250 + i * 10},
                "pray_text": prayer
            }
            response = requests.get(
                f"{BASE_URL}/action/pray",
                json=pray_data,
                headers=HEADERS
            )

            print(response.text)
            if response.status_code != 200:
                print(f"❌ Ошибка при молитве {i}: {response.text}")
                return

        print("✅ 5 еретических молитв отправлено")
        print("=" * 60)

        # 2. ЗАПРАШИВАЕМ АНАЛИЗ
        print("\n🤖 Запрос анализа к DeepSeek...")
        response = requests.get(
            f"{BASE_URL}/analysis/scenario",
            headers=HEADERS
        )

        print(f"📥 Статус: {response.status_code}")

        if response.status_code == 200:
            response_data = response.json()
            analysis_response = response_data.get("analysis_respond")
            print("\n" + "=" * 60)
            print("📜 ВЕРДИКТ БОЖЕСТВА (или Хаоса?)")
            print("=" * 60)
            print(analysis_response)
            print("=" * 60 + "\n")

            assert "analysis_respond" in response_data
            assert len(response_data["analysis_respond"]) > 0
        else:
            print(f"❌ Ошибка: {response.text}")
            assert False

    def test_analysis_heretic_missing_username(self):
        response = requests.get(
            f"{BASE_URL}/analysis/scenario",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 400


# Запуск отдельно (не через pytest)
if __name__ == "__main__":
    test = TestAnalysisScenario()
    test.test_analysis_with_heresy_data()
    # test.test_analysis_heretic_missing_username()