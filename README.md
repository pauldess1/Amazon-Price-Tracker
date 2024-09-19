# AMAZON Price Alert Tracker

**AMAZON Alert Tracker** is a Python application that allows you to track product prices on Amazon and send email alerts when the price drops below a defined threshold. The user interface is built with `tkinter` for easy alert management.

## Features

- Track prices for multiple products.
- Automatically send an email when the price falls below a defined threshold.
- Simple user interface using `tkinter`.
- Multi-threading support to run several alerts in parallel.

## Installation

1. Clone the repository to your local machine:
    ```bash
    git clone https://github.com/pauldess1/Amazon-Price-Tracker.git
    cd Amazon-Price-Tracker
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the application:
    ```bash
    python app.py
    ```

## Configuration

In the user interface, you can add multiple alerts by specifying:
- The product URL
- Your email address to send alerts
- The receiver's email address
- The sender email's password
- The price threshold (in €)
- The checking interval (in seconds)

## Usage

1. Open the application.
2. Enter the required information to add an alert.
3. Click "Add Alert" to start tracking the price.

### Email Example

Here is an example of the email notification that will be sent when a price drops below the threshold:

![Email Notification](./images/message.png)

### Examples

Here is a screenshot of the user interface:

![User Interface](./images/interface.png)

## Technologies Used

- **Python 3.x**: Main programming language.
- **tkinter**: For the graphical user interface.
- **BeautifulSoup**: For extracting price information.
- **smtplib**: To send email alerts.
- **Threading**: To handle multiple alerts concurrently.

## Contributing

Contributions are welcome! If you have ideas or suggestions, feel free to open an **issue** or submit a **pull request**.
