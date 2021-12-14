node {
     def app

     stage('Clone repository') {
         /* Let's make sure we have the repository cloned to our workspace */

         checkout scm
     }

     stage('Build image') {
         /* This builds the actual image; synonymous to
          * docker build on the command line */

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
         /* Finally, we'll push the image with two tags:
          * First, the incremental build number from Jenkins
          * Second, the 'latest' tag.
          * Pushing multiple tags is cheap, as all the layers are reused. */
         docker.withRegistry('https://registry.hub.docker.com', 'd8c18dc6-3da8-49c6-9589-ca328cc695b8') {
             app.push("${env.BUILD_NUMBER}")
             app.push("latest")
         }
     }
 }
