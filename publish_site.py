import subprocess
import sys
from datetime import datetime


def run_command(command):
    result = subprocess.run(
        command,
        shell=True,
        text=True,
        capture_output=True
    )

    if result.stdout:
        print(result.stdout.strip())

    if result.returncode != 0:
        if result.stderr:
            print(result.stderr.strip())
        sys.exit(result.returncode)


print()
print("================================")
print(" MONEY PC AUTO PUBLISHER")
print("================================")
print()

print("1. Building website...")
run_command("python build_site.py")

print()
print("2. Staging website changes...")
run_command("git add index.html deals.csv")

status = subprocess.run(
    "git status --porcelain",
    shell=True,
    text=True,
    capture_output=True
).stdout.strip()

if not status:
    print()
    print("No changes found.")
    print("Nothing to publish.")
    sys.exit(0)

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

print()
print("3. Creating commit...")
run_command(
    f'git commit -m "Automatic deal update {timestamp}"'
)

print()
print("4. Publishing to GitHub...")
run_command("git push origin main")

print()
print("================================")
print(" SITE UPDATE COMPLETE")
print("================================")