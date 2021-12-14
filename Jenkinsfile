node {
     def app

     stage('Clone repository') {
         checkout scm
     }

     stage('Build image') {
         def dockerfile = "docker/Dockerfile"
         app = docker.build("fdelgados/nlp-application", "--build-arg PYTHON_DEPS=requirements-devel.txt -f ${dockerfile} ./")
     }

     stage('Run Unit Tests') {
         app.inside {
             sh 'pytest /opt/code/tests/unit'
         }
     }

     stage('Run Static Analysis') {
        app.inside {
            sh 'flake8 --ignore=E203,W503 .'
        }
     }

     stage('Push image') {
         docker.withRegistry('https://registry.hub.docker.com', 'd8c18dc6-3da8-49c6-9589-ca328cc695b8') {
             app.push("${env.BUILD_NUMBER}")
             app.push("latest")
         }
     }
 }
