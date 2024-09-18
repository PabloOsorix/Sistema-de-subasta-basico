import unittest
from unittest.mock import patch, mock_open
import json
from app.external.data_access.repositories.json_operation_repository import JsonOperationRepository
from app.external.data_access.entities.operation_json_entity import OperationJsonEntity
from datetime import datetime

class TestJsonOperationRepository(unittest.TestCase):

    def setUp(self):
        self.repo = JsonOperationRepository()
        self.mock_data = {
            "operations": [
                {
                    "id": "ecb9b643-e0fb-4f68-9c94-0edd9b6c17ca",
                    "user_id": "40b6ce25-bea1-4d10-9e93-10be572eb352",
                    "description": "Expansion y crecimiento de startup Wood, que genera ingresos de 10x la inversión que se está subastando",
                    "amount": 200000,
                    "available_amount": "0",
                    "interest_rate": 3.5,
                    "limit_date": "2024-09-15",
                    "status": "closed",
                    "create_date": "2024-09-15 11:19:17",
                    "type": "StandardOperation"
                },
                {
                    "id": "3ebbcc40-3cff-4489-b7a8-386296b6858a",
                    "user_id": "cb090840-803b-494b-97b5-b907e654001a",
                    "description": "Lo invertire en inmueble de finca raiz que esta en preacuerdo de venta.",
                    "amount": 50000,
                    "available_amount": 50000,
                    "interest_rate": 6.5,
                    "limit_date": "2024-10-25",
                    "status": "open",
                    "create_date": "2024-09-15 13:19:29",
                    "type": "StandardOperation"
                },
                {
                    "id": "7evvdd20-5cff-4489-a7b8-406586c6858d",
                    "user_id": "ebdc15a2-0a4e-44df-98dd-0fe370857d64",
                    "description": "Operacion de testeo",
                    "amount": 50000,
                    "available_amount": 50000,
                    "interest_rate": 6.5,
                    "limit_date": "2024-09-14",
                    "status": "open",
                    "create_date": "2024-09-15 13:19:29",
                    "type": "StandardOperation"
                }
            ]
        }
        self.operation = OperationJsonEntity(
            id="177c8333-04cb-4893-8891-9cd0648dc167",
            description="New Test to Update Operation",
            user_id="13289639-806a-4e9e-83d1-e4bc453b4c80",
            amount=200000,
            limit_date="2025-12-24",
            status="open",
            create_date=datetime.now().strftime("%Y-%m-%d"),
            interest_rate=5.3,
            available_amount=200000,
            type="StandardOperation"
            )
        
    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({"operations": []}))
    def test_read(self, mock_file):
        result = self.repo.read()
        self.assertEqual(result, [])
        mock_file.assert_called_once_with(self.repo.file_path, '+r', encoding="utf-8")

    @patch("json.dump")
    @patch("builtins.open", new_callable=mock_open)
    def test_write(self, mock_file, mock_json_dump):
        data = [self.operation]
        result = self.repo.write(data)
        self.assertTrue(result)
        mock_file.assert_called_once_with(self.repo.file_path, 'w', encoding='utf-8')
        mock_json_dump.assert_called_once_with({"operations": data}, mock_file(), ensure_ascii=False, indent=4)

    @patch.object(JsonOperationRepository, "read")
    @patch.object(JsonOperationRepository, "write")
    def test_save(self, mock_write, mock_read):
        mock_read.return_value = []
        mock_write.return_value = True
        result = self.repo.save(self.operation)
        self.assertTrue(result)
        mock_write.assert_called_once()

    @patch.object(JsonOperationRepository, "read")
    def test_get_single(self, mock_read):
        mock_read.return_value = self.mock_data["operations"]
        operation = self.repo.get({"id": "ecb9b643-e0fb-4f68-9c94-0edd9b6c17ca"})
        self.assertIsInstance(operation, OperationJsonEntity)
        self.assertEqual(operation.id, "ecb9b643-e0fb-4f68-9c94-0edd9b6c17ca")

    @patch.object(JsonOperationRepository, "read")
    def test_get_multiple(self, mock_read):
        mock_data = self.mock_data["operations"] * 2  # Duplicate the operation to have multiple results
        mock_read.return_value = mock_data
        operations = self.repo.get({"user_id": "cb090840-803b-494b-97b5-b907e654001a"})
        self.assertIsInstance(operations, list)
        self.assertEqual(len(operations), 2)

    @patch.object(JsonOperationRepository, "read")
    def test_get_not_found(self, mock_read):
        mock_read.return_value = self.mock_data["operations"]
        result = self.repo.get({"id": "999"})
        self.assertFalse(result)

    @patch.object(JsonOperationRepository, "read")
    @patch.object(JsonOperationRepository, "write")
    def test_update(self, mock_write, mock_read):
        mock_read.return_value = self.mock_data["operations"]
        mock_write.return_value = True
        operation_to_update = OperationJsonEntity(
            id="177c8333-04cb-4893-8891-9cd0648dc167",
            description="New Test to Update Operation",
            user_id="13289639-806a-4e9e-83d1-e4bc453b4c80",
            amount=200000,
            limit_date="2025-12-24",
            status="open",
            create_date=datetime.now().strftime("%Y-%m-%d"),
            interest_rate=5.3,
            available_amount=200000,
            type="StandardOperation"
            )
        result = self.repo.update(operation_to_update)
        self.assertTrue(result)
        mock_write.assert_called_once()

    @patch.object(JsonOperationRepository, "get")
    @patch.object(JsonOperationRepository, "update")
    def test_update_available_amount(self, mock_update, mock_get):
        mock_operation = OperationJsonEntity(
            id="177c8333-04cb-4893-8891-9cd0648dc167",
            user_id="13289639-806a-4e9e-83d1-e4bc453b4c80",
            description="New Test Operation operation",
            amount=200000,
            limit_date="2025-12-24",
            status="open",
            create_date=datetime.now().strftime("%Y-%m-%d"),
            interest_rate=5.3,
            available_amount=200000,
            type="StandardOperation"
            )
        mock_get.return_value = mock_operation
        mock_update.return_value = True
        result = self.repo.update_available_amount(
            "177c8333-04cb-4893-8891-9cd0648dc167", 80000
            )
        self.assertTrue(result)
        self.assertEqual(mock_operation.available_amount, 120000)
        mock_update.assert_called_once()

    @patch.object(JsonOperationRepository, "read")
    @patch.object(JsonOperationRepository, "write")
    def test_delete(self, mock_write, mock_read):
        mock_read.return_value = self.mock_data["operations"]
        mock_write.return_value = True
        result = self.repo.delete("ebdc15a2-0a4e-44df-98dd-0fe370857d64",
                                  "7evvdd20-5cff-4489-a7b8-406586c6858d"
                                  )
        self.assertTrue(result)
        mock_write.assert_called_once()
        # Verify that the status was changed to "delete"
        self.assertEqual(mock_write.call_args[0][0][2]["status"], "delete")
