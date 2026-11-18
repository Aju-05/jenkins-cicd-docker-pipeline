pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        IMAGE_NAME = "sample-service:${BUILD_NUMBER}"
        CONTAINER_NAME = "sample-service-ci-${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install and test') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pytest -q
                '''
            }
        }

        stage('Build image') {
            steps {
                sh 'docker build --pull -t "$IMAGE_NAME" .'
            }
        }

        stage('Container smoke test') {
            steps {
                sh '''
                    set -eu
                    docker run -d --name "$CONTAINER_NAME" -p 18080:8080 "$IMAGE_NAME"
                    trap 'docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true' EXIT
                    for attempt in $(seq 1 15); do
                      if curl --fail http://127.0.0.1:18080/health; then
                        exit 0
                      fi
                      sleep 2
                    done
                    echo "Health endpoint did not become ready"
                    exit 1
                '''
            }
        }
    }

    post {
        always {
            sh 'docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true'
            sh 'docker image rm "$IMAGE_NAME" >/dev/null 2>&1 || true'
        }
    }
}
