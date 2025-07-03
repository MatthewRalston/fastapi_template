#!/bin/bash

npm run build:css

uvicorn app.main:app --reload
