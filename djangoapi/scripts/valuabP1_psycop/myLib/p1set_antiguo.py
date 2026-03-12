import os

#crear variables de entorno para la conexion a la base de datos
POSTGRES_USER=os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD=os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST=os.getenv('POSTGRES_HOST') #esta dentro del docker
POSTGRES_PORT=os.getenv('POSTGRES_PORT')
POSTGRES_DB='proyecto1'

