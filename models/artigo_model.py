from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from core.configs import settings


class ArtigoModel(settings.DBBaseModel):
    __tablename__ = 'artigos'

    id = Column(Integer, primary_key=True, autoincremment = True)
    titulo = Column(String(256))
    