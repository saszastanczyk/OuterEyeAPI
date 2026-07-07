import datetime
import uuid
from typing import Optional, List

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100))
    karma: Mapped[int] = mapped_column(default=20)
    register_date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now())

    actions:Mapped[List["Action"]] = relationship(back_populates="user")
    positions_scans: Mapped[ List["PositionScan"]] = relationship(back_populates="user")
    inventory_scans:Mapped[List["InventoryScan"]] = relationship(back_populates="user")

class Position(Base):
    __tablename__ = "positions"
    position_id: Mapped[int] = mapped_column(primary_key=True)
    pos_x: Mapped[int] = mapped_column()
    pos_y: Mapped[int] = mapped_column()
    pos_z: Mapped[int] = mapped_column()

    action: Mapped[List["Action"]] = relationship(back_populates="position")
    position_scan: Mapped["PositionScan"] = relationship(back_populates="position")

class Action(Base):
    __tablename__ = "actions"

    action_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id",ondelete="CASCADE"),index=True)
    position_id: Mapped[int] = mapped_column(ForeignKey("positions.position_id",ondelete="CASCADE"),index=True)
    happen_time: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now(),index=True)

    user: Mapped["User"] = relationship(back_populates="actions")
    position: Mapped["Position"] = relationship(Position, back_populates="action")

    meal_action: Mapped["MealAction"] = relationship(back_populates="action")
    craft_action: Mapped["CraftAction"] = relationship(back_populates="action")
    kill_action: Mapped["KillAction"] = relationship(back_populates="action")
    breed_action: Mapped["BreedAction"] = relationship(back_populates="action")
    death_action: Mapped["DeathAction"] =    relationship(back_populates="action")
    pray_action: Mapped["PrayAction"] = relationship(back_populates="action")


class MealAction(Base):
    __tablename__ = "meal_actions"
    meal_id: Mapped[int] = mapped_column(primary_key=True)
    action_id: Mapped[int] = mapped_column(ForeignKey("actions.action_id",ondelete="CASCADE"),index=True)
    meal_name: Mapped[str] = mapped_column(String(100))

    action:Mapped["Action"] = relationship(back_populates="meal_action")

class CraftAction(Base):
    __tablename__ = "craft_actions"

    craft_id: Mapped[int] = mapped_column(primary_key=True)
    action_id: Mapped[int] = mapped_column(ForeignKey("actions.action_id",ondelete="CASCADE"),index=True)
    craft_subject: Mapped[str] = mapped_column(String(100))
    amount: Mapped[int] = mapped_column(default=1)

    action:Mapped["Action"] = relationship(back_populates="craft_action")

class KillAction(Base):
    __tablename__ = "kill_actions"

    kill_id: Mapped[int] = mapped_column(primary_key=True)
    action_id: Mapped[int] = mapped_column(ForeignKey("actions.action_id",ondelete="CASCADE"),index=True)
    killed_type: Mapped[str] = mapped_column(String(100))
    killed_subject_id: Mapped[Optional[uuid.UUID]]
    killed_name: Mapped[Optional[str]] = mapped_column(String(100))
    kill_tool: Mapped[str] = mapped_column(String(100))

    action:Mapped["Action"] = relationship(back_populates="kill_action")

class BreedAction(Base):
    __tablename__ = "breed_actions"
    breed_id: Mapped[int] = mapped_column(primary_key=True)
    action_id: Mapped[int] = mapped_column(ForeignKey("actions.action_id",ondelete="CASCADE"),index=True)
    father_subject_id: Mapped[uuid.UUID]
    mother_subject_id: Mapped[uuid.UUID]
    child_subject_id: Mapped[uuid.UUID]
    child_type: Mapped[str] = mapped_column(String(30))

    action:Mapped["Action"] = relationship(back_populates="breed_action")

class DeathAction(Base):
    __tablename__ = "death_actions"
    death_id: Mapped[int] = mapped_column(primary_key=True)
    action_id: Mapped[int] = mapped_column(ForeignKey("actions.action_id",ondelete="CASCADE"),index=True)
    death_cause: Mapped[str]

    action:Mapped["Action"] = relationship(back_populates="death_action")

class PrayAction(Base):
    __tablename__ = "pray_actions"

    pray_id: Mapped[int] = mapped_column(primary_key=True)
    action_id: Mapped[int] = mapped_column(ForeignKey("actions.action_id",ondelete="CASCADE"),index=True)
    pray_text: Mapped[Optional[str]] = mapped_column(String(1000))
    pray_respond: Mapped[Optional[str]] = mapped_column(String(1000))

    action:Mapped["Action"] = relationship(back_populates="pray_action")

class InventoryScan(Base):
    __tablename__ = "inventory_scans"

    inventory_scan_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id",ondelete="CASCADE"),index=True)
    time: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now(), index=True)

    user: Mapped["User"] = relationship(back_populates="inventory_scans")

    inventory_scan_items: Mapped[List["InventoryScanItem"]] = relationship(back_populates="inventory_scan")

class InventoryScanItem(Base):
    __tablename__ = "inventory_scan_items"

    scan_item_id: Mapped[int] = mapped_column(primary_key=True)
    inventory_scan_id: Mapped[int] = mapped_column(ForeignKey("inventory_scans.inventory_scan_id",ondelete="CASCADE"),index=True)
    item_name: Mapped[str] = mapped_column(String(100))
    amount: Mapped[int]

    inventory_scan: Mapped["InventoryScan"] = relationship(back_populates="inventory_scan_items")

class PositionScan(Base):
    __tablename__ = "positions_scans"

    position_scan_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id",ondelete="CASCADE"),index=True)
    position_id: Mapped[int] = mapped_column(ForeignKey("positions.position_id",ondelete="CASCADE"),index=True)
    scan_time: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now(), index=True)

    user: Mapped["User"] = relationship(back_populates="positions_scans")
    position: Mapped["Position"] = relationship(back_populates="position_scan")
