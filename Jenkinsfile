pipeline {
    agent any

    environment {
        DOCKER_IMAGE = '756043/cloudtask'
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
                echo 'Checking required tools...'
                bat 'python --version'
                bat 'docker --version'
                bat 'trivy --version'
            }
        }

        stage('Docker Build') {
            steps {
                echo 'Building CloudTask Docker image...'

                bat 'docker build --no-cache -t %DOCKER_IMAGE%:%BUILD_NUMBER% .'
            }
        }

        stage('Security Scan') {
            steps {
                echo 'Scanning Docker image for HIGH and CRITICAL vulnerabilities...'

                bat 'trivy image --severity HIGH,CRITICAL --ignore-unfixed --exit-code 1 --scanners vuln %DOCKER_IMAGE%:%BUILD_NUMBER%'
            }
        }

        stage('Docker Login') {
            steps {
                echo 'Logging in to Docker Hub...'

                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    bat 'echo %DOCKER_PASS%| docker login -u %DOCKER_USER% --password-stdin'
                }
            }
        }

        stage('Docker Push') {
            steps {
                echo 'Pushing CloudTask image to Docker Hub...'

                bat 'docker push %DOCKER_IMAGE%:%BUILD_NUMBER%'
            }
        }

        stage('Docker Image Check') {
            steps {
                echo 'Checking Docker image...'

                bat 'docker images %DOCKER_IMAGE%'
            }
        }
    }

    post {
        success {
            echo 'CloudTask CI/CD pipeline completed successfully!'
            echo 'Docker image pushed successfully to Docker Hub.'
        }

        failure {
            echo 'CloudTask CI/CD pipeline failed.'
        }

        always {
            bat 'docker logout'
        }
    }
}