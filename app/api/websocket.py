from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from typing import Dict, List
from app.db.db import users_collection, messages_collection
import json
from bson import ObjectId
from datetime import datetime

router = APIRouter()
clients: Dict[str, List[WebSocket]] = {}

# Helper function to get user by car_id
def get_user_by_car_id(car_id: str):
    user = users_collection.find_one({"vehicle.carId": car_id})
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")

@router.websocket("/ws/{sender}/{car_id}")
async def websocket_endpoint(websocket: WebSocket, sender: str , car_id: str):
    await websocket.accept()
    user = get_user_by_car_id(car_id)
    if not user:
        await websocket.close()
        return

    if car_id not in clients:
        clients[car_id] = []
    clients[car_id].append(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            message_data['sender'] = sender
            message_data['timestamp'] = datetime.utcnow().isoformat()  # Add timestamp
            if 'receiver' not in message_data or not message_data['receiver']:
                await websocket.close()
                return
            await save_message(message_data)
            await broadcast_message(message_data, websocket)
    except WebSocketDisconnect:
        clients[car_id].remove(websocket)
        if not clients[car_id]:
            del clients[car_id]

async def broadcast_message(message_data: dict, sender: WebSocket):
    encoded_message = json.dumps(message_data, default=str)
    for client in clients.get(message_data['receiver'], []):
        if client != sender:
            await client.send_text(encoded_message)

async def save_message(message_data: dict):
    messages_collection.insert_one(message_data)

@router.get("/messages/{car_id}")
def get_messages(car_id: str):
    messages = list(messages_collection.find({"$or": [{"receiver": car_id}, {"sender": car_id}]}).sort("timestamp", -1))
    for message in messages:
        message["_id"] = str(message["_id"])
    return messages

@router.get("/last-chats/{car_id}")
def get_last_chats(car_id: str):
    pipeline = [
        {"$match": {"$or": [{"receiver": car_id}, {"sender": car_id}]}},
        {"$sort": {"timestamp": -1}},
        {"$group": {
            "_id": {"sender": "$sender", "receiver": "$receiver"},
            "doc": {"$first": "$$ROOT"}
        }},
        {"$replaceRoot": {"newRoot": "$doc"}}
    ]
    messages = list(messages_collection.aggregate(pipeline))
    for message in messages:
        message["_id"] = str(message["_id"])
    return messages

@router.get("/users/{car_id}")
def get_user_by_car_id_endpoint(car_id: str):
    user = users_collection.find_one({"vehicle.carId": car_id})
    if user:
        return {"car_id": car_id, "exists": True}
    else:
        raise HTTPException(status_code=404, detail="Car ID not found")

@router.delete("/messages/{message_id}")
def delete_message(message_id: str):
    result = messages_collection.delete_one({"_id": ObjectId(message_id)})
    if result.deleted_count == 1:
        return {"status": "success", "message": "Message deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Message not found")

@router.delete("/chats/{car_id}/{chat_partner}")
def delete_chat(car_id: str, chat_partner: str):
    result = messages_collection.delete_many({
        "$or": [
            {"sender": car_id, "receiver": chat_partner},
            {"sender": chat_partner, "receiver": car_id}
        ]
    })
    if result.deleted_count > 0:
        return {"status": "success", "message": "Chat deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Chat not found")