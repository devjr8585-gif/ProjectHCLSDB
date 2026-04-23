pipeline {
    agent any

    environment {
        IMAGE_NAME = "joel123/projecthclsdb"
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
        sh """
        echo "Building Docker image: ${IMAGE_NAME}:${TAG}"
        docker build -t ${IMAGE_NAME}:${TAG} .
        """
    }
}

        stage('Login to DockerHub') {
    steps {
        withCredentials([usernamePassword(
            credentialsId: 'docker-cred',
            usernameVariable: 'DOCKER_USER',
            passwordVariable: 'DOCKER_PASS'
        )]) {
            sh '''
                echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
            '''
        }
    }
}

        stage('Push Image') {
            steps {
                sh 'docker push $IMAGE_NAME:$TAG'
            }
        }
    }
}
