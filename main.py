from session import Session
from components.secret_manager import SecretManager
from components.sender import Sender
from components.receiver import Receiver
from pathlib import Path
import click
import os

@click.command()
@click.option(
    "--profile", 
    type=click.Path(exists=True, dir_okay=True, writable=True),
    help="Path to the profile directory which holds the private key"
)
def main(profile: str):
    shared_folder_path = Path("shared")
    shared_folder_path.mkdir(parents=True, exist_ok=True)

    # user_name = click.prompt("Enter a user name for this session")
    # user_name = user_name.lower().strip()

    profile = os.path.normpath(profile)
    shared = os.path.normpath(shared_folder_path)
    session = Session(shared_path=shared, profile_path=profile)
    click.echo(f"Profile path set to: {session.profile_path}")
    click.echo(f"Shared path set to: {session.shared_path}")
    # Map to hold action instances
    components = {}
    try:
        while True:
            click.echo(
                "\nMenu:\n"
                "1. Generate Keys\n"
                "2. Write Encrypted Message\n"
                "3. Read Encrypted Message\n"
            )
            cmd = click.prompt("Enter an action number (type 'q' to quit)")
            cmd = cmd.lower().strip()
            if cmd == "q":
                raise SystemExit
            
            if cmd == "1":
                click.echo("Generating keys...")
                # Initialize SecretManager action if not already done
                if not components.get("secret_manager"):
                    components["secret_manager"] = SecretManager(session)
                
                # Call the generate wrapper method to handle key pair generation
                components["secret_manager"].generate_pair()
            elif cmd == "2":
                click.echo("Writing encrypted message...")
                
                message_file = click.prompt("Enter path to message file")
                receiver_name = click.prompt("Enter receiver's profile name")
                
                # Initialize sender
                components["sender"] = Sender(session)
                components["sender"].send_message(message_file, receiver_name)
                
            elif cmd == "3":
                click.echo("Reading encrypted message...")
                
                # Initialize receiver
                if not components.get("receiver"):
                    components["receiver"] = Receiver(session)
                
                components["receiver"].receive_message()
                
    except (KeyboardInterrupt, SystemExit):
        click.echo("\nExiting application.")

if __name__ == "__main__":
    main()