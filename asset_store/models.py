import enum
import re

from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship, validates
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class AssetTypeChoice(enum.Enum):
    SATELLITE = "satellite"
    ANTENNA = "antenna"


class AssetClassChoice(enum.Enum):
    DOVE = "dove"
    RAPIDEYE = "rapideye"
    SKYSAT = "skysat"
    DISH = "dish"
    YAGI = "yagi"


class Asset(Base):
    __tablename__ = "asset"
    name = Column(String(64), primary_key=True)
    asset_class = Column(Integer, ForeignKey("asset_class.id"))
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
        return self.asset_class_details.class_type.value

    def verify_type(self, asset_class_detail, asset_type):
        assert asset_class_detail.class_type.value == asset_type


class AssetClass(Base):
    __tablename__ = "asset_class"
    id = Column(Integer, primary_key=True)
    class_name = Column(
        Enum(AssetClassChoice, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False,
    )
    class_type = Column(
        Enum(AssetTypeChoice, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False,
    )
    assets = relationship("Asset", backref="asset_class_details")
