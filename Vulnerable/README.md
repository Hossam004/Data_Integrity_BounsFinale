
# 🔐 Length Extension Attack Simulation

This project demonstrates the **Length Extension Attack** on insecure MAC construction using **MD5**, and shows how the attack **fails** on a secure MAC using **HMAC-SHA256**.

---

## 📁 Project Structure

```
.
├── client.py               # Attacker client against insecure MD5-based server (successful attack)
├── client_attack.py        # Attacker client against secure HMAC-based server (attack fails)
├── server_vulnerable.py    # Vulnerable server using MD5(key || message)
├── server_secure.py        # Secure server using HMAC(key, message)
├── README.md               # Project documentation
```

---

## 🧪 Scenario Overview

- **Victim's Message**: `amount=100&to=alice`
- **Attacker's Goal**: Append `&admin=true` without knowing the secret key and forge a valid MAC.

---

## 🚩 Files Explained

### `server_vulnerable.py`
- Simulates an insecure server that generates a MAC using:
  ```python
  hashlib.md5(SECRET_KEY + message)
  ```
- Susceptible to a length extension attack.

### `server_secure.py`
- Uses a cryptographically secure HMAC construction:
  ```python
  hmac.new(SECRET_KEY, message, hashlib.sha256)
  ```
- Resistant to length extension attacks.

### `client.py`
- Brute-forces the secret key from a predefined wordlist.
- Uses `hashpumpy` to forge a valid message + MAC.
- Simulates a **successful attack** on the vulnerable server.

### `client_attack.py`
- Attempts the same attack on the secure HMAC server.
- **Fails** as HMAC mitigates length extension vulnerabilities.

---

## 🛠️ Requirements

- Python 3.x
- [`hashpumpy`](https://pypi.org/project/hashpumpy/)

### Install `hashpumpy`:
```bash
pip install hashpumpy
```

---

## 🚀 How to Run

### Step 1: Simulate the vulnerable server
```bash
python server_vulnerable.py
```

### Step 2: Attack the vulnerable server
```bash
python client.py
```

Expected output:
```
Secret key found
Forged message: b'amount=100&to=alice&admin=true'
Forged MAC: <forged_mac>
MAC verified successfully (attack succeeded).
```

---

### Step 3: Simulate the secure server
```bash
python server_secure.py
```

### Step 4: Attack the secure server
```bash
python client_attack.py
```

Expected output:
```
Secret key not found in wordlist. Attack failed.
OR
Attack failed: ...
MAC verification failed (attack failed).
```

---

## ✅ Expected Results

| Server Type         | Attack Result        | Vulnerability           |
|---------------------|----------------------|--------------------------|
| `server_vulnerable` | ✅ Attack Succeeds   | Yes (MD5 insecure MAC)   |
| `server_secure`     | ❌ Attack Fails      | No (HMAC is secure)      |

---

## 📚 Key Concepts

- **Length Extension Attack**: Exploits the way some hash functions process input to append data without knowing the original key.
- **HMAC**: Mitigates this attack by applying the key *inside* the hash process securely.
- **Brute-force Key Recovery**: Simulates attacker trying weak keys from a list.
