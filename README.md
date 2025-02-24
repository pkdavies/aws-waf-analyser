# Header Analyzer and Request Sender

## Overview

This repository contains a Python script that provides a class-based solution for parsing HTTP header strings, extracting cookies into their own JSON block, and optionally sending an HTTP request using the provided headers (including cookies). The script decodes any URL-encoded values and includes both raw and decoded versions in its output.

## Features

- **Header Parsing:**  
  Extracts the request line and individual headers from a multi-line header string.

- **Cookie Extraction:**  
  Breaks the cookie header into individual cookies, parsing each cookie's name and value.

- **URL Decoding:**  
  Decodes URL-encoded header and cookie values and provides both the raw and decoded data.

- **HTTP Request:**  
  Optionally sends an HTTP request with the parsed headers and cookies and returns the HTTP response code.

- **JSON Output:**  
  Outputs the parsed headers and cookies in a structured JSON format.

## Installation

1. **Clone the Repository:**

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install Dependencies:**

   The script requires Python 3 and the following Python packages:
   - `requests`

   Install the dependencies using `pip`:

   ```bash
   pip install requests
   ```

## Usage

The script is executed directly from the command line. It parses a predefined header string, outputs the parsed JSON, and attempts to send an HTTP request using the parsed headers and cookies.

```bash
python main.py
```

### Command-Line Options

- **HTTP Scheme:**  
  By default, the script uses `https` as the URL scheme. To change this, modify the `scheme` parameter in the `send_request()` method call in the script.

## Code Structure

- **`HeaderAnalyzer` Class:**  
  The main class defined in the script. It includes the following methods:
  
  - `parse_headers()`:  
    Parses the header string into structured header fields and cookies. If a header or cookie value is URL encoded, both the raw and decoded versions are provided.
  
  - `to_json()`:  
    Converts the parsed header information into a formatted JSON string.
  
  - `send_request()`:  
    Constructs the full URL using the request line and host header, sends an HTTP request using the parsed headers and cookies, and returns the HTTP response code.

- **Main Block:**  
  Demonstrates how to define the header text, instantiate the `HeaderAnalyzer` class, print the parsed JSON output, and send an HTTP request to display the response code.

## Example Output

The script will output a JSON structure similar to the following:

```json
{
    "request_line": "GET /",
    "headers": {
        "host": "www.website.com",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        // additional headers...
    },
    "cookies": {
        "wp_woocommerce_session_624b810f3a3ebc674e415a7637e6df5f": {
            "raw": "6%7C%7C1740554520%7C%7C1740450920%7C%7C664257b24991b2864d6d0c097ef4212a",
            "decoded": "2||1740552520||1740660920||664257b24891b2864d5e0c097ef4212a"
        },
        // additional cookies...
    }
}
```

After displaying the parsed JSON, the script attempts to send an HTTP request and prints the HTTP response code (e.g., `200`).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request with any improvements or bug fixes.

## Contact

For any questions or support, please open an issue or contact me.
