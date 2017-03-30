#!/bin/bash
docker stop tlsmd
docker rm tlsmd
docker run -d -p 127.0.0.1:9193:9193 --name=tlsmd tlsmd:latest
