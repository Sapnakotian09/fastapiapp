from fastapi import APIRouter
from schemas.job import JobCreate,JobUpdate

router = APIRouter(prefix="/job",tags=["job"])
jobs=[]


@router.post("/")
def create_job(job:JobCreate):
    jobs.append(job)
    return jobs

@router.get("/")
def get_all_jobs():
    return jobs

@router.put("/{job_id}")
def update_job(job_id:int,job:JobUpdate):
    jobs[job_id] = job
    return jobs


@router.delete("/{job_id}")
def delete_job(job_id:int):
    jobs.pop(job_id)
    return jobs