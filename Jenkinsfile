stage('Install Dependencies') {
    steps {
        sh '''
        python3 -m venv venv
        source venv/bin/activate
        pip install --upgrade pip
        pip install -r requirements.txt
        '''
    }
}

stage('Run Robot Framework Tests') {
    steps {
        sh '''
        source venv/bin/activate
        robot --output output.xml tests/
        '''
    }
}

stage('Generate Allure Report') {
    steps {
        sh '''
        source venv/bin/activate
        mkdir -p allure-results
        cp output.xml allure-results/
        '''
    }
    post {
        always {
            allure([
                includeProperties: false,
                results: [[path: 'allure-results']]
            ])
        }
    }
}
