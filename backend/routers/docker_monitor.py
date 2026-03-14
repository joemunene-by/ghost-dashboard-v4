from fastapi import APIRouter, HTTPException
import docker
import psutil

router = APIRouter()

def get_client():
    try:
        return docker.from_env()
    except Exception:
        return None

@router.get("/containers")
def get_containers():
    client = get_client()
    if not client:
        return {"containers": [], "error": "Docker not accessible"}
    try:
        containers = []
        for c in client.containers.list(all=True):
            containers.append({
                "id": c.short_id,
                "name": c.name,
                "image": c.image.tags[0] if c.image.tags else "unknown",
                "status": c.status,
                "ports": c.ports,
            })
        return {"containers": containers, "total": len(containers)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/system")
def get_system():
    try:
        return {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "ram_total": round(psutil.virtual_memory().total / 1024**3, 2),
            "ram_used": round(psutil.virtual_memory().used / 1024**3, 2),
            "ram_percent": psutil.virtual_memory().percent,
            "disk_total": round(psutil.disk_usage('/').total / 1024**3, 2),
            "disk_used": round(psutil.disk_usage('/').used / 1024**3, 2),
            "disk_percent": psutil.disk_usage('/').percent,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
