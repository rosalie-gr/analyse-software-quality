import subprocess
import sys

class Dependencies:

    def install_dependencies():

        dependencies = ["bcrypt==4.1.3", "cryptography==42.0.8"]

        # Install dependencies from the requirements.txt file
        for item in dependencies:
            try:
                subprocess.call([sys.executable, '-m', 'pip', 'install', item])
                print(f"Installed {item}")
            except Exception as e:
                print(f"Error installing {item}: {e}")
                
    def uninstall_dependencies():
        dependencies = ["bcrypt", "cryptography"]

        # Uninstall dependencies
        for item in dependencies:
            try:
                subprocess.call([sys.executable, '-m', 'pip', 'uninstall', item, '-y'])
                print(f"Uninstalled {item}")
            except Exception as e:
                print(f"Error uninstalling {item}: {e}")
