from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    senha = Column(String)

    contas = relationship("Conta", back_populates="usuario")

class Conta(Base):
    __tablename__ = "contas"

    numero = Column(Integer, primary_key=True, index=True)
    saldo = Column(Float, default=0.0)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

    usuario = relationship("Usuario", back_populates="contas")
