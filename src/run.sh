#!/bin/bash

uvicorn timeout.entrypoints.api:app --reload --host 0.0.0.0 --port 80
