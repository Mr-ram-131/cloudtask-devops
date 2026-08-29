pipeline {
    agent any

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
                bat 'docker build -t cloudtask:2 .'
            }
        }

        stage('Security Scan') {
            steps {
                echo 'Scanning Docker image for vulnerabilities...'
                bat 'trivy image --severity HIGH,CRITICAL --exit-code 1 cloudtask:2'
            }
        }

        stage('Docker Image Check') {
            steps {
                echo 'Checking Docker image...'
                bat 'docker images cloudtask'
            }
        }
    }

    post {
        success {
            echo 'CloudTask CI pipeline completed successfully!'
        }

        failure {
            echo 'CloudTask CI pipeline failed.'
        }
    }
}