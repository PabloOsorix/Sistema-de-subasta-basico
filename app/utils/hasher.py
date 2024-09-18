import bcrypt

# Función para hashear la contraseña
def hash_sensible_data(password: str) -> str:
    # Generar un salt
    salt = bcrypt.gensalt()
    # Hashear la contraseña con el salt generado
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

# Función para verificar la contraseña
def check_hashed_data(plain_password: str, hashed_password: str) -> bool:
    # Comparar la contraseña en texto plano con el hash
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


