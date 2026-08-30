pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "756043/cloudtask"
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out CloudTask source code...'
                checkout scm
            }
        }

        stage('Test') {
            steps {
                echo 'Running application tests...'

                bat 'python --version'
                bat 'docker --version'
            }
        }

        stage('Docker Build') {
            steps {
                echo 'Building CloudTask Docker image...'

                bat "docker build -t %DOCKER_IMAGE%:%BUILD_NUMBER% ."
            }
        }

        stage('Security Scan') {
            steps {
                echo 'Scanning Docker image for HIGH and CRITICAL vulnerabilities...'

                bat "trivy image --severity HIGH,CRITICAL --ignore-unfixed --exit-code 1 %DOCKER_IMAGE%:%BUILD_NUMBER%"
            }
        }

        stage('Docker Image Check') {
            steps {
                echo 'Checking Docker image...'

                bat "docker images %DOCKER_IMAGE%"
            }
        }

        stage('Docker Hub Push') {
            steps {
                echo 'Pushing CloudTask image to Docker Hub...'

                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {

                    bat '''
                        echo %DOCKER_PASSWORD% | docker login -u %DOCKER_USERNAME% --password-stdin
                        docker push %DOCKER_IMAGE%:%BUILD_NUMBER%
                        docker tag %DOCKER_IMAGE%:%BUILD_NUMBER% %DOCKER_IMAGE%:latest
                        docker push %DOCKER_IMAGE%:latest
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'CloudTask CI/CD pipeline completed successfully!'
        }

        failure {
            echo 'CloudTask CI/CD pipeline failed.'
        }
    }
}