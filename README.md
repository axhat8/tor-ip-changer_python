# 🔱 Akshat's Tor IP Changer 🔱

A fancy, cross-platform, and user-friendly script to automatically change your Tor IP address. Designed for privacy enthusiasts and developers who need to rotate their IP address on the fly.

Run process is in the bottom
![Banner](https://raw.githubusercontent.com/user/repo/main/banner.png)  <!-- You will need to upload a screenshot and replace this URL -->

## ✨ Features

- **Cross-Platform:** Works on Linux, Windows, and Termux.
- **Fancy UI:** Uses a rich, colorful, and interactive command-line interface.
- **Manual & Automatic Mode:** Change your IP once or set it to change automatically at a custom interval.
- **IP Verification:** Automatically checks and displays your IP address before and after the change.
- **Advanced Protection (Error Handling):**
  - Gracefully handles connection errors.
  - Checks if the Tor service is running.
  - Verifies that the IP address has actually changed.
- **Password Support:** Supports Tor control ports protected by a password.
- **No Bundled Tor:** The script is lightweight and uses your existing Tor installation.

## ⚠️ Disclaimer

This tool is for educational and legitimate testing purposes only. The misuse of this script for malicious activities is strongly discouraged. The developers are not responsible for any damage or illegal activities caused by this tool. **Always respect the law and the terms of service of any website you visit.**

## ⚙️ Prerequisites

This script **does not** install Tor for you. You must have the Tor service installed and running on your system.

- **On Linux (Debian/Ubuntu):**
  ```bash
  sudo apt update && sudo apt install tor -y
  ```
- **On Windows:**
  - Download and install the [Tor Browser Expert Bundle](https://www.torproject.org/download/tor/).
  - Run Tor from the command line: `tor.exe`
- **On Termux:**
  ```bash
  pkg install tor -y
  ```

You also need to configure Tor to allow control port connections. Edit your `torrc` file (usually at `/etc/tor/torrc` on Linux, or `Data/Tor/torrc` in your Tor Browser folder on Windows) and add/uncomment the following lines:

```
ControlPort 9051
```

If you want to set a password for the control port, run this command:
```bash
tor --hash-password "your_password"
```
Then add the hashed password to your `torrc` file:
```
HashedControlPassword YOUR_HASHED_PASSWORD
```
Restart the Tor service after editing the `torrc` file.

## 🚀 Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/tor-ip-changer.git
    cd tor-ip-changer
    ```

2.  **Install Python 3** if you don't have it.

3.  **Install the required Python libraries:**
    ```bash
    pip install -r requirements.txt
    ```
    (A `requirements.txt` file should be created with the following content: `requests`, `pysocks`, `rich`)

## ▶️ How to Run

Once you have Tor running and the dependencies installed, you can run the script:

```bash
python3 changer.py
```

The script will greet you with a banner and a menu to choose your desired action.

---
Made with ❤️ by Akshat
