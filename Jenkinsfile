pipeline {
    agent any

    environment {
        IMAGE_NAME = "joelsp123/projecthclsdb"
        TAG = "latest"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/devjr8585-gif/ProjectHCLSDB.git'
            }
        }

        stage('Build Docker Image') {
    steps {
        script {
            def image = "${env.IMAGE_NAME}:${env.TAG}"
            sh """
            echo "Building Docker image: ${image}"
            docker build -t ${image} .
            """
        }
    }
}

        stage('Login to DockerHub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'docker-cred',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh """
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                    """
                }
            }
        }

        stage('Push Image') {
    steps {
        script {
            def image = "${env.IMAGE_NAME}:${env.TAG}"
            sh "docker push ${image}"
        }
    }
}
    

