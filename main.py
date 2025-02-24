#!/usr/bin/env python3
"""
Header Analyzer Script

This script defines a HeaderAnalyzer class that parses an HTTP header string,
extracts all header fields, and further processes the cookie header by splitting
its individual cookies into a separate block. For any cookie (or header value)
containing URL-encoded content, the script decodes the value and includes both
the raw and decoded versions in the JSON response.

Usage:
    python header_analyzer.py
"""

import json
import urllib.parse


class HeaderAnalyzer:
    """
    A class to parse HTTP header strings and extract header fields and cookies.
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


if __name__ == '__main__':
    # Define the header string to be analyzed
    header_text = (
        "GET /\n"
        "host: www.website.com\n"
        "accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\n"
        "sec-fetch-site: none\n"
        "accept-encoding: gzip, deflate, br\n"
        "sec-fetch-mode: navigate\n"
        "user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15\n"
        "accept-language: en-GB,en;q=0.9\n"
        "sec-fetch-dest: document\n"
        "cookie: wp_woocommerce_session_874e415a7637e6df5e=6%7C%7C10c097ef4212a;"
    )

    # Instantiate the analyzer and print the JSON output
    analyzer = HeaderAnalyzer(header_text)
    print(analyzer.to_json())
