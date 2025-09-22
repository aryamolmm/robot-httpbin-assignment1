pipeline {
    agent any

    environment {
        VENV_DIR = "${WORKSPACE}/venv"
        ALLURE_RESULTS = "${WORKSPACE}/allure-results"
    }

    stages {

        stage('Checkout') {
            steps {
                // Checkout your Git repository
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
        robot --output output.xml tests/
        """
    }
}

        stage('Generate Allure Report') {
            steps {
                sh """
                # Create results directory
                mkdir -p ${ALLURE_RESULTS}

                # Copy Robot Framework output.xml to Allure results
                cp output.xml ${ALLURE_RESULTS}/
                """

                // Generate Allure report using Jenkins plugin
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
