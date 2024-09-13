import subprocess
import time
import os

def start_minikube():
    print("Starting Minikube...")
    subprocess.run(["minikube", "start"], check=True)
    print("Minikube started.")

def deploy_helm_chart():
    print("Deploying Helm chart...")

    # Dynamically get the absolute path to the Helm chart from the script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(script_dir)
    helm_chart_path = os.path.join(script_dir, "..", "helm", "my-pods-chart")
    print(helm_chart_path)
    # Normalize the path for Windows
    helm_chart_path = os.path.normpath(helm_chart_path)
    print(helm_chart_path)
    # Check if the release already exists
    try:
        subprocess.run(["helm", "status", "my-pods"], check=True)
        print("Release 'my-pods' exists, uninstalling...")
        subprocess.run(["helm", "uninstall", "my-pods"], check=True)
    except subprocess.CalledProcessError:
        print("Release 'my-pods' does not exist, proceeding with install...")

    # Install the Helm chart
    subprocess.run(["helm", "install", "my-pods", helm_chart_path], check=True)
    print("Helm chart deployed.")

def run_spring_boot_app():
    print("Running Spring Boot application...")

    # Compute the root directory of the project from the script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(script_dir)
    project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
    print(project_root)

    # Path to mvnw.cmd in the project root
    mvnw_cmd_path = os.path.join(project_root, "mvnw.cmd")
    print(mvnw_cmd_path)

    # Check if the file exists
    if not os.path.isfile(mvnw_cmd_path):
        raise FileNotFoundError(f"The file '{mvnw_cmd_path}' does not exist.")

    # Run the Maven command with the correct working directory
    subprocess.Popen(["mvnw.cmd", "spring-boot:run"], cwd=project_root, shell=True)
    print("Spring Boot application is running.")

if __name__ == "__main__":
    try:
        # Start Minikube
        start_minikube()

        # Deploy Helm chart to Minikube
        deploy_helm_chart()

        # Give some time for Helm chart to deploy
        time.sleep(10)

        # Run the Spring Boot application
        run_spring_boot_app()

        # Keep the script alive until user terminates it
        while True:
            time.sleep(60)

    except subprocess.CalledProcessError as e:
        print(f"Error during execution: {e}")
    except FileNotFoundError as e:
        print(e)
