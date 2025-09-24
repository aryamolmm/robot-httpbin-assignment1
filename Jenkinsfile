pipeline {
    agent any

    environment {
        VENV_DIR = "${WORKSPACE}/venv"
        ALLURE_RESULTS = "${WORKSPACE}/allure-results"
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
    }

    post {
        always {
            echo "Pipeline finished. Check Allure report for details."
            archiveArtifacts artifacts: 'allure-results/**', allowEmptyArchive: true
        }
    }
}
