# Jenkins CI/CD Pipeline with Docker

A small Python service used to demonstrate a Jenkins pipeline from source checkout through unit tests, Docker image build and container smoke test.

## Pipeline stages
1. Checkout source
2. Create Python virtual environment and install dependencies
3. Run unit tests
4. Build a Docker image
5. Start the container and call its health endpoint
6. Stop and remove the test container

The pipeline deliberately does not push to a registry or deploy to a live environment. Add credentials and an approved deployment target only after adapting it to your environment.

## Run locally
```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
pytest -q
docker build -t sample-service:local .
docker run --rm -p 8080:8080 sample-service:local
curl http://localhost:8080/health
```

## Jenkins prerequisites
- Jenkins with Pipeline support
- Agent with Docker Engine access
- Git and Python 3.11 installed on the agent

## Security notes
Do not mount the Docker socket into untrusted jobs. Use isolated agents, pin production image versions, scan images, and store registry credentials in Jenkins Credentials rather than in the Jenkinsfile.

## Status
Pipeline and sample app are provided as a repository example. A successful run on a Jenkins controller is not claimed.
