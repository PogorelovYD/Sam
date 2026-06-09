#!/bin/bash

mkdir -p certs

echo "Генерация CA..."
openssl genrsa -out certs/ca_key.pem 4096
openssl req -x509 -new -nodes -key certs/ca_key.pem -sha256 -days 365 \
    -out certs/ca_cert.pem \
    -subj "/C=RU/ST=Moscow/L=Moscow/O=LabCA/OU=DistributedSystems/CN=LabCA"

echo "Создание OpenSSL config для server..."
cat > certs/server_ext.cnf <<EOF
[req]
distinguished_name=req
[san]
subjectAltName=DNS:localhost,IP:127.0.0.1
extendedKeyUsage=serverAuth
EOF

echo "Генерация server key/csr..."
openssl genrsa -out certs/server_key.pem 2048
openssl req -new -key certs/server_key.pem \
    -out certs/server.csr \
    -subj "/C=RU/ST=Moscow/L=Moscow/O=LabServer/OU=DistributedSystems/CN=localhost"

echo "Подпись server certificate..."
openssl x509 -req -in certs/server.csr \
    -CA certs/ca_cert.pem -CAkey certs/ca_key.pem -CAcreateserial \
    -out certs/server_cert.pem -days 365 -sha256 \
    -extfile certs/server_ext.cnf -extensions san

echo "Создание OpenSSL config для client..."
cat > certs/client_ext.cnf <<EOF
[req]
distinguished_name=req
[san]
extendedKeyUsage=clientAuth
EOF

echo "Генерация client key/csr..."
openssl genrsa -out certs/client_key.pem 2048
openssl req -new -key certs/client_key.pem \
    -out certs/client.csr \
    -subj "/C=RU/ST=Moscow/L=Moscow/O=LabClient/OU=DistributedSystems/CN=lab_client"

echo "Подпись client certificate..."
openssl x509 -req -in certs/client.csr \
    -CA certs/ca_cert.pem -CAkey certs/ca_key.pem -CAcreateserial \
    -out certs/client_cert.pem -days 365 -sha256 \
    -extfile certs/client_ext.cnf -extensions san

echo "Готово. Сертификаты созданы в папке certs/"
ls -l certs/