pipeline {
    agent any

    environment {
        VENV_DIR = "${WORKSPACE}/venv"
        ALLURE_RESULTS = "${WORKSPACE}/allure-results"
        RABBITMQ_CONTAINER = "rabbitmq_test"
    }

    stages {

        stage('Checkout') {
            steps {
                git url: 'https://github.com/aryamolmm/robot-httpbin-assignment.git', branch: 'main'
            }
        }

        stage('Start RabbitMQ') {
            steps {
                sh """
                # Stop any old container
                docker rm -f ${RABBITMQ_CONTAINER} || true

                # Start RabbitMQ container
                docker run -d --name ${RABBITMQ_CONTAINER} -p 5672:5672 -p 15672:15672 rabbitmq:3-management
                echo "RabbitMQ started at http://localhost:15672"
                sleep 10
                """
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

        stage('Stop RabbitMQ') {
            steps {
                sh "docker stop ${RABBITMQ_CONTAINER} || true"
            }
        }
    }

    post {
        always {
            echo "Pipeline finished. Check Allure report for details."
            archiveArtifacts artifacts: 'allure-results/**', allowEmptyArchive: true
            sh "docker rm -f ${RABBITMQ_CONTAINER} || true"
        }
    }
}
