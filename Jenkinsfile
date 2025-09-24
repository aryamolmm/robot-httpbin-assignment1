pipeline {
    agent any

    environment {
        VENV_DIR = "${WORKSPACE}/venv"
        ALLURE_RESULTS = "${WORKSPACE}/allure-results"
        DOCKER_IMAGE = "aryamolmm/robot-httpbin:latest" // Change to your Docker Hub repo
        DEPLOY_HOST = "your.server.com"
        DEPLOY_USER = "username"
        DEPLOY_DIR = "/path/to/deploy"
    }

    stages {

        stage('Checkout') {
            steps {
                git url: 'https://github.com/aryamolmm/robot-httpbin-assignment.git', branch: 'main'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh """
                python3 -m venv ${VENV_DIR}
                . ${VENV_DIR}/bin/activate

                pip install --upgrade pip
                pip install -r requirements.txt
                """
            }
        }

        stage('Run Robot Framework Tests') {
            steps {
                sh """
                . ${VENV_DIR}/bin/activate
                robot --listener allure_robotframework:${ALLURE_RESULTS} tests/
                """
            }
        }

        stage('Generate Allure Report') {
            steps {
                sh """
                mkdir -p ${ALLURE_RESULTS}
                cp output.xml ${ALLURE_RESULTS}/
                """
                allure([
                    includeProperties: false,
                    results: [[path: "${ALLURE_RESULTS}"]],
                    reportBuildPolicy: 'ALWAYS'
                ])
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                docker build -t ${DOCKER_IMAGE} .
                """
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh """
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                    docker push ${DOCKER_IMAGE}
                    """
                }
            }
        }

        stage('Deploy Docker Container') {
            when {
                branch 'main'
            }
            steps {
                echo "Deploying Docker container to server..."
                sh """
                ssh ${DEPLOY_USER}@${DEPLOY_HOST} '
                    docker pull ${DOCKER_IMAGE} &&
                    docker stop robot-httpbin || true &&
                    docker rm robot-httpbin || true &&
                    docker run -d --name robot-httpbin -p 8080:8080 ${DOCKER_IMAGE}
                '
                """
            }
        }
    }

    post {
        always {
            echo "Pipeline finished. Check Allure report for details."
            archiveArtifacts artifacts: 'allure-results/**', allowEmptyArchive: true
        }
    }
}
