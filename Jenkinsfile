pipeline {
    agent any

    tools {
        python 'Python3'   // Make sure Python is configured in Jenkins global tools
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/aryamolmm/robot-httpbin-assignment.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install --upgrade pip'
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Robot Framework Tests') {
            steps {
                sh 'robot --output output.xml tests/'
            }
        }

        stage('Generate Allure Report') {
            steps {
                sh 'allure generate output.xml --clean -o allure-report'
            }
        }
    }

    post {
        always {
            allure([
                includeProperties: false,
                jdk: '',
                results: [[path: 'allure-report']]
            ])
        }
    }
}
