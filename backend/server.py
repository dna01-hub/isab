from fastapi import FastAPI, APIRouter, HTTPException, Depends
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime
import re

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Models
class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    whatsapp: str
    companions: List[str] = []
    stay_connected: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(BaseModel):
    name: str
    whatsapp: str
    companions: List[str] = []
    stay_connected: bool = False

class UserLogin(BaseModel):
    name: str
    whatsapp: str

class Gift(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    category: str
    image_url: str
    buy_link: Optional[str] = None
    quantity: int = 1
    price_range: Optional[str] = None
    is_unique: bool = True  # Se verdadeiro, apenas um convidado pode escolher
    created_at: datetime = Field(default_factory=datetime.utcnow)

class GiftReservation(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    gift_id: str
    quantity: int = 1
    reserved_at: datetime = Field(default_factory=datetime.utcnow)

# Initialize gifts data
INITIAL_GIFTS = [
    # Fraldas
    {
        "name": "Fralda Recém-nascido (RN)",
        "description": "Pacote de fraldas RN para os primeiros dias das bebês",
        "category": "fraldas",
        "image_url": "https://images.unsplash.com/photo-1622290291165-d341f1938b8a?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHwzfHxiYWJ5JTIwc2hvd2VyfGVufDB8fHx8MTc1MzQ5OTYwMXww&ixlib=rb-4.1.0&q=85",
        "buy_link": "https://www.amazon.com.br",
        "quantity": 50,
        "price_range": "R$ 15-25",
        "is_unique": False
    },
    {
        "name": "Fralda Tamanho P",
        "description": "Pacote de fraldas P para o crescimento das bebês",
        "category": "fraldas",
        "image_url": "https://images.unsplash.com/photo-1622290291165-d341f1938b8a?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHwzfHxiYWJ5JTIwc2hvd2VyfGVufDB8fHx8MTc1MzQ5OTYwMXww&ixlib=rb-4.1.0&q=85",
        "buy_link": "https://www.amazon.com.br",
        "quantity": 30,
        "price_range": "R$ 20-30",
        "is_unique": False
    },
    {
        "name": "Fralda Tamanho M",
        "description": "Pacote de fraldas M para quando crescerem mais",
        "category": "fraldas",
        "image_url": "https://images.unsplash.com/photo-1622290291165-d341f1938b8a?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHwzfHxiYWJ5JTIwc2hvd2VyfGVufDB8fHx8MTc1MzQ5OTYwMXww&ixlib=rb-4.1.0&q=85",
        "buy_link": "https://www.amazon.com.br",
        "quantity": 20,
        "price_range": "R$ 25-35",
        "is_unique": False
    },
    # Roupas
    {
        "name": "Body Manga Curta RN",
        "description": "Body de algodão para recém-nascidas",
        "category": "roupas",
        "image_url": "https://images.unsplash.com/photo-1622290319146-7b63df48a635?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHwyfHxiYWJ5JTIwc2hvd2VyfGVufDB8fHx8MTc1MzQ5OTYwMXww&ixlib=rb-4.1.0&q=85",
        "buy_link": "https://www.amazon.com.br",
        "quantity": 10,
        "price_range": "R$ 15-30",
        "is_unique": False
    },
    {
        "name": "Macacão de Bebê",
        "description": "Macacão confortável para o dia a dia",
        "category": "roupas",
        "image_url": "https://images.unsplash.com/photo-1622290319146-7b63df48a635?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHwyfHxiYWJ5JTIwc2hvd2VyfGVufDB8fHx8MTc1MzQ5OTYwMXww&ixlib=rb-4.1.0&q=85",
        "buy_link": "https://www.amazon.com.br",
        "quantity": 8,
        "price_range": "R$ 25-45",
        "is_unique": False
    },
    # Higiene
    {
        "name": "Kit Higiene Bebê",
        "description": "Kit completo com shampoo, sabonete e hidratante",
        "category": "higiene",
        "image_url": "https://images.unsplash.com/photo-1622290291165-d341f1938b8a?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHwzfHxiYWJ5JTIwc2hvd2VyfGVufDB8fHx8MTc1MzQ5OTYwMXww&ixlib=rb-4.1.0&q=85",
        "buy_link": "https://www.amazon.com.br",
        "quantity": 5,
        "price_range": "R$ 40-80",
        "is_unique": False
    },
    {
        "name": "Toalhas de Bebê",
        "description": "Kit com toalhas macias para as bebês",
        "category": "higiene",
        "image_url": "https://images.unsplash.com/photo-1622290319146-7b63df48a635?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHwyfHxiYWJ5JTIwc2hvd2VyfGVufDB8fHx8MTc1MzQ5OTYwMXww&ixlib=rb-4.1.0&q=85",
        "buy_link": "https://www.amazon.com.br",
        "quantity": 6,
        "price_range": "R$ 30-60",
        "is_unique": False
    },
    # Alimentação
    {
        "name": "Mamadeiras Anticólica",
        "description": "Kit de mamadeiras para alimentação das gêmeas",
        "category": "alimentacao",
        "image_url": "https://images.unsplash.com/photo-1597413545419-4013431dbfec?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzh8MHwxfHNlYXJjaHwxfHx0d2luc3xlbnwwfHx8fDE3NTM0OTk2MDl8MA&ixlib=rb-4.1.0&q=85",
        "buy_link": "https://www.amazon.com.br",
        "quantity": 4,
        "price_range": "R$ 50-100",
        "is_unique": False
    },
    # Quarto
    {
        "name": "Berço para Gêmeas",
        "description": "Berço seguro e confortável",
        "category": "quarto",
        "image_url": "https://images.unsplash.com/photo-1597413545419-4013431dbfec?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzh8MHwxfHNlYXJjaHwxfHx0d2luc3xlbnwwfHx8fDE3NTM0OTk2MDl8MA&ixlib=rb-4.1.0&q=85",
        "buy_link": "https://www.amazon.com.br",
        "quantity": 2,
        "price_range": "R$ 300-600",
        "is_unique": True
    },
    {
        "name": "Kit Lençol de Berço",
        "description": "Lençóis macios para o berço das bebês",
        "category": "quarto",
        "image_url": "https://images.unsplash.com/photo-1622290319146-7b63df48a635?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHwyfHxiYWJ5JTIwc2hvd2VyfGVufDB8fHx8MTc1MzQ5OTYwMXww&ixlib=rb-4.1.0&q=85",
        "buy_link": "https://www.amazon.com.br",
        "quantity": 4,
        "price_range": "R$ 40-80",
        "is_unique": False
    },
    # Passeio
    {
        "name": "Carrinho Duplo para Gêmeas",
        "description": "Carrinho prático para passear com as duas",
        "category": "passeio",
        "image_url": "https://images.unsplash.com/photo-1597413545419-4013431dbfec?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzh8MHwxfHNlYXJjaHwxfHx0d2luc3xlbnwwfHx8fDE3NTM0OTk2MDl8MA&ixlib=rb-4.1.0&q=85",
        "buy_link": "https://www.amazon.com.br",
        "quantity": 1,
        "price_range": "R$ 400-800",
        "is_unique": True
    },
    {
        "name": "Bebê Conforto",
        "description": "Bebê conforto para segurança no carro",
        "category": "passeio",
        "image_url": "https://images.unsplash.com/photo-1622290291165-d341f1938b8a?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHwzfHxiYWJ5JTIwc2hvd2VyfGVufDB8fHx8MTc1MzQ5OTYwMXww&ixlib=rb-4.1.0&q=85",
        "buy_link": "https://www.amazon.com.br",
        "quantity": 2,
        "price_range": "R$ 200-400",
        "is_unique": True
    }
]

# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "isabelle_isadora_2025"

# Routes

@api_router.post("/register", response_model=User)
async def register_user(user_data: UserCreate):
    # Validate WhatsApp format
    whatsapp_pattern = r'^\(\d{2}\)\s?\d{4,5}-?\d{4}$|^\d{2}\d{4,5}\d{4}$|^\+\d{2}\d{2}\d{4,5}\d{4}$'
    if not re.match(whatsapp_pattern, user_data.whatsapp.replace(" ", "").replace("-", "")):
        raise HTTPException(status_code=400, detail="Formato de WhatsApp inválido")
    
    # Check if user already exists
    existing_user = await db.users.find_one({"whatsapp": user_data.whatsapp}, {"_id": 0})
    if existing_user:
        raise HTTPException(status_code=400, detail="WhatsApp já cadastrado")
    
    user = User(**user_data.dict())
    await db.users.insert_one(user.dict())
    return user

@api_router.post("/login")
async def login_user(login_data: UserLogin):
    user = await db.users.find_one({
        "name": login_data.name,
        "whatsapp": login_data.whatsapp
    }, {"_id": 0})
    
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return User(**user)

@api_router.get("/gifts/{category}")
async def get_gifts_by_category(category: str):
    gifts = await db.gifts.find({"category": category}, {"_id": 0}).to_list(1000)
    if not gifts:
        return []
    
    # Get reservations to check availability
    gift_ids = [gift["id"] for gift in gifts]
    reservations = await db.reservations.find({"gift_id": {"$in": gift_ids}}, {"_id": 0}).to_list(1000)
    
    reservation_counts = {}
    for reservation in reservations:
        gift_id = reservation["gift_id"]
        reservation_counts[gift_id] = reservation_counts.get(gift_id, 0) + reservation["quantity"]
    
    # Add availability info to gifts
    for gift in gifts:
        gift_id = gift["id"]
        reserved_qty = reservation_counts.get(gift_id, 0)
        gift["available_quantity"] = gift["quantity"] - reserved_qty
        gift["is_available"] = gift["available_quantity"] > 0
    
    return gifts

@api_router.get("/gifts")
async def get_all_gifts():
    gifts = await db.gifts.find({}, {"_id": 0}).to_list(1000)
    
    # Get reservations to check availability
    gift_ids = [gift["id"] for gift in gifts]
    reservations = await db.reservations.find({"gift_id": {"$in": gift_ids}}, {"_id": 0}).to_list(1000)
    
    reservation_counts = {}
    for reservation in reservations:
        gift_id = reservation["gift_id"]
        reservation_counts[gift_id] = reservation_counts.get(gift_id, 0) + reservation["quantity"]
    
    # Add availability info to gifts
    for gift in gifts:
        gift_id = gift["id"]
        reserved_qty = reservation_counts.get(gift_id, 0)
        gift["available_quantity"] = gift["quantity"] - reserved_qty
        gift["is_available"] = gift["available_quantity"] > 0
    
    return gifts

@api_router.post("/reserve-gift")
async def reserve_gift(reservation_data: dict):
    user_id = reservation_data["user_id"]
    gift_id = reservation_data["gift_id"]
    quantity = reservation_data.get("quantity", 1)
    
    # Check if gift exists
    gift = await db.gifts.find_one({"id": gift_id}, {"_id": 0})
    if not gift:
        raise HTTPException(status_code=404, detail="Presente não encontrado")
    
    # Check availability
    existing_reservations = await db.reservations.find({"gift_id": gift_id}, {"_id": 0}).to_list(1000)
    total_reserved = sum(res["quantity"] for res in existing_reservations)
    
    if total_reserved + quantity > gift["quantity"]:
        raise HTTPException(status_code=400, detail="Quantidade insuficiente disponível")
    
    # Create reservation
    reservation = GiftReservation(
        user_id=user_id,
        gift_id=gift_id,
        quantity=quantity
    )
    
    await db.reservations.insert_one(reservation.dict())
    return {"message": "Presente reservado com sucesso!", "reservation": reservation}

@api_router.get("/user/{user_id}/reservations")
async def get_user_reservations(user_id: str):
    reservations = await db.reservations.find({"user_id": user_id}, {"_id": 0}).to_list(1000)
    
    # Get gift details for each reservation
    gift_ids = [res["gift_id"] for res in reservations]
    gifts = await db.gifts.find({"id": {"$in": gift_ids}}, {"_id": 0}).to_list(1000)
    gift_dict = {gift["id"]: gift for gift in gifts}
    
    detailed_reservations = []
    for res in reservations:
        gift = gift_dict.get(res["gift_id"])
        if gift:
            detailed_reservations.append({
                "reservation": res,
                "gift": gift
            })
    
    return detailed_reservations

@api_router.post("/admin/login")
async def admin_login(credentials: dict):
    if credentials.get("username") != ADMIN_USERNAME or credentials.get("password") != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    return {"message": "Login administrativo realizado com sucesso"}

@api_router.get("/admin/dashboard")
async def get_admin_dashboard():
    # Get all users
    users = await db.users.find({}, {"_id": 0}).to_list(1000)
    total_confirmed = len(users)
    total_companions = sum(len(user.get("companions", [])) for user in users)
    total_attendees = total_confirmed + total_companions
    
    # Get all reservations with user and gift details
    reservations = await db.reservations.find({}, {"_id": 0}).to_list(1000)
    gifts = await db.gifts.find({}, {"_id": 0}).to_list(1000)
    
    gift_dict = {gift["id"]: gift for gift in gifts}
    user_dict = {user["id"]: user for user in users}
    
    detailed_reservations = []
    for res in reservations:
        gift = gift_dict.get(res["gift_id"])
        user = user_dict.get(res["user_id"])
        if gift and user:
            detailed_reservations.append({
                "user_name": user["name"],
                "gift_name": gift["name"],
                "quantity": res["quantity"],
                "reserved_at": res["reserved_at"]
            })
    
    # Calculate gift statistics
    total_gifts_reserved = len(detailed_reservations)
    total_gifts_available = sum(gift["quantity"] for gift in gifts)
    
    reservation_counts = {}
    for res in reservations:
        gift_id = res["gift_id"]
        reservation_counts[gift_id] = reservation_counts.get(gift_id, 0) + res["quantity"]
    
    available_gifts = []
    for gift in gifts:
        reserved_qty = reservation_counts.get(gift["id"], 0)
        available_qty = gift["quantity"] - reserved_qty
        if available_qty > 0:
            available_gifts.append({
                "name": gift["name"],
                "available_quantity": available_qty
            })
    
    return {
        "total_confirmed": total_confirmed,
        "total_companions": total_companions,
        "total_attendees": total_attendees,
        "total_gifts_reserved": total_gifts_reserved,
        "total_gifts_available": total_gifts_available,
        "users": users,
        "reservations": detailed_reservations,
        "available_gifts": available_gifts
    }

# Initialize database with gifts
@app.on_event("startup")
async def startup_db():
    # Check if gifts already exist
    existing_gifts = await db.gifts.count_documents({})
    if existing_gifts == 0:
        # Insert initial gifts
        gifts_to_insert = []
        for gift_data in INITIAL_GIFTS:
            gift = Gift(**gift_data)
            gifts_to_insert.append(gift.dict())
        
        if gifts_to_insert:
            await db.gifts.insert_many(gifts_to_insert)
            logger.info(f"Inserted {len(gifts_to_insert)} initial gifts")

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()