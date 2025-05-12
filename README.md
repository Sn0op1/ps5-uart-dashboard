PS5 UART Dashboard

A Python-based GUI tool for real-time monitoring of PlayStation 5 UART output. This application detects system errors, decodes known error codes (if available), and provides an intuitive interface for log analysis.
🛠️ Features

    Real-time UART Monitoring: Connect to your PS5's UART interface and view live logs.

    Error Code Detection: Automatically identifies and decodes known PS5 error codes.

    Search & Filter Logs: Easily search through logs to find relevant information.

    Log Saving: Option to save logs for future reference or analysis.

    User-Friendly Interface: Built with Tkinter for a straightforward and accessible GUI.

📦 Requirements

    Python 3.x
    Download from: https://www.python.org/downloads/

Install required dependencies:

pip install -r requirements.txt

🚀 Getting Started

Clone the repository:

git clone https://github.com/Sn0op1/ps5-uart-dashboard.git

cd ps5-uart-dashboard

Install dependencies:

pip install -r requirements.txt

Run the application:

python3 ps5_uart_log_dashboard.py

⚠️ Error Code Database

To enable decoding of PS5 hardware error codes, the tool uses an external JSON file.
How to Get the Error Code File

Download ErrorCodes.json from the official source here: 

👉 https://github.com/amoamare/PS5CodeReader/blob/master/ErrorCodes.json

Place the downloaded file in the same directory as ps5_uart_log_dashboard.py.

    ℹ️ If the file is missing, the dashboard will still work, but raw error codes will be shown without descriptions.

📄 License

This project is licensed under the MIT License. See the LICENSE file for details.
🤝 Contributing

Contributions are welcome!
Fork the repository and submit a pull request for any enhancements or bug fixes.
📫 Contact

For questions or suggestions, feel free to open an issue or contact me directly through my GitHub profile.
