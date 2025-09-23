# robot-httpbin-assignment

A Python project using Robot Framework for automated API and RabbitMQ testing.

## Setup

1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd robot-httpbin-assignment
   ```

2. **Create a virtual environment (recommended):**
   ```sh
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

## Running Tests

Run all Robot Framework tests in the `tests` directory:
```sh
robot tests/
```

Or use the provided shell script (if on Unix):
```sh
sh robot_run.sh
```

## Generating and Viewing Reports

After running tests, Robot Framework will generate `report.html` and `log.html` in the project directory.

- **View report:** Open `report.html` in your browser.
- **View log:** Open `log.html` in your browser.

If you use Allure for advanced reporting:
1. Generate Allure results (already in `output/allure/`).
2. Generate the Allure report:
   ```sh
   allure generate output/allure/ -o output/allure-report/ --clean
   ```
3. Open the Allure report:
   ```sh
   allure open output/allure-report/
   ```

## Notes

- Ensure all required services (e.g., httpbin, RabbitMQ) are running if your tests depend on them.
- Update `requirements.txt` as needed for your dependencies.
- For Docker-based setup, see `docker-compose.yml` and `dockerfile`.
