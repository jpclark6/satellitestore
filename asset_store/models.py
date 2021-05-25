from enum import Enum
import re

from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship, backref, validates
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import null


Base = declarative_base()


class TypeChoice(Enum):
    SATELLITE = "satellite"
    ANTENNA = "antenna"


class AssetClassChoice(Enum):
    DOVE = "dove"
    RAPIDEYE = "rapideye"
    SKYSAT = "skysat"
    DISH = "dish"
    YAGI = "yagi"


class Asset(Base):
    __tablename__ = "asset"
    name = Column(String(64), primary_key=True)
    asset_class = Column(Integer, ForeignKey('asset_class.id'))
    created_at = Column(DateTime)

    @validates("name")
    def validate_name(self, key, value):
        """
        Values can only contain alphanumeric ascii characters, underscores, and dashes
        Values cannot start with an underscore or dash
        Values must be between 4 and 64 characters long
        """
        assert re.search(r"^(?![-_])[a-zA-Z0-9_-]{4,64}$", value)
        return value

    @property
    def asset_type(self):
        return self.asset_class.class_type.value


class AssetClass(Base):
    __tablename__ = "asset_class"
    id = Column(Integer, primary_key=True)
    class_name = Column(
        Enum(AssetClassChoice, values_callable=lambda obj: [e.value for e in obj]), nullable=False
    )
    class_type = Column(
        Enum(TypeChoice, values_callable=lambda obj: [e.value for e in obj]), nullable=False
    )
    assets = relationship("Asset", backref="asset_class")
