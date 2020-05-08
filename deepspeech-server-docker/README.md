# Deepspeech Server Docker

This repository contains a Dockerfile to set up a DeepSpeech server

# Build Image
 ./build_images.sh

# To Start Container
 ./start_container.sh

# Docker run command
 docker run -d -p 8000:4242 deepspeech-server-docker:latest

# Curl - To test speech to text via API
 curl -v  --header "Content-Type:application/octet-stream" -X POST --data-binary @yes.wav http://localhost:8000/transcribe

# Response 
 {"words": [{"word": "yes", "start_time ": 0.0, "duration": 2.26}], "confidence": -13.221184626582627}
