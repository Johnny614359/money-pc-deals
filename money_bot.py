import subprocess
import sys


def run(command):
    print()
    print(f"> {command}")

    result = subprocess.run(
        command,
        shell=True,
        text=True
    )

    if result.returncode != 0:
        print()
        print("BOT STOPPED — command failed.")
        sys.exit(result.returncode)


print()
print("================================")
print("       MONEY PC BOT")
print("================================")

run("python import_products.py")
run("python rank_deals.py")
run("python publish_site.py")

print()
print("================================")
print(" MONEY PC BOT FINISHED")
print("================================")