from pydantic import BaseModel
from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, Enum
from database import Base
import enum

class CreateProjectObj(BaseModel):
    pName: str
    pDesc: str

class CreateTaskObj(BaseModel):
    tName: str
    tDesc: str
    pid: str

class Project(BaseModel):
    pid: str
    pname: str
    pdesc: str
    status: str
    createdTs: str
    updatedTs: str

class Task(BaseModel):
    tid: str
    pid: str
    tname: str
    tdesc: str
    status: str
    createdTs: str
    updatedTs: str

class ProjectDBRow(Base):
    __tablename__ = "projects"

    pid = Column(String, primary_key=True, nullable=False)
    pname = Column(String, nullable=False)
    pdesc = Column(String, nullable=True)
    createdTs = Column(String, nullable=False)
    updatedTs = Column(String, nullable=False)
    status = Column(String, nullable=False)

class TasksDBRow(Base):
    __tablename__ = "tasks"

    tid = Column(String, primary_key=True, nullable=False)
    pid = Column(String, nullable=False)
    tname = Column(String, nullable=False)
    tdesc = Column(String, nullable=True)
    createdTs = Column(String, nullable=False)
    updatedTs = Column(String, nullable=False)
    status = Column(String, nullable=False)