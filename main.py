from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict
import uuid
import time
import asyncio

app = FastAPI()

job_storage: Dict[str, dict] = {}
job_queue = []
is_job_processor_active = False
priority_map = {"HIGH": 1, "MEDIUM": 2, "LOW": 3}

class JobRequest(BaseModel):
    ids: List[int]
    priority: str

@app.post("/ingest")
async def ingest_job(job_data: JobRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    timestamp = time.time()

    job_batches = []
    for i in range(0, len(job_data.ids), 3):
        batch_ids = job_data.ids[i:i+3]
        batch_id = str(uuid.uuid4())
        job_batches.append({
            "batch_id": batch_id,
            "ids": batch_ids,
            "status": "yet_to_start"
        })
        job_queue.append((job_data.priority.upper(), timestamp, job_id, batch_id, batch_ids))

    job_storage[job_id] = {
        "created_time": timestamp,
        "priority": job_data.priority.upper(),
        "batches": job_batches,
        "status": "yet_to_start"
    }

    if not is_job_processor_active:
        background_tasks.add_task(process_jobs)

    return {"ingestion_id": job_id}

@app.get("/status/{job_id}")
def get_job_status(job_id: str):
    job = job_storage.get(job_id)
    if not job:
        return {"error": "Job not found"}

    batch_statuses = [batch["status"] for batch in job["batches"]]
    if all(status == "completed" for status in batch_statuses):
        job["status"] = "completed"
    elif any(status == "triggered" for status in batch_statuses):
        job["status"] = "triggered"
    else:
        job["status"] = "yet_to_start"

    return {
        "ingestion_id": job_id,
        "status": job["status"],
        "batches": job["batches"]
    }

async def process_jobs():
    global is_job_processor_active
    is_job_processor_active = True

    while job_queue:
        job_queue.sort(key=lambda x: (priority_map[x[0]], x[1]))
        priority, timestamp, job_id, batch_id, batch_ids = job_queue.pop(0)

        for batch in job_storage[job_id]["batches"]:
            if batch["batch_id"] == batch_id:
                batch["status"] = "triggered"

        await asyncio.sleep(2)

        for batch in job_storage[job_id]["batches"]:
            if batch["batch_id"] == batch_id:
                batch["status"] = "completed"

        await asyncio.sleep(5)

    is_job_processor_active = False
