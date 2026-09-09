from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from .agent import run_shopping_agent
from .products import load_products, compare_products

SECRET_KEY = "development-secret-change-me"
ALGORITHM = "HS256"

engine = create_engine(
    "sqlite:///./buywise.db",
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="customer")

Base.metadata.create_all(engine)

def db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

with SessionLocal() as session:
    if not session.query(User).filter_by(email="demo@buywise.ai").first():
        session.add(User(
            email="demo@buywise.ai",
            password_hash=pwd.hash("demo123"),
            role="customer"
        ))
        session.commit()

app = FastAPI(
    title="BuyWise",
    description="Autonomous E-Commerce Shopping Agent",
    version="0.1.0"
)

class LoginRequest(BaseModel):
    email: str
    password: str

class ShoppingRequest(BaseModel):
    message: str

class CompareRequest(BaseModel):
    product_ids: list[int]

@app.get("/")
def root():
    return {"project": "BuyWise", "status": "running"}

@app.get("/products")
def products():
    return load_products()

@app.post("/auth/login")
def login(data: LoginRequest, session: Session = Depends(db)):
    user = session.query(User).filter_by(email=data.email).first()

    if not user or not pwd.verify(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = jwt.encode(
        {"sub": str(user.id), "role": user.role},
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {"access_token": token, "token_type": "bearer"}

def current_user(
    credentials=Depends(security),
    session: Session = Depends(db)
):
    try:
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        user = session.get(User, int(payload["sub"]))

        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except (JWTError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/shopping/ask")
def shopping(
    data: ShoppingRequest,
    user: User = Depends(current_user)
):
    result = run_shopping_agent(data.message)

    return {
        "user": user.email,
        "intent": result["intent"],
        "confidence": result["confidence"],
        "route": result["route"],
        "response": result["response"],
        "products": result["products"]
    }

@app.post("/products/compare")
def compare(
    data: CompareRequest,
    user: User = Depends(current_user)
):
    products = compare_products(data.product_ids)

    return {
        "count": len(products),
        "products": products
    }
