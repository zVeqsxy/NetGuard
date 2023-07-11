# NetGuard

This project is a network monitoring and user management tool built using python and the following libraries:

- `cryptography`
- `bcrypt`
- `scapy`
- `mysql-connector-python`


## Description

NetGuard is a Python-based network monitoring and user management tool that allows you to scan the network, monitor network traffic, and manage users and their information. It provides functionalities to ping active IP addresses and sniff packets on the network, add/edit/delete users, and display their information.

--------------

**Note: This project is still under development and is a work in progress.**

Please keep in mind that the code in this repository may not be fully optimized, efficient, or feature-complete. It is a representation of the current state of development and may contain bugs or incomplete functionality.


## Features

- Scan and ping active IP addresses on the network.
- Sniff network packets for all interfaces or a specific user.
- Add, edit, and delete user information.
- Display user information including first name, last name, description, IP address, and MAC address.
- Support for blocking websites for individual or all users.
- MySQL database integration for storing user information.
- User-friendly command-line interface.


## Installation

1. Clone or download the repository:

    ``` bash
    git clone https://github.com/zVeqsxy/NetGuard.git
    ```

2. Change to the project directory:

    ``` bash
    cd NetGuard
    ```

3. Install the required dependencies:

    ``` bash
    pip install -r requirements.txt
    ```


## Usage

1. Run the main.py file to start the NetGuard tool:

    ``` bash
    python main.py
    ```

2. The main menu will be displayed with options for Tools and Users.

3. Choose the desired option by entering the corresponding number or letter.

4. Follow the on-screen prompts and instructions to perform the desired actions.


## Contributing

Contributions to this project are welcome. If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## Disclaimer

NetGuard is a project created for educational purposes and should only be used in controlled environments with proper authorization. Use this code at your own risk. The developer is not responsible for any misuse, damage, or loss caused by the usage of this project

## License

This project is licensed under the MIT License.

