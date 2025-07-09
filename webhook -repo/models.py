from pymongo import MongoClient
from datetime import datetime
import json

class WebhookModel:
    def __init__(self, mongodb_uri, db_name):
        self.client = MongoClient(mongodb_uri)
        self.db = self.client[db_name]
        self.collection = self.db.webhooks
    
    def insert_webhook(self, webhook_data):
        """Insert webhook data into MongoDB"""
        try:
            result = self.collection.insert_one(webhook_data)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error inserting webhook: {e}")
            return None
    
    def get_latest_webhooks(self, limit=50):
        """Get latest webhooks sorted by timestamp"""
        try:
            webhooks = list(self.collection.find().sort("timestamp", -1).limit(limit))
            return webhooks
        except Exception as e:
            print(f"Error fetching webhooks: {e}")
            return []
    
    def close_connection(self):
        """Close MongoDB connection"""
        self.client.close()