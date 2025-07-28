# utils/config.py
import os, pathlib

BASE = pathlib.Path(__file__).resolve().parent.parent
MODEL_NAME = os.getenv("MODEL_NAME", "intfloat/e5-base-v2")
HF_HOME    = os.getenv("HF_HOME", str(BASE/"models"/"e5-base-v2"))
