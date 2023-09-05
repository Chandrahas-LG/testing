import subprocess
import json

def authenticate_and_choose_region():
    subprocess.run(["oci", "session", "authenticate"])

def list_all_block_volumes():
    try:
        output = subprocess.run(["oci", "bv", "volume", "list", "--all"], capture_output=True, text=True).stdout
        block_volumes = json.loads(output)
        return block_volumes
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        print("Command Output:", output)
        return []

def update_block_volume_size(volume_id, new_size):
    subprocess.run(["oci", "bv", "volume", "update", "--volume-id", volume_id, "--size-in-gbs", new_size,"--auth security_token"])

# def rescan_block_device(block_volume_name):
#     subprocess.run(["sudo", "dd", "if=/dev/" + block_volume_name, "of=/dev/null", "count=1"])
#     subprocess.run(["echo", "1", "|", "sudo", "tee", "/sys/class/block/" + block_volume_name + "/device/rescan"])

def rescan_block_device(block_volume_name):
    # Replace subprocess.run(...) line with this:
    result = subprocess.run(["sudo", "dd", "if=/dev/" + block_volume_name, "of=/dev/null", "count=1"],
                            capture_output=True, text=True)

    # Print the captured output and error
    print("Command Output:", result.stdout)
    print("Command Error:", result.stderr)
    subprocess.run(["echo", "1", "|", "sudo", "tee", "/sys/class/block/" + block_volume_name + "/device/rescan"], shell=True)


def main():
    # authenticate_and_choose_region()
    block_volumes = list_all_block_volumes()

    # Display list of block volumes
    print("List of Block Volumes:")
    for volume in block_volumes:
        print("Volume ID:", volume["id"])
        print("Display Name:", volume["display-name"])
        print("-" * 30)

    # Prompt user for input
    volume_id = input("Enter the Volume ID to update: ")
    new_size = input("Enter the new size (in GB) for the volume: ")

    update_block_volume_size(volume_id, new_size)
    # subprocess.run(["ssh satya2_psqltestdb2.db.gtc-dev.eva.expertcity.com"])
    # subprocess.run(["lsblk"])
    block_volume_name = input("Enter the block_volume_name to update: ")
    rescan_block_device(block_volume_name)

if __name__ == "__main__":
    main()

