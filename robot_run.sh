#!/bin/bash
set -e  # exit if any command fails

# Clean previous results
rm -rf ./allure-results ./allure-report output
mkdir -p output

echo "Running Robot Framework tests..."
robot --outputdir output --listener allure_robotframework;./allure-results tests/

echo "Generating Allure report..."
allure generate ./allure-results --clean -o ./allure-report

echo "Allure report generated at ./allure-report"
echo "Done!"
