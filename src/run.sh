#!/bin/bash

uvicorn timeout.entrypoints.api:app --host 0.0.0.0 --port 80 --reload
