pipeline {
    agent any

    environment {
        VENV_DIR = "${WORKSPACE}/venv"
        ALLURE_RESULTS = "${WORKSPACE}/allure-results"
        RABBITMQ_HOST = "localhost"
        RABBITMQ_PORT = "5672"
    }

    stages {

        stage('Checkout') {
            steps {
                // Checkout your Git repository
                git url: 'https://github.com/aryamolmm/robot-httpbin-assignment.git', branch: 'main'
            }
        }

        stage('Start RabbitMQ') {
            steps {
                sh """
                docker run -d --rm \
                    --name rabbitmq \
                    -p 5672:5672 -p 15672:15672 \
                    -e RABBITMQ_DEFAULT_USER=guest \
                    -e RABBITMQ_DEFAULT_PASS=guest \
                    rabbitmq:3-management
                """
                // Give RabbitMQ a few seconds to initialize
                sleep 10
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
                sh "docker stop rabbitmq || true"
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
