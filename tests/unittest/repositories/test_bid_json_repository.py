import unittest
from unittest.mock import patch, mock_open
import json
from app.external.data_access.repositories.json_bid_repository import JsonBidRepository
from app.external.data_access.entities.bid_json_entity import BidJsonEntity
from datetime import datetime
class TestJsonBidRepository(unittest.TestCase):

    def setUp(self):
        self.repo = JsonBidRepository()
        self.mock_data = {
            "bids": [
                {
                    "id": "6c1604a6-85d5-4bbd-a8bf-62d8d7ed787a",
                    "user_id": "7c6f9dfc-cba0-4cf2-9828-0517354ae07c",
                    "operation_id": "ecb9b643-e0fb-4f68-9c94-0edd9b6c17ca",
                    "amount": 57000,
                    "interest_rate": 2.5,
                    "create_date": "2024-09-15 11:22:44",
                    "status": "closed",
                    "type": "Bid"
                },
                {
                    "id": "c769a2e1-23f5-48eb-9411-6e41b0cf8b08",
                    "user_id": "419c5188-202d-4684-b748-66ab2b1bbdbcc",
                    "operation_id": "ecb9b643-e0fb-4f68-9c94-0edd9b6c17ca",
                    "amount": 50000,
                    "interest_rate": 2.2,
                    "create_date": "2024-09-15 15:49:33",
                    "status": "closed",
                    "type": "Bid"
                },
                {
                    "id": "ea1dc810-9f0a-4de8-8a98-b7c15567452b",
                    "user_id": "49ed60e5-5625-41a5-a2d1-0631e3ee3ed8",
                    "operation_id": "ecb9b643-e0fb-4f68-9c94-0edd9b6c17ca",
                    "amount": 143000,
                    "interest_rate": 2.2,
                    "create_date": "2024-09-16 20:35:53",
                    "status": "closed",
                    "type": "Bid"
                }
            ]
        }
        

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({"bids": []}))
    def test_read(self, mock_file):
        result = self.repo.read()
        self.assertEqual(result, [])
        mock_file.assert_called_once_with(self.repo.file_path, '+r', encoding="utf-8")

    @patch("json.dump")
    @patch("builtins.open", new_callable=mock_open)
    def test_write(self, mock_file, mock_json_dump):
        data = [{"id": "1", "user_id": "user1"}]
        result = self.repo.write(data)
        self.assertTrue(result)
        mock_file.assert_called_once_with(self.repo.file_path, 'w', encoding='utf-8')
        mock_json_dump.assert_called_once_with({"bids": data}, mock_file(), ensure_ascii=False, indent=4)

    @patch.object(JsonBidRepository, "read")
    @patch.object(JsonBidRepository, "write")
    def test_save(self, mock_write, mock_read):
        mock_read.return_value = []
        mock_write.return_value = True
        bid = BidJsonEntity(id="747a1e92-6ff7-4df7-bcdf-f9e5d3ec59ee",
                            user_id="ae54f732-7836-43c1-9eea-28bac09f0f81",
                            operation_id="f5e5b9a2-b1e7-469f-9f7a-d4b1aff5d0b9",
                            amount=20000,
                            interest_rate=0.06,
                            create_date=datetime.now().strftime("%Y-%m-%d"),
                            status="open",
                            type="Bid"
                            )
        result = self.repo.save(bid)
        self.assertTrue(result)
        mock_write.assert_called_once()

    @patch.object(JsonBidRepository, "read")
    def test_get_single(self, mock_read):
        mock_read.return_value = self.mock_data["bids"]
        bid = self.repo.get({"id": "6c1604a6-85d5-4bbd-a8bf-62d8d7ed787a"})
        self.assertIsInstance(bid, BidJsonEntity)
        self.assertEqual(bid.id, "6c1604a6-85d5-4bbd-a8bf-62d8d7ed787a")

    @patch.object(JsonBidRepository, "read")
    def test_get_multiple(self, mock_read):
        mock_data = self.mock_data["bids"] * 2  # Duplicate the bid to have multiple results
        mock_read.return_value = mock_data
        bids = self.repo.get({"user_id": "7c6f9dfc-cba0-4cf2-9828-0517354ae07c"})
        self.assertIsInstance(bids, list)
        self.assertEqual(len(bids), 2)

    @patch.object(JsonBidRepository, "read")
    def test_get_not_found(self, mock_read):
        mock_read.return_value = self.mock_data["bids"]
        result = self.repo.get({"id": "999"})
        self.assertFalse(result)

    @patch.object(JsonBidRepository, "read")
    @patch.object(JsonBidRepository, "write")
    def test_update(self, mock_write, mock_read):
        mock_read.return_value = self.mock_data