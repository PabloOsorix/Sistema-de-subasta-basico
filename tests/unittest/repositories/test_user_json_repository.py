import unittest
import json
import os
from unittest.mock import patch, mock_open
from app.external.data_access.repositories.json_user_repository import JsonUserRepository
from app.external.data_access.entities.user_json_entity import UserJsonEntity


class TestJsonUserRepository(unittest.TestCase):
    def setUp(self):
        self.repository = JsonUserRepository()
        self.mock_data = {
            "users": [
                {
                    "id": "94597574-a361-4e33-99f6-71c43d06d792",
                    "username": "Juan Osorio",
                    "email": "osoriojuan@gmail.com",
                    "hashed_password": "$2b$12$ank7Wk1SXfln2bUinLRodeliDpLd4Q95a2BnWiVS.CF027a336GRm",
                    "type": "Investor",
                    "create_date": "2024-09-13 11:52:23"
                },
                {
                    "id": "9c522ff5-09d2-4a67-b5f8-224d273c60ff",
                    "username": "johndoe",
                    "email": "johndoe@example.com",
                    "hashed_password": "$2b$12$uHaUBo6Cbn/VIWBs2nCzVefIwF4FpERVRObq9B66JCjg1SUOYZJFu",
                    "type": "Operator",
                    "create_date": "2024-09-13 11:52:24"
                }
            ]
        }

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({"users": []}))
    def test_read(self, mock_file):
        result = self.repository.read()
        self.assertEqual(result, {"users": []})
        mock_file.assert_called_once_with(self.repository.file_path, '+r', encoding="utf-8")

    @patch("json.dump")
    @patch("builtins.open", new_callable=mock_open)
    def test_save(self, mock_file, mock_json_dump):

        user = UserJsonEntity(
                id="2e778ba0-fed8-4473-be97-4a27e4b9d909",
                username="Juan Osorio",
                email="osorixjuan@gmail.com",
                hashed_password="$2b$12$ank7Wk1SXfln2bUinLRodeliDpLd4Q95a2BnWiVS.CF027a336GRm",
                type="Investor",
                create_date="2024-09-13 11:52:23"
        )
        
        with patch.object(self.repository, 'read', return_value=self.mock_data):
            self.repository.save(user)

        mock_file.assert_called_once_with(self.repository.file_path, "+w", encoding='utf-8')
        mock_json_dump.assert_called_once()
        args, _ = mock_json_dump.call_args
        self.assertNotEqual(len(args[0]["users"]), 2)  # Verifica que se agregó un nuevo usuario

    @patch.object(JsonUserRepository, "read")
    def test_get_user_by_email_existing(self, mock_read):
        mock_read.return_value = self.mock_data
        user = self.repository.get_user_by_email("osoriojuan@gmail.com")
        self.assertIsInstance(user, UserJsonEntity)
        self.assertEqual(user.email, "osoriojuan@gmail.com")

    @patch.object(JsonUserRepository, "read")
    def test_get_user_by_email_non_existing(self, mock_read):
        mock_read.return_value = self.mock_data
        user = self.repository.get_user_by_email("nonexistent@example.com")
        self.assertFalse(user)

    @patch.object(JsonUserRepository, "read")
    def test_get_user_by_id_existing(self, mock_read):
        mock_read.return_value = self.mock_data
        print(mock_read.return_value)
        user = self.repository.get_user_by_id("94597574-a361-4e33-99f6-71c43d06d792")
        self.assertIsInstance(user, UserJsonEntity)
        self.assertEqual(user.id, "94597574-a361-4e33-99f6-71c43d06d792")

    @patch.object(JsonUserRepository, "read")
    def test_get_user_by_id_non_existing(self, mock_read):
        mock_read.return_value = self.mock_data
        user = self.repository.get_user_by_id("999")
        self.assertFalse(user)
