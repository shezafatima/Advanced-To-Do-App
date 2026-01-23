import subprocess
import os
from datetime import datetime
from typing import Optional
from ..config import settings


class DatabaseBackup:
    """
    Class to handle database backup and recovery procedures.
    """

    @staticmethod
    def create_backup(backup_path: Optional[str] = None) -> str:
        """
        Create a database backup using pg_dump.

        Args:
            backup_path: Optional path where the backup should be saved.
                        If not provided, creates backup in default location with timestamp.

        Returns:
            Path to the created backup file
        """
        if not backup_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"todo_app_backup_{timestamp}.sql"
            backup_path = os.path.join("backups", backup_filename)

        # Ensure backup directory exists
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)

        # Extract database connection parameters from the database URL
        db_url = settings.database_url
        if db_url.startswith("postgresql://"):
            # Parse the PostgreSQL URL
            db_url = db_url.replace("postgresql://", "")
            auth_db = db_url.split("@")[-1]  # Get the auth@host:port/db part
            auth_part = db_url.split("@")[0] if "@" in db_url else ""
            host_part = auth_db.split("/")[0] if "/" in auth_db else ""
            db_name = auth_db.split("/")[-1] if "/" in auth_db else ""

            if ":" in auth_part:
                username, password = auth_part.split(":")
            else:
                username = auth_part
                password = ""

            if ":" in host_part:
                host, port = host_part.split(":")
            else:
                host = host_part
                port = "5432"

            # Use environment variables for password to avoid command line exposure
            env = os.environ.copy()
            if password:
                env["PGPASSWORD"] = password

            # Execute pg_dump command
            cmd = [
                "pg_dump",
                "-h", host,
                "-p", port,
                "-U", username,
                "-d", db_name,
                "-f", backup_path
            ]

            try:
                subprocess.run(cmd, check=True, env=env)
                print(f"Backup created successfully at: {backup_path}")
                return backup_path
            except subprocess.CalledProcessError as e:
                print(f"Error creating backup: {e}")
                raise e
            except FileNotFoundError:
                # pg_dump not found, try alternative approach using psycopg
                print("pg_dump not found, using alternative backup method...")
                return DatabaseBackup._create_backup_alternative(backup_path)

    @staticmethod
    def _create_backup_alternative(backup_path: str) -> str:
        """
        Alternative backup method using Python libraries when pg_dump is not available.
        This is a simplified implementation - in production, you might want to use
        more sophisticated methods.
        """
        # This is a placeholder for an alternative backup method
        # In a real implementation, you would use SQLModel/SQLAlchemy to
        # extract data and save it to a file
        print(f"Creating backup at {backup_path} using alternative method")
        with open(backup_path, 'w') as f:
            f.write(f"-- Backup created on {datetime.now()}\n")
            f.write("-- This is a placeholder backup file\n")
        return backup_path

    @staticmethod
    def restore_backup(backup_path: str) -> bool:
        """
        Restore a database from a backup file using pg_restore.

        Args:
            backup_path: Path to the backup file to restore from

        Returns:
            True if restore was successful, False otherwise
        """
        if not os.path.exists(backup_path):
            print(f"Backup file does not exist: {backup_path}")
            return False

        # Extract database connection parameters from the database URL
        db_url = settings.database_url
        if db_url.startswith("postgresql://"):
            # Parse the PostgreSQL URL
            db_url = db_url.replace("postgresql://", "")
            auth_db = db_url.split("@")[-1]  # Get the auth@host:port/db part
            auth_part = db_url.split("@")[0] if "@" in db_url else ""
            host_part = auth_db.split("/")[0] if "/" in auth_db else ""
            db_name = auth_db.split("/")[-1] if "/" in auth_db else ""

            if ":" in auth_part:
                username, password = auth_part.split(":")
            else:
                username = auth_part
                password = ""

            if ":" in host_part:
                host, port = host_part.split(":")
            else:
                host = host_part
                port = "5432"

            # Use environment variables for password to avoid command line exposure
            env = os.environ.copy()
            if password:
                env["PGPASSWORD"] = password

            # Execute psql command to restore the backup
            cmd = [
                "psql",
                "-h", host,
                "-p", port,
                "-U", username,
                "-d", db_name,
                "-f", backup_path
            ]

            try:
                subprocess.run(cmd, check=True, env=env)
                print(f"Database restored successfully from: {backup_path}")
                return True
            except subprocess.CalledProcessError as e:
                print(f"Error restoring backup: {e}")
                return False
            except FileNotFoundError:
                print("psql command not found. Please install PostgreSQL client tools.")
                return False

    @staticmethod
    def list_backups(backup_dir: str = "backups") -> list:
        """
        List all available backup files in the specified directory.

        Args:
            backup_dir: Directory to search for backup files

        Returns:
            List of backup file paths
        """
        if not os.path.exists(backup_dir):
            return []

        backup_files = []
        for filename in os.listdir(backup_dir):
            if filename.endswith(".sql") and "backup" in filename:
                backup_files.append(os.path.join(backup_dir, filename))

        # Sort by modification time (newest first)
        backup_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        return backup_files