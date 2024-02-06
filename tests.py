import unittest
from datetime import datetime
from delivery_fee_calculator import calculate_delivery_fee

class TestDeliveryFeeCalculator(unittest.TestCase):

    def test_small_order_surcharge(self):
        # Test small order surcharge
        result = calculate_delivery_fee(750, 1200, 2, '2024-02-15T10:30:00')
        self.assertEqual(result, 550)

    def test_distance_surcharge(self):
        # Test distance surcharge
        result = calculate_delivery_fee(1800, 800, 3, '2024-02-15T14:45:00')
        self.assertEqual(result, 200)

    def test_free_delivery(self):
        # Test free delivery
        result = calculate_delivery_fee(25000, 1500, 1, '2024-02-15T18:00:00')
        self.assertEqual(result, 0)

    def test_friday_rush(self):
        # Test Friday rush
        result = calculate_delivery_fee(1200, 1000, 2, '2024-02-23T16:30:00')
        self.assertEqual(result, 240)

    def test_item_surcharge(self):
        # Test item surcharge
        result = calculate_delivery_fee(3000, 1200, 4, '2024-02-15T12:00:00')
        self.assertEqual(result, 300)

    def test_bulk_item_surcharge(self):
        # Test bulk item surcharge
        result = calculate_delivery_fee(4000, 1200, 15, '2024-02-15T17:15:00')
        self.assertEqual(result, 1090)

    def test_delivery_fee_cap(self):
        # Test delivery fee capped at 15€
        result = calculate_delivery_fee(180, 3500, 53, '2024-02-15T14:30:00')
        self.assertEqual(result, 1500)  

if __name__ == '__main__':
    unittest.main()