## seenada
This project is a secure end to end desktop chat application, developed for the course Information Security at CSU Long Beach. 

**Authors**
- Jocelyn Ramirez(jsyramirez@gmail.com)
- Thanh Tran ()

### External Requirements
Crytography: AES (CBC), RSA (OAEP), Hash (SHA-512)
PyOpenSSL
MySQL
Scrypt
PyJWT
Tkinter (GUI)
Requests (POST, GET)

### Usage
1. Run client.py script: python client.py
2. Create account or log in (your new public key will be written to the run directory 'public_key.pem')
3. Send public key via Gmail (or other trusted method)
4. Enter recipient username, message, load their public key, and then hit send.
5. Messages sent to you will automatically appear in the GUI.
