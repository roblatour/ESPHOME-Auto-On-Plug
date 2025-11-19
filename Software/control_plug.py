# Copyright Rob Latour, 2025
# License MIT
#
#
# This python script directly controls an ESPHOME switch device; that is to say, without needing to go through Home Assistant
#
#
# Prerequisites:
# the computer you will be using to issue the control_plug.py command needs to have Python 3.7 or higher installed
# and also needs to have pip and the aioesphomeapi and protobuf packages installed.
#
# to install python, follow instructions at https://www.python.org/downloads/
# to install pip, follow instructions at https://pip.pypa.io/en/stable/installation/
# to install aioesphomeapi and protobuf on your system:
# py -m pip install aioesphomeapi protobuf
#
#
# note: this script can either hardcode the esphome encryption key used by the target device,
# or you can pass it on the command line.
#
# If ENCRYPTION_KEY below is an empty string (""), you MUST provide --ekey=... on the command line.
# If ENCRYPTION_KEY has a value, --ekey is optional and will override it if supplied.
#
# The encryption key can be found in the ESPHOME configuration yaml file for the device,
# look for the line that starts with "api:" and then find the "encryption:" subsection
#
#
# Usage:
#   python control_plug.py --host=<host> --action=on|off [--ekey=<encryption_key>]
#
# Examples:
#   py control_plug.py --host=192.168.1.100 --action=on
#   py control_plug.py --host=esphome-jetkvm-power-control.local --action=off
#   py control_plug.py --host=esphome-jetkvm-power-control.local --action=on --ekey=YOUR_ENCRYPTION_KEY_HERE
#

import asyncio
import sys
import inspect
from aioesphomeapi import APIClient

# Set to "" to force providing --ekey on the command line
ENCRYPTION_KEY = "" 

def parse_args(argv):
    host = None
    action = None
    ekey = None

    for arg in argv:
        if arg.startswith("--host="):
            host = arg.split("=", 1)[1]
        elif arg.startswith("--action="):
            action = arg.split("=", 1)[1].lower()
        elif arg.startswith("--ekey="):
            ekey = arg.split("=", 1)[1]

    return host, action, ekey


def print_usage():
    print("Usage:")
    print("  python control_plug.py --host=<host> --action=on|off [--ekey=<encryption_key>]")
    print("")
    print("Examples:")
    print("  py control_plug.py --host=192.168.2.230 --action=on")
    print("  py control_plug.py --host=esphome-jetkvm-power-control.local --action=off")
    print("  py control_plug.py --host=esphome-jetkvm-power-control.local --action=on --ekey=\"Your_Encryption_Key_Here\"")


async def find_relay_entity(entities):
    # 1) Prefer entities marked as switch
    switches = [e for e in entities if getattr(e, "component_type", "") == "switch"]
    if len(switches) == 1:
        return switches[0]
    if len(switches) > 1:
        # If multiple switches, try to pick one with "relay" in id/name
        for e in switches:
            oid = getattr(e, "object_id", "") or ""
            name = getattr(e, "name", "") or ""
            if "relay" in oid.lower() or "relay" in name.lower():
                return e
        return switches[0]

    # 2) Fallback: no explicit switch type; search by "relay" in id/name
    candidates = []
    for e in entities:
        oid = getattr(e, "object_id", "") or ""
        name = getattr(e, "name", "") or ""
        if "relay" in oid.lower() or "relay" in name.lower():
            candidates.append(e)
    if len(candidates) == 1:
        return candidates[0]
    if len(candidates) > 1:
        return candidates[0]

    return None


async def main():
    if len(sys.argv) < 3:
        print_usage()
        return

    host, action, ekey_arg = parse_args(sys.argv[1:])

    if host is None or action not in ("on", "off"):
        print_usage()
        return

    # Decide which encryption key to use
    if ENCRYPTION_KEY:
        encryption_key = ENCRYPTION_KEY
        if ekey_arg:
            encryption_key = ekey_arg  # command line overrides hardcoded value
    else:
        # ENCRYPTION_KEY is empty; require --ekey
        if not ekey_arg:
            print("Error: ENCRYPTION_KEY is empty in the script and no --ekey provided.")
            print_usage()
            return
        encryption_key = ekey_arg

    state = action == "on"

    client = APIClient(
        host,
        6053,
        password=None,
        noise_psk=encryption_key,
    )

    await client.connect(login=True)

    entities, services = await client.list_entities_services()

    relay = await find_relay_entity(entities)

    if relay is None:
        print("Could not automatically identify relay entity. Entities discovered:")
        for e in entities:
            print(
                f"- object_id='{getattr(e, 'object_id', '')}', "
                f"name='{getattr(e, 'name', '')}', "
                f"type='{getattr(e, 'component_type', '')}'"
            )
        await client.disconnect()
        return

    print(
        f"Controlling relay: object_id='{getattr(relay, 'object_id', '')}', "
        f"name='{getattr(relay, 'name', '')}' -> {'ON' if state else 'OFF'}"
    )

    # Handle both sync and async implementations of switch_command
    if inspect.iscoroutinefunction(client.switch_command):
        await client.switch_command(relay.key, state)
    else:
        client.switch_command(relay.key, state)

    print("Done.")
    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())