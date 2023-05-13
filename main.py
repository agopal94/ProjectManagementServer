from fastapi import FastAPI, Depends
from models import models
import uuid
from datetime import datetime
from constants import constants
from sqlalchemy.orm import Session
from database import SessionLocal

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Endpoints

#Creation

@app.post("/createProject")
async def create_project(project: models.CreateProjectObj, db:Session = Depends(get_db)):
    enrichedProject = enrichProjectObject(project)
    return insert_project(db, enrichedProject)

@app.post("/createTask")
async def create_task(task: models.CreateTaskObj, db:Session = Depends(get_db)):
    enrichedTask = enrichTaskObject(task)
    return insert_task(db, enrichedTask)

#Updating
@app.post("/updateProject")
async def update_project(project: models.Project, db: Session = Depends(get_db)):
    curr_proj = db.query(models.ProjectDBRow).filter(models.ProjectDBRow.pid == project.pid).first()
    if curr_proj is None:
        raise Exception
    curr_proj.pdesc = project.pdesc
    curr_proj.pname = project.pname
    curr_proj.status = project.status
    curr_proj.updatedTs = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    db.commit()
    db.refresh(curr_proj)
    return curr_proj

@app.post("/updateTask")
async def update_task(task: models.Task, db: Session = Depends(get_db)):
    curr_task = db.query(models.TasksDBRow).filter(models.TasksDBRow.tid == task.tid).first()
    if curr_task is None:
        raise Exception
    curr_task.tdesc = task.pdesc
    curr_task.tname = task.pname
    curr_task.status = task.status
    curr_task.pid = task.pid
    curr_task.updatedTs = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    db.commit()
    db.refresh(curr_task)
    return curr_task


#Reading

@app.get("/getAllProjects")
async def get_all_projects(db:Session = Depends(get_db)):
    return db.query(models.ProjectDBRow).all()

@app.get("/getProjectById")
async def get_project_by_id(pid: str, db:Session = Depends(get_db)):
    return db.query(models.ProjectDBRow).filter(models.ProjectDBRow.pid == pid).first()

@app.get("/getAllTasks")
async def get_all_tasks(db:Session = Depends(get_db)):
    return db.query(models.TasksDBRow).all()

@app.get("/getTasksByPid")
async def get_tasks_by_pid(pid: str, db:Session = Depends(get_db)):
    return db.query(models.TasksDBRow).filter(models.TasksDBRow.pid == pid).all()

@app.get("/getTaskById")
async def get_task_by_id(tid: str, db:Session = Depends(get_db)):
    return db.query(models.TasksDBRow).filter(models.TasksDBRow.tid == tid).first()

#DB Methods

def insert_project(session: Session, projectObj: models.Project):
    project_details = session.query(models.ProjectDBRow).filter(models.ProjectDBRow.pid == projectObj.pid).first()
    if project_details is not None:
        raise Exception()
    new_project_info = models.ProjectDBRow(**projectObj.dict())
    session.add(new_project_info)
    session.commit()
    session.refresh(new_project_info)
    return new_project_info

def insert_task(session: Session, taskObj: models.Task):
    task_details = session.query(models.TasksDBRow).filter(models.TasksDBRow.tid == taskObj.tid).first()
    if task_details is not None:
        raise Exception()
    new_task_info = models.TasksDBRow(**taskObj.dict())
    session.add(new_task_info)
    session.commit()
    session.refresh(new_task_info)
    return new_task_info

#Helper Methods

def enrichTaskObject(taskObj: models.CreateTaskObj):
    currTimeNow = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    task = models.Task(createdTs=currTimeNow,pid=taskObj.pid,tdesc=taskObj.tDesc,
                       tid=str(uuid.uuid1()), tname=taskObj.tName,
                       status=constants.TASK_STATUS_NEW,updatedTs=currTimeNow)
    return task


def enrichProjectObject(projectObj: models.CreateProjectObj):
    currTimeNow = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    project = models.Project(createdTs=currTimeNow, pdesc=projectObj.pDesc, 
                             pname=projectObj.pName, updatedTs=currTimeNow,
                             pid=str(uuid.uuid1()), status=constants.PROJECT_STATUS_NEW)
    return project
