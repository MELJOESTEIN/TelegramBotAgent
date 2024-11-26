import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

async def test_mongodb_connection(uri: str):
    try:
        # 1. Test Basic Connection
        client = AsyncIOMotorClient(uri)
        print("✅ Successfully connected to MongoDB")
        
        # 2. Test Database Operations
        db = client.expense_tracker
        test_collection = db.test_collection
        
        # Test Write Operation
        test_doc = {
            "test_id": 1,
            "timestamp": datetime.now(),
            "message": "Test connection"
        }
        result = await test_collection.insert_one(test_doc)
        print(f"✅ Write test successful. Inserted ID: {result.inserted_id}")
        
        # Test Read Operation
        found_doc = await test_collection.find_one({"test_id": 1})
        if found_doc:
            print("✅ Read test successful")
        
        # Test Update Operation
        update_result = await test_collection.update_one(
            {"test_id": 1},
            {"$set": {"message": "Updated test"}}
        )
        print(f"✅ Update test successful. Modified count: {update_result.modified_count}")
        
        # Test Delete Operation
        delete_result = await test_collection.delete_one({"test_id": 1})
        print(f"✅ Delete test successful. Deleted count: {delete_result.deleted_count}")
        
        # 3. Test Database Information
        db_list = await client.list_database_names()
        print(f"📊 Available databases: {', '.join(db_list)}")
        
        collections = await db.list_collection_names()
        print(f"📊 Collections in expense_tracker: {', '.join(collections)}")
        
        return True

    except Exception as e:
        print(f"❌ Error connecting to MongoDB: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Check if your MongoDB server is running")
        print("2. Verify your connection string format")
        print("3. Ensure network connectivity")
        print("4. Check if IP address is whitelisted (for remote connections)")
        print("5. Verify username and password are correct")
        return False
    finally:
        client.close()

if __name__ == "__main__":
    # Your MongoDB URI
    MONGODB_URI = "mongodb+srv://prontix:admin@botdevelopementcluster.5ogfo.mongodb.net/?retryWrites=true&w=majority&appName=BotDevelopementCluster"
    
    print("🔍 Testing MongoDB Connection...")
    asyncio.run(test_mongodb_connection(MONGODB_URI))