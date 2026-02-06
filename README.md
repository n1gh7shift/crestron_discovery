    # Crestron UDP Discovery

    A lightweight Python tool that replicates Crestron Toolbox UDP device discovery.

    It broadcasts a discovery packet on UDP port 41794 and listens for replies,
    parsing device information directly from Crestron hardware.

    ## Features

    - Discovers Crestron devices on the local network
    - Extracts:
    - IP address
    - Hostname
    - Device type
    - Firmware version
    - MAC address
    - De-duplicates devices automatically
    - No external dependencies
    - Works on Linux and macOS
    - Uses the same discovery mechanism as Crestron Toolbox

    ## Requirements

    - Python 3.7+
    - Root / Administrator privileges (required for UDP broadcast)

    ## Usage

    ```bash
    sudo python3 crestron_discovery.py