#!/usr/bin/env python3
"""
Header Analyzer and Request Sender Script

This script defines a HeaderAnalyzer class that parses an HTTP header string,
extracts header fields and cookies (with URL-decoding if needed), and can also
place an HTTP request using these headers. The send_request method constructs
the full URL from the request line and host header, sends the request (including
the cookies), and returns the HTTP response code.

Usage:
    python header_analyzer.py
"""

import json
import urllib.parse
import requests


class HeaderAnalyzer:
    """
    A class to parse HTTP header strings, extract header fields and cookies,
    and send an HTTP request using those headers.
    """

    def __init__(self, header_text: str):
        """
        Initialize the HeaderAnalyzer with the header text.
        
        :param header_text: A string containing the HTTP headers.
        """
        self.header_text = header_text

    def parse_headers(self) -> dict:
        """
        Parse the header text into a structured dictionary containing:
         - request_line: The initial request line (e.g. "GET /")
         - headers: A dictionary of all non-cookie header fields. If a header value is URL-encoded,
                    its decoded version is provided alongside the raw value.
         - cookies: A dictionary where each cookie name maps to its raw value and, if applicable,
                    the decoded version.
        
        :return: A dictionary representing the parsed header data.
        """
        # Split header text into individual lines and initialize containers
        lines = self.header_text.strip().splitlines()
        result = {
            "request_line": "",
            "headers": {},
            "cookies": {}
        }

        # Assume the first line is the request line if it doesn't contain a colon.
        if lines and ':' not in lines[0]:
            result["request_line"] = lines[0].strip()

        # Iterate over all lines and process headers
        for line in lines:
            # Only process lines that contain a colon
            if ':' not in line:
                continue

            # Split the line into key and value on the first colon
            key, value = line.split(":", 1)
            key = key.strip().lower()
            value = value.strip()

            # Check if the header is the Cookie header
            if key == "cookie":
                # The cookies are separated by semicolons
                cookie_items = value.split(";")
                for cookie in cookie_items:
                    # Process each cookie which should be in name=value format
                    if '=' in cookie:
                        name, val = cookie.split("=", 1)
                        name = name.strip()
                        val = val.strip()
                        # Decode if URL encoding is detected
                        decoded_val = urllib.parse.unquote(val) if "%" in val else val
                        if decoded_val != val:
                            result["cookies"][name] = {"raw": val, "decoded": decoded_val}
                        else:
                            result["cookies"][name] = {"raw": val}
                    else:
                        # If there is no '=', treat the cookie as a flag with an empty value
                        name = cookie.strip()
                        result["cookies"][name] = {"raw": ""}
            else:
                # For other headers, check if the value is URL encoded
                decoded_value = urllib.parse.unquote(value) if "%" in value else value
                if decoded_value != value:
                    result["headers"][key] = {"raw": value, "decoded": decoded_value}
                else:
                    result["headers"][key] = value

        return result

    def to_json(self) -> str:
        """
        Convert the parsed header information into a formatted JSON string.
        
        :return: A JSON string representing the parsed headers and cookies.
        """
        parsed_data = self.parse_headers()
        return json.dumps(parsed_data, indent=4)

    def send_request(self, scheme: str = "https") -> int:
        """
        Build and send an HTTP request using the parsed headers and cookies.
        The URL is constructed using the 'host' header and the request path from the
        request line. Cookies are included separately.

        :param scheme: The URL scheme to use (default: "https").
        :return: The HTTP response status code.
        :raises ValueError: If a required header (such as 'host') is missing.
        """
        # Parse the headers and cookies
        parsed_data = self.parse_headers()

        # Retrieve the host header; raise error if missing
        host = ""
        headers_parsed = parsed_data.get("headers", {})
        if "host" in headers_parsed:
            if isinstance(headers_parsed["host"], dict):
                host = headers_parsed["host"].get("raw", "")
            else:
                host = headers_parsed["host"]
        if not host:
            raise ValueError("Host header is missing in the provided headers.")

        # Parse the request line (e.g., "GET /")
        request_line = parsed_data.get("request_line", "")
        parts = request_line.split()
        if len(parts) >= 2:
            method = parts[0].upper()
            path = parts[1]
        else:
            # Default to GET and root path if request line is malformed or missing
            method = "GET"
            path = "/"

        # Construct the full URL
        url = f"{scheme}://{host}{path}"

        # Rebuild the headers dictionary (excluding cookies which are handled separately)
        headers = {}
        for key, value in headers_parsed.items():
            if key == "host":
                # Host header can remain in the headers if needed
                headers[key] = value["raw"] if isinstance(value, dict) else value
            else:
                headers[key] = value["raw"] if isinstance(value, dict) else value

        # Build cookies dictionary from parsed cookies (using the raw value)
        cookies = {}
        for cookie_name, cookie_val in parsed_data.get("cookies", {}).items():
            cookies[cookie_name] = cookie_val["raw"] if isinstance(cookie_val, dict) else cookie_val

        # Debug: Uncomment the next lines to see the built URL, headers, and cookies
        # print("URL:", url)
        # print("Method:", method)
        # print("Headers:", headers)
        # print("Cookies:", cookies)

        # Make the HTTP request using the requests library
        response = requests.request(method, url, headers=headers, cookies=cookies)
        return response.status_code


if __name__ == '__main__':
    # Define the header string to be analyzed and used for the request
    header_text = (
        "GET /\n"
        "host: www.gamingintelligence.com\n"
        "accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\n"
        "sec-fetch-site: none\n"
        "accept-encoding: gzip, deflate, br\n"
        "sec-fetch-mode: navigate\n"
        "user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15\n"
        "accept-language: en-GB,en;q=0.9\n"
        "sec-fetch-dest: document\n"
        "cookie: "
    )

    analyzer = HeaderAnalyzer(header_text)

    # Print the parsed header JSON
    print("Parsed Header JSON:")
    print(analyzer.to_json())

    # Attempt to send an HTTP request using the parsed headers and cookies.
    try:
        response_code = analyzer.send_request()
        print("\nHTTP Response Code:", response_code)
    except Exception as e:
        print("\nAn error occurred while sending the HTTP request:", e)
