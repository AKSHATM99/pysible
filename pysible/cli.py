import typer
import shutil
import os
from dotenv import load_dotenv
import time

app = typer.Typer()

def starter(project_name) -> bool:
    try:
        from .database.redis_client import redis_client
        print("Loading .env \U0001F600")
        print("Loaded .env to system \u2713")
        print("Checking Redis Connection \U0001F600")
        time.sleep(1)
        if redis_client.ping()!=None:
            print("✅ Redis connection successful!")
            time.sleep(1)
            # Enable Append Only File
            redis_client.config_set("appendonly", "yes")
            redis_client.config_set("appendfsync", "everysec")
            print("AOF persistence enabled ✅")
            time.sleep(1)
            return True
        if redis_client.ping()==None:
            print("⚠️ Redis connection failed.")
            return False
    except Exception as e:
        print("Connection Failed With Redis")
        shutil.rmtree(project_name)
        raise e

@app.command()
def action():
    try:
        project_name = typer.prompt("Project name:->")
        is_redis = typer.prompt("Redis is running now? (yes/no):->")
        if is_redis=="yes":
            redis_host = typer.prompt("Host of Redis (e.g 'localhost' if running locally):->")
            redis_port = typer.prompt("Port of Redis:->")
            redis_db_no = typer.prompt("Redis DB Number (e.g '0', '1'):->")
            want_dummy_data = typer.prompt("Want to load dummy data for testing ? ( yes / no ):->")
            if want_dummy_data=="yes":
                from .database.db import Data
                Data.load_data()
                print("Loading default user & roles... ✅")
                time.sleep(1)
            # Create project folder
            os.makedirs(project_name, exist_ok=True)
            # Create .env file
            env_content = f"""
        REDIS_HOST={redis_host}
        REDIS_PORT={redis_port}
        REDIS_DB_NUMBER={redis_db_no}
                            """
            print(redis_db_no,redis_host,redis_port)
            with open(f"{project_name}/.env", "w") as f:
                f.write(env_content)
            # ✅ explicitly load the .env file you just created
            env_path = os.path.join(project_name, ".env")
            load_dotenv(dotenv_path=env_path)
            """
            Check Redis connection
            """
            starter(project_name)
            """
            Creating Required Files & Folders
            """
            # Define folders and files
            folders = ["static", "src", "tests"]
            files = [".gitignore", "requirements.txt", "README.md", "LICENSE"]
            # Create folders
            print(f"📂 Creating Project Structure for: {project_name}")
            time.sleep(1)
            for folder in folders:
                folder_path = os.path.join(project_name, folder)
                os.makedirs(folder_path, exist_ok=True)
            # Create files
            for file in files:
                file_path = os.path.join(project_name, file)
                if not os.path.exists(file_path):  # avoid overwriting
                    with open(file_path, "w") as f:
                        if file == "README.md":
                            f.write("# Project Title\n\nProject description goes here.\n")
                        elif file == "requirements.txt":
                            f.write("# Add project dependencies here\n")
                        elif file == ".gitignore":
                            f.write("__pycache__/\n*.pyc\n.env\n")
                else:
                    print(f"⚠️ File already exists: {file_path}")
            typer.echo(f"✅ Project {project_name} created with .env file \u2764 \U0001F680")
        elif is_redis=="no":
            print("Pysible requires running Redis instance in system to work...⚠️\nPlease run Redis first...⚠️")
    except Exception as e:
        return e

def main():
    app()
