from session import Session
from components.secret_manager import SecretManager
from components.sender import Sender
from components.receiver import Receiver
from pathlib import Path
import click
import os

@click.command()
def main():
    shared_folder_path = Path("shared")
    shared_folder_path.mkdir(parents=True, exist_ok=True)

    user_name = click.prompt("Enter a username for this session")
    user_profile_path = Path(f"profiles/{user_name.lower().strip()}")
    user_profile_path.mkdir(parents=True, exist_ok=True)

    shared = os.path.normpath(shared_folder_path)
    session = Session(shared_path=shared, profile_path=user_profile_path)
    click.echo(f"Profile path set to: {session.profile_path}")
    click.echo(f"Shared path set to: {session.shared_path}")

    click.echo("Generating key pairs...")
    # Handle key pair generation for the current session
    SecretManager(session).generate_pair()


    # Map to hold action instances
    components = {}
    try:
        while True:
            click.echo(
                "\nMenu:\n"
                "1. Write Encrypted Message\n"
                "2. Read Encrypted Message\n"
            )
            cmd = click.prompt("Enter an action number (type 'q' to quit)")
            cmd = cmd.lower().strip()
            if cmd == "q":
                raise SystemExit
            elif cmd == "1":
                click.echo("Writing encrypted message...")
                
                message_file = click.prompt("Enter path to message file")
                receiver_name = click.prompt("Enter receiver's profile name")
                
                # Initialize sender
                components["sender"] = Sender(session)
                components["sender"].send_message(message_file, receiver_name)
                
            elif cmd == "2":
                click.echo("Reading encrypted message...")
                
                # Initialize receiver
                if not components.get("receiver"):
                    components["receiver"] = Receiver(session)
                
                components["receiver"].receive_message()
                
    except (KeyboardInterrupt, SystemExit):
        click.echo("\nExiting application.")

if __name__ == "__main__":
    main()