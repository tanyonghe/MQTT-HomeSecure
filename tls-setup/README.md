# Mosquitto SSL Configuration - MQTT TLS Security

## Follow these steps to create your own Certificate Authority, Server keys and certificates.

0. Install `openssl` on your MQTT broker.  
`sudo apt-get install openssl`

1. Create key pair for the CA.  
`openssl genrsa -des3 -out ca.key 2048`

2. Create certificate for CA using the CA key created in step 1.  
`openssl req -new -x509 -days 1826 -key ca.key -out ca.crt`

Example form details:
```
Country Name (2 letter code): SG
State or Province Name (full name): Singapore
Locality Name (eg, city): Singapore
Organization Name (eg, company): CAmaster
Organization Unit Name (eg, section): TEST
Common Name (e.g. server FQDN or YOUR name): ws4
Email Address: steve@testemail.com
```

3. Create server key pair that will be used by the broker.  
`openssl genrsa -out server.key 2048`

4. Create a certificate request `.csr`.  
`openssl req -new -out server.csr -key server.key`

Example form details:
```
Country Name (2 letter code): SG
State or Province Name (full name): Singapore
Locality Name (eg, city): Singapore
Organization Name (eg, company): Server-cert
Organization Unit Name (eg, section): test
Common Name (e.g. server FQDN or YOUR name): ws4
Email Address: steve@testemail.com
```

5. Use the CA key to verify and sign the server certificate to create the `server.crt` file.  
`openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 360`

6. Check that these three files are found in the current directory:

```
ca.crt
server.crt
server.key
```

7. Copy `ca.crt` into the broker's `/etc/mosquitto/ca_certificates/` directory.

8. Copy `server.crt` and `server.key` into the `/etc/mosquitto/certs/` directory.

9. Copy `ca.crt` into the `src/broker` directory and `src/client` directory.
   * The certificate allows communication with the broker on port 8883 using TLS protocol.
   * Data Transfer Flow: Data sensors -> Broker -> Client
   * And yes, you need the certificate even if data sensors are connected to the same physical device as the MQTT broker.

10. Replace the `mosquitto.conf` file found in the broker's `/etc/mosquitto/` directory with the `mosquitto.conf` file provided in this repository's `tls-setup` directory.

11. In the MQTT publisher code, replace TLS_CERT_FILEPATH with the filepath location for `ca.crt` in the `src/broker` directory.

12. In the MQTT subscriber code, replace TLS_CERT_FILEPATH with the filepath location for `ca.crt` in the `src/cient` directory.

## Extra Things to Note

To run Mosquitto on port 8883 for TLS connections instead of the default port 1883, you can first stop the service using `sudo systemctl stop mosquitto` 
before running it again but this time with the configuration files you set earlier on `sudo mosquitto -c /etc/mosquitto/mosquitto.conf`  

When filling out the forms in steps 2 and 4, the common name is important and is usually the domain name of the server.  

If there is a problem with mismatched server names on the certificate, add in `client.tls_insecure_set(True)` in the MQTT subscriber code. 
However this is discouraged when it comes to actual deployment as it opens up the protocol to TLS vulnerabilities and exploits like Browser Exploit Against SSL/TLS (BEAST).  
