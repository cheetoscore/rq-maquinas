from sqlalchemy import create_engine

# Configuración de la conexión a PostgreSQL
connection_string = "postgresql://neondb_owner:Vk8otUHlaQG0@ep-round-truth-a5tysl1v.us-east-2.aws.neon.tech/neondb"
engine = create_engine(connection_string, connect_args={"sslmode": "require"})
