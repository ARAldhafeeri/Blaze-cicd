
import subprocess
from blaze_cicd import blaze_logger

def check_namespace_exists(namespace_name):
    try:
        out = subprocess.check_output(["kubectl", "get", "ns", "-A"])
        out_str = out.decode('utf-8')
        lines = out_str.strip().split('\n')
        for line in lines[1:]:  # Skip the header line
            if namespace_name in line:
                blaze_logger.info(f"Namespace '{namespace_name}' exists.")
                return True
        
        blaze_logger.info(f"Namespace '{namespace_name}' does not exist.")
        return False

    except subprocess.CalledProcessError as e:
        blaze_logger.info(f"Error executing command: {e}")
        return False
    
def kubectl_create_project_namespace(namespace: str):
    """Create a namespace using kubectl in the current configured context, if it exists, skip the creation process"""
    try:
        if check_namespace_exists(namespace):
            return 
        subprocess.run(["kubectl", "create", "namespace", namespace], check=True)
        blaze_logger.info("Namespace created successfully.")
        
    except subprocess.CalledProcessError as e:
        blaze_logger.error(f"Failed to create namespace: {e}")
        return
    