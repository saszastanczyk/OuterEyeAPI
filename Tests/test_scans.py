import pytest
import requests
from typing import Dict, Any

BASE_URL = "http://localhost:8088"
HEADERS = {"X-Username": "Steve", "Content-Type": "application/json"}

POSITION_SCAN = {"pos_x": 0, "pos_y": 64, "pos_z": 0}

INVENTORY_SCAN = {
    "items": [
        {"item_name": "NETHERITE_PICKAXE", "item_amount": 1},
        {"item_name": "NETHERITE_SWORD", "item_amount": 1},
        {"item_name": "NETHERITE_AXE", "item_amount": 1},
        {"item_name": "NETHERITE_SHOVEL", "item_amount": 1},
        {"item_name": "IRON_PICKAXE", "item_amount": 1},
        {"item_name": "IRON_SWORD", "item_amount": 1},
        {"item_name": "IRON_AXE", "item_amount": 1},
        {"item_name": "IRON_SHOVEL", "item_amount": 1},
        {"item_name": "COOKED_BEEF", "item_amount": 32},
        {"item_name": "BREAD", "item_amount": 16},
        {"item_name": "GOLDEN_APPLE", "item_amount": 3},
        {"item_name": "COAL", "item_amount": 64},
        {"item_name": "IRON_INGOT", "item_amount": 48},
        {"item_name": "DIAMOND", "item_amount": 12},
        {"item_name": "EMERALD", "item_amount": 5},
        {"item_name": "OBSIDIAN", "item_amount": 16},
        {"item_name": "REDSTONE_DUST", "item_amount": 64},
        {"item_name": "TORCH", "item_amount": 32},
        {"item_name": "WATER_BUCKET", "item_amount": 1},
        {"item_name": "BUCKET", "item_amount": 1},
        {"item_name": "COBBLESTONE", "item_amount": 128},
        {"item_name": "DEEPSLATE", "item_amount": 64},
        {"item_name": "RAW_IRON", "item_amount": 24},
        {"item_name": "RAW_GOLD", "item_amount": 8},
        {"item_name": "ENDER_PEARL", "item_amount": 4},
        {"item_name": "BLAZE_POWDER", "item_amount": 6},
        {"item_name": "SHIELD", "item_amount": 1}
    ]
}

MINIMAL_INVENTORY_SCAN = {
    "items": [
        {"item_name": "NETHERITE_PICKAXE", "item_amount": 1},
        {"item_name": "DIAMOND", "item_amount": 10},
        {"item_name": "COOKED_BEEF", "item_amount": 32}
    ]
}


class TestPositionScan:
    def test_success(self):
        response = requests.post(
            f"{BASE_URL}/scan/position",
            json=POSITION_SCAN,
            headers=HEADERS
        )
        assert response.status_code == 200
        assert response.json() == {"status": "created"}

    def test_empty_username_header(self):
        headers = {"X-Username": "", "Content-Type": "application/json"}
        response = requests.post(
            f"{BASE_URL}/scan/position",
            json=POSITION_SCAN,
            headers=headers
        )
        assert response.status_code == 400

    def test_invalid_position_negative(self):
        data = {"pos_x": -1, "pos_y": -1, "pos_z": -1}
        response = requests.post(
            f"{BASE_URL}/scan/position",
            json=data,
            headers=HEADERS
        )
        assert response.status_code == 200


class TestInventoryScan:
    def test_success_full_inventory(self):
        response = requests.post(
            f"{BASE_URL}/scan/inventory",
            json=INVENTORY_SCAN,
            headers=HEADERS
        )
        assert response.status_code == 200
        assert response.json() == {"status": "created"}

    def test_success_minimal_inventory(self):
        response = requests.post(
            f"{BASE_URL}/scan/inventory",
            json=MINIMAL_INVENTORY_SCAN,
            headers=HEADERS
        )
        assert response.status_code == 200
        assert response.json() == {"status": "created"}

    def test_success_single_item(self):
        data = {"items": [{"item_name": "NETHERITE_PICKAXE", "item_amount": 1}]}
        response = requests.post(
            f"{BASE_URL}/scan/inventory",
            json=data,
            headers=HEADERS
        )
        assert response.status_code == 200

    def test_success_empty_inventory(self):
        data = {"items": []}
        response = requests.post(
            f"{BASE_URL}/scan/inventory",
            json=data,
            headers=HEADERS
        )
        assert response.status_code == 200

    def test_missing_username_header(self):
        response = requests.post(
            f"{BASE_URL}/scan/inventory",
            json=MINIMAL_INVENTORY_SCAN,
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 400

    def test_invalid_item_amount_negative(self):
        data = {"items": [{"item_name": "DIAMOND", "item_amount": -5}]}
        response = requests.post(
            f"{BASE_URL}/scan/inventory",
            json=data,
            headers=HEADERS
        )
        assert response.status_code == 200