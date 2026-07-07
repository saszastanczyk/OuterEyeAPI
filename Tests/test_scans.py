import requests

BASE_URL = "http://localhost:8088"
HEADERS = {"X-Username": "Steve", "Content-Type": "application/json"}

# Тестовые данные
POSITION_SCAN = {
    "pos_x": 100,
    "pos_y": 64,
    "pos_z": 200
}

INVENTORY_SCAN = {
    "items": [
        {"name": "NETHERITE_PICKAXE", "amount": 1},
        {"name": "NETHERITE_SWORD", "amount": 1},
        {"name": "NETHERITE_AXE", "amount": 1},
        {"name": "NETHERITE_SHOVEL", "amount": 1},
        {"name": "IRON_PICKAXE", "amount": 1},
        {"name": "IRON_SWORD", "amount": 1},
        {"name": "IRON_AXE", "amount": 1},
        {"name": "IRON_SHOVEL", "amount": 1},
        {"name": "COOKED_BEEF", "amount": 32},
        {"name": "BREAD", "amount": 16},
        {"name": "GOLDEN_APPLE", "amount": 3},
        {"name": "COAL", "amount": 64},
        {"name": "IRON_INGOT", "amount": 48},
        {"name": "DIAMOND", "amount": 12},
        {"name": "EMERALD", "amount": 5},
        {"name": "OBSIDIAN", "amount": 16},
        {"name": "REDSTONE_DUST", "amount": 64},
        {"name": "TORCH", "amount": 32},
        {"name": "WATER_BUCKET", "amount": 1},
        {"name": "BUCKET", "amount": 1},
        {"name": "COBBLESTONE", "amount": 128},
        {"name": "DEEPSLATE", "amount": 64},
        {"name": "RAW_IRON", "amount": 24},
        {"name": "RAW_GOLD", "amount": 8},
        {"name": "ENDER_PEARL", "amount": 4},
        {"name": "BLAZE_POWDER", "amount": 6},
        {"name": "SHIELD", "amount": 1}
    ]
}

MINIMAL_INVENTORY_SCAN = {
    "items": [
        {"name": "NETHERITE_PICKAXE", "amount": 1},
        {"name": "DIAMOND", "amount": 10},
        {"name": "COOKED_BEEF", "amount": 32}
    ]
}


class TestPositionScan:
    def test_add_position_scan_success(self):
        response = requests.post(
            f"{BASE_URL}/scan/position",
            json=POSITION_SCAN,
            headers=HEADERS
        )
        assert response.status_code == 200
        assert response.json() == {"status": "created"}


class TestInventoryScan:
    def test_add_inventory_scan_success_full(self):
        response = requests.post(
            f"{BASE_URL}/scan/inventory",
            json=INVENTORY_SCAN,
            headers=HEADERS
        )
        assert response.status_code == 200
        assert response.json() == {"status": "created"}

    def test_add_inventory_scan_success_minimal(self):
        response = requests.post(
            f"{BASE_URL}/scan/inventory",
            json=MINIMAL_INVENTORY_SCAN,
            headers=HEADERS
        )
        assert response.status_code == 200
        assert response.json() == {"status": "created"}

    def test_add_inventory_scan_success_single_item(self):
        data = {"items": [{"name": "NETHERITE_PICKAXE", "amount": 1}]}
        response = requests.post(
            f"{BASE_URL}/scan/inventory",
            json=data,
            headers=HEADERS
        )
        assert response.status_code == 200
        assert response.json() == {"status": "created"}

    def test_add_inventory_scan_success_empty(self):
        data = {"items": []}
        response = requests.post(
            f"{BASE_URL}/scan/inventory",
            json=data,
            headers=HEADERS
        )
        assert response.status_code == 200
        assert response.json() == {"status": "created"}