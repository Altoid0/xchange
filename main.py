from session import Session
from actions.generate import Generate
import click
import os

@click.command()
@click.option(
    "--profile", 
    type=click.Path(exists=True, dir_okay=True, writable=True),
    help="Path to the profile directory which holds the private key"
)
@click.option(
    "--shared",
    default=".",
    type=click.Path(exists=True, dir_okay=True, writable=True),
    help="Path to the shared directory which holds the public keys"
)
def main(profile: str, shared: str):
    profile = os.path.normpath(profile)
    shared = os.path.normpath(shared)
    session = Session(shared_path=shared, profile_path=profile)

    click.echo(f"Profile path set to: {session.profile_path}")
    click.echo(f"Shared path set to: {session.shared_path}")

    # Map to hold action instances
    actions = {}

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

                # Initialize Generate action if not already done
                if not actions.get("generate"):
                    actions["generate"] = Generate(session)
                
                # Call the generate wrapper method to handle key pair generation
                actions["generate"].generate()

            elif cmd == "2":
                click.echo("Writing encrypted message...")
                # Placeholder for writing encrypted message logic
            elif cmd == "3":
                click.echo("Reading encrypted message...")
                # Placeholder for reading encrypted message logic

    except (KeyboardInterrupt, SystemExit):
        click.echo("\nExiting application.")

if __name__ == "__main__":
    main()
    