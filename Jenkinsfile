pipeline {
    agent any

    environment {
        ENVIRONMENT = "test"
        FLASK_ENV = "test"
    }

    stages {
        stage("Prepare") {
            steps {
                sh "docker --version"
                sh "docker-compose version"
            }
        }

        stage('Clone repository') {
            steps {
                checkout scm
            }
        }

        stage("Run unit tests") {
            steps {
                sh "docker-compose -f ${env.WORKSPACE}/docker/docker-compose.yml build --build-arg PYTHON_DEPS=requirements-devel.txt"
                sh "docker-compose -f ${env.WORKSPACE}/docker/docker-compose.yml run --entrypoint=\"pytest /opt/code/tests/unit\" application"
            }
        }

        stage("Run static analysis") {
            steps {
                sh "docker-compose -f ${env.WORKSPACE}/docker/docker-compose.yml build --build-arg PYTHON_DEPS=requirements-devel.txt static-analysis"
                sh "docker-compose -f ${env.WORKSPACE}/docker/docker-compose.yml run static-analysis"
            }
        }

        stage("Tag and push build") {
            steps {
                sh "docker-compose -f ${env.WORKSPACE}/docker/docker-compose.yml build application"
                sh "docker tag nlp-application:latest fdelgados/nlp-application:master"
            }
        }
    }
}
