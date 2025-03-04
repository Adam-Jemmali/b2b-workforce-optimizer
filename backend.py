from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import sqlite3
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import json
import requests

app = FastAPI()

class Employee(BaseModel):
    id: int
    name: str
    role: str
    performance_score: float
    availability: List[str]
    skills: List[str]

class WorkloadData(BaseModel):
    date: str
    department: str
    workload_hours: float
    complexity_score: float

def get_db_connection():
    conn = sqlite3.connect("workforce.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create tables if they don't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            performance_score REAL,
            availability TEXT,
            skills TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS workload_history (
            id INTEGER PRIMARY KEY,
            date TEXT NOT NULL,
            department TEXT NOT NULL,
            workload_hours REAL,
            complexity_score REAL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS schedules (
            id INTEGER PRIMARY KEY,
            date TEXT NOT NULL,
            employee_id INTEGER,
            shift_start TEXT,
            shift_end TEXT,
            department TEXT,
            FOREIGN KEY (employee_id) REFERENCES employees (id)
        )
    """)
    
    conn.commit()
    conn.close()

init_db()

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Workforce Optimizer API"}

@app.post("/employees/")
def create_employee(employee: Employee):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        """
        INSERT INTO employees (name, role, performance_score, availability, skills)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            employee.name,
            employee.role,
            employee.performance_score,
            json.dumps(employee.availability),
            json.dumps(employee.skills)
        )
    )
    
    conn.commit()
    conn.close()
    return {"message": "Employee created successfully"}

@app.post("/workload/")
def record_workload(workload: WorkloadData):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        """
        INSERT INTO workload_history (date, department, workload_hours, complexity_score)
        VALUES (?, ?, ?, ?)
        """,
        (workload.date, workload.department, workload.workload_hours, workload.complexity_score)
    )
    
    conn.commit()
    conn.close()
    return {"message": "Workload data recorded successfully"}

@app.get("/predict/{date}")
def predict_demand(date: str):
    try:
        # Call DeepSeek API to get a prediction
        headers = {
            "Authorization": f"Bearer {"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"}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "deepseek-chat",
            "messages": [{"role": "system", "content": f"Predict customer demand for {date} in a retail store."}],
            "temperature": 0.7
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        response_json = response.json()

        # Extract prediction and convert to number
        prediction_text = response_json["choices"][0]["message"]["content"].strip()
        # Convert text to number (assuming the API returns a number as text)
        try:
            predicted_demand = float(prediction_text)
        except ValueError:
            # If conversion fails, provide a default value
            predicted_demand = 100.0  # Default value for testing

        return {
            "date": date,
            "predicted_demand": predicted_demand,
            "status": "success"
        }

    except Exception as e:
        return {
            "date": date,
            "predicted_demand": 100.0,  # Default value
            "status": "error",
            "error": str(e)
        }

@app.get("/analytics")
def get_analytics():
    conn = get_db_connection()
    
    # Get historical performance metrics
    workload_trends = pd.read_sql_query(
        "SELECT date, AVG(workload_hours) as avg_workload FROM workload_history GROUP BY date",
        conn
    )
    
    employee_performance = pd.read_sql_query(
        "SELECT role, AVG(performance_score) as avg_performance FROM employees GROUP BY role",
        conn
    )
    
    conn.close()
    
    return {
        "workload_trends": workload_trends.to_dict('records'),
        "employee_performance": employee_performance.to_dict('records')
    }
