from fastapi import FastAPI
import subprocess
import os

app = FastAPI()

@app.get("/read-file")
def read_file(path: str):
    try:
        with open(path, "r") as f:
            return {"content": f.read()}
    except Exception as e:
        return {"error": str(e)}

@app.get("/run")
def run_command(cmd: str):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return {
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except Exception as e:
        return {"error": str(e)}

@app.post("/analyze-error")
def analyze_error(log: str):
    if "ModuleNotFoundError" in log:
        return {"suggestion": "Revisa si instalaste las dependencias con pip install"}
    if "npm ERR!" in log:
        return {"suggestion": "Ejecuta npm install o borra node_modules"}
    return {"suggestion": "Error no reconocido"}