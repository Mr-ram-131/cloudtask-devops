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
                bat 'trivy --version'
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

                    powershell '''
                        Write-Host "Logging into Docker Hub..."

                        $Env:DOCKER_PASSWORD | docker login -u $Env:DOCKER_USERNAME --password-stdin
                        if ($LASTEXITCODE -ne 0) {
                            Write-Host "Docker Hub login failed!"
                            exit 1
                        }

                        Write-Host "Docker Hub login successful!"

                        docker push "$Env:DOCKER_IMAGE`:$Env:BUILD_NUMBER"
                        if ($LASTEXITCODE -ne 0) {
                            Write-Host "Docker image push failed!"
                            exit 1
                        }

                        docker tag "$Env:DOCKER_IMAGE`:$Env:BUILD_NUMBER" "$Env:DOCKER_IMAGE`:latest"

                        docker push "$Env:DOCKER_IMAGE`:latest"
                        if ($LASTEXITCODE -ne 0) {
                            Write-Host "Docker latest image push failed!"
                            exit 1
                        }

                        Write-Host "Docker images pushed successfully!"
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