# Instrucciones de uso

## 1. Clonar:

Introduce el suiguiente comando en tu terminar para clonar el repositorio.

``` bash
git clone https://github.com/PabloOsorix/Sistema-de-subasta-basico.git
```

### 3. Cambio de directorio
``` bash
cd Sistema-de-subasta-basico/
```

### 4. Ambiente virtual
Debes crear y activar un nuevo ambiente virtual 
``` python
python -m venv venv
source ./venv/bin/activate
```

### 5. Instalacion de dependencias
Instala las dependencias desde el archivo requierements txt.
``` python
pip install -r requirements.txt
```
### 6. Inicializacion de la API
Deberas moverte al directorio app
``` bash
cd app/
```
Una vez allí introduce el siguiente comando para iniciar el servidor en modo
desarrollador, este desplegara la API realizada en fastAPI en el localhost
puerto 8000 (http://127.0.0.1:8000/).
``` bash
fastapi dev main.py
```

### Nota:
Sugiero navegar la API a traves de la url http://127.0.0.1:8000/docs#/, la cual usa
Swagger UI para mostrar los end-points.


# Tests
## Ejecucion
Para correr los test disponibles de la aplicacion deberas moverte al directorio **tests**

```
Sistema-de-subasta-basico/tests
```
y luego ejecutar el comando: 
```
pytest unittest 
```

