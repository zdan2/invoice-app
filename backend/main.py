from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Literal

# SQLAlchemyのためのインポート
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

# --- 1. データベース設定 ---
DATABASE_URL = "sqlite:///./invoices.db"  # invoices.dbという名前のファイルが作られる

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- 2. データベースのテーブル（モデル）定義 ---
class DBInvoice(Base):
    __tablename__ = "invoices" # テーブル名を定義
    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String, index=True)
    file_name = Column(String)
    uploaded_at = Column(String)
    status = Column(String)

# --- 3. APIで受け渡しするためのデータモデル（スキーマ）定義 ---
InvoiceStatus = Literal["提出済み", "確認中", "承認済み", "差し戻し"]

class Invoice(BaseModel):
    id: int
    client_name: str
    file_name: str
    uploaded_at: str
    status: InvoiceStatus
    
    class Config:
        orm_mode = True # SQLAlchemyモデルをPydanticモデルに変換できるようにする

# --- FastAPIアプリの初期化 ---
app = FastAPI()

# --- CORS設定 ---
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 4. データベースセッションを管理するための関数 ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- 5. アプリ起動時にデータベースとテーブルを作成する ---
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    # --- 初回起動時に仮データを入れる ---
    db = SessionLocal()
    if db.query(DBInvoice).count() == 0:
        initial_invoices = [
            DBInvoice(client_name="ひかり保育園", file_name="2025年8月分請求書.xlsx", uploaded_at="2025-08-01 10:30", status="承認済み"),
            DBInvoice(client_name="さくら保育園", file_name="R7年8月請求書.pdf", uploaded_at="2025-08-03 15:00", status="確認中"),
            DBInvoice(client_name="つばさ保育園", file_name="【至急】8月分.xlsx", uploaded_at="2025-08-05 09:15", status="提出済み"),
        ]
        db.add_all(initial_invoices)
        db.commit()
    db.close()

# --- 6. APIエンドポイントの修正 ---
@app.get("/")
def read_root():
    return {"message": "請求書管理アプリのバックエンドへようこそ！"}

# 「/invoices」APIが、本物のデータベースからデータを取得するように変更
@app.get("/invoices", response_model=List[Invoice])
def get_invoices(db: Session = Depends(get_db)):
    invoices = db.query(DBInvoice).all()
    return invoices