#!/bin/bash

uvicorn src.entrypoints.api:app --reload --host 0.0.0.0 --port 80
