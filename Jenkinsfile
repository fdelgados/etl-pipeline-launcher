pipeline {
    agent any

    environment {
        ENVIRONMENT = "test"
        FLASK_ENV = "test"
    }

    stages {
        stage("Prepare") {
            steps {
                sh "rm /usr/local/bin/docker-compose"
                sh "curl -L https://github.com/docker/compose/releases/download/1.29.2/docker-compose-`uname -s`-`uname -m` > docker-compose"
                sh "chmod +x docker-compose"
                sh "sudo mv docker-compose /usr/local/bin"
                sh "docker --version"
            }
        }

        stage('Clone repository') {
            steps {
                checkout scm
            }
        }

        stage("Run unit tests") {
            steps {
                sh "docker-compose -f ./docker/docker-compose.yml build --build-arg PYTHON_DEPS=requirements-devel.txt application"
                sh "docker-compose -f ./docker/docker-compose.yml run --entrypoint=\"pytest /opt/code/tests/unit\" application"
            }
        }

        stage("Run static analysis") {
            steps {
                sh "docker-compose -f ./docker/docker-compose.yml build --build-arg PYTHON_DEPS=requirements-devel.txt static-analysis"
                sh "docker-compose -f ./docker/docker-compose.yml run static-analysis"
            }
        }

        stage("Tag and push build") {
            steps {
                sh "docker-compose -f ./docker/docker-compose.yml build application"
                sh "docker tag nlp-application:latest fdelgados/nlp-application:$TRAVIS_BRANCH"
            }
        }
    }
}
