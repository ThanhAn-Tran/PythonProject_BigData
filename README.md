# Project Deployment Guide

## Prerequisites
Before deploying this project, ensure that you have the following installed on your system:
- **Docker Desktop Personal v27.3.1**
- **PyCharm 2024.3 (Community Edition)**
- **Windows 11**

## Step 1: Set Up Apache Cassandra
1. Open **Docker Desktop** and make sure it is running.
2. Open a terminal or command prompt and execute the following command to pull the Cassandra image:
   ```sh
   docker pull antranthanh/my-cassandra
   ```
3. Run the Cassandra container with:
   ```sh
   docker run --name my-cassandra -p 9042:9042 -d antranthanh/my-cassandra
   ```
4. Verify that the container is running:
   ```sh
   docker ps
   ```
   You should see `my-cassandra` in the list of running containers.

## Step 2: Configure PyCharm
1. Open **PyCharm 2024.3 (Community Edition)**.
2. Install the following **Non-Bundled Plugins**:
   - Docker (243.21565.204)
   - com.intellij.ml.llm (243.21565.247)
   - ru.adelf.idea.dotenv (2024.3)
   - net.ashald.envfile (3.4.2)
   - com.github.copilot (1.5.32-242)
3. Configure the Python Interpreter:
   - Navigate to **File > Settings > Project > Python Interpreter**.
   - Set up a virtual environment or use a system interpreter.

## Step 3: Install Dependencies
1. Navigate to the project directory:
   ```sh
   cd /path/to/your/project
   ```
2. Create a virtual environment (optional but recommended):
   ```sh
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate     # On Windows
   ```
3. Install required dependencies from `requirements.txt`:
   ```sh
   pip install -r requirements.txt
   ```

## Step 4: Connect to Apache Cassandra
1. Ensure the Cassandra container is running:
   ```sh
   docker ps
   ```
2. Use **CQLSH** (Cassandra Query Language Shell) to verify the connection:
   ```sh
   docker exec -it my-cassandra cqlsh 127.0.0.1 9042
   ```
3. If the connection is successful, proceed with the application setup.

## Step 5: Run the Application
1. Open PyCharm and navigate to your main script.
2. Run the script using the configured Python interpreter:
   ```sh
   python web_interface.py
   ```
3. Ensure that the application successfully connects to Cassandra and runs as expected.

## Step 6: Troubleshooting
- If Cassandra is not running, restart the container:
  ```sh
  docker restart my-cassandra
  ```
- If dependencies fail to install, ensure you have the correct Python version and try reinstalling:
  ```sh
  pip install --upgrade pip
  pip install -r requirements.txt
  ```
- If PyCharm does not detect the interpreter, reconfigure the Python environment in settings.

## Conclusion
Your system is now deployed and ready for use. Ensure all configurations are correctly set up for a smooth operation.

---

**Author:** Trần Thành An  
**License:** MIT  
**GitHub:** [ThanhAn-Tran](https://github.com/ThanhAn-Tran)

