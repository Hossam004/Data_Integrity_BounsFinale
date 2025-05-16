from server_secure import generate_mac as server_generate_mac, verify as server_verify
import hmac
import hashlib
import hashpumpy

def brute_force_key(intercepted_message: bytes, intercepted_mac: str, wordlist: list[str]) -> str | None:
    for key in wordlist:
        print(f'Trying key "{key}" ...', end=' ')
        trial_mac = hmac.new(key.encode(), intercepted_message, hashlib.sha256).hexdigest()
        if trial_mac == intercepted_mac:
            print("Key found!")
            return key
        else:
            print("Not valid.")
    return None

def perform_attack():
    intercepted_message = b"amount=100&to=alice"
    data_to_append = b"&admin=true"
    intercepted_mac = server_generate_mac(intercepted_message)

    print("=== Brute-Forcing Key ===")
    wordlist = ["123456", "password", "letmein", "supersecretkey", "admin", "test"]
    key = brute_force_key(intercepted_message, intercepted_mac, wordlist)

    if not key:
        print("Secret key not found in wordlist. Attack failed.")
        return

    key_length = len(key)

    try:
        new_mac, new_message = hashpumpy.hashpump(intercepted_mac, intercepted_message, data_to_append, key_length)
        forged_message = new_message
        forged_mac = new_mac

        print(f"Forged message: {forged_message}")
        print(f"Forged MAC: {forged_mac}")

        if server_verify(forged_message, forged_mac):
            print("MAC verified successfully (attack succeeded).")
        else:
            print("MAC verification failed (attack failed).")

    except Exception as e:
        print(f"Attack failed: {e}")

if __name__ == "__main__":
    perform_attack()
