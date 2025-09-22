pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/aryamolmm/robot-httpbin-assignment.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'python3 -m pip install --upgrade pip'
                sh 'python3 -m pip install -r requirements.txt'
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
