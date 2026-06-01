# Ejecución local

## Propósito

Este documento describe cómo levantar ADA WebApp en ambiente local para desarrollo, validación visual y pruebas de integración.

La ejecución local permite trabajar sobre la WebApp Flask + Dash sin desplegarla en Azure App Service. Algunas funcionalidades pueden requerir acceso a servicios externos como Cosmos DB, SharePoint/DataEntry, Microsoft Entra ID o Key Vault, dependiendo de la configuración activa en `.env`.

Este documento cubre únicamente ejecución local. La arquitectura general, variables de entorno, despliegue y troubleshooting se documentan en archivos separados dentro de `/docs`.

## Requisitos previos

Antes de ejecutar la WebApp localmente, validar que el entorno cuente con:

| Requisito                   | Uso                                                                                           |
| --------------------------- | --------------------------------------------------------------------------------------------- |
| Python 3.14.2               | Versión base requerida por la WebApp.                                                         |
| pip                         | Instalación de dependencias Python.                                                           |
| Entorno virtual             | Aislamiento de dependencias del proyecto.                                                     |
| Docker                      | Ejecución contenerizada de la WebApp o servicios locales.                                     |
| Docker Compose              | Levantamiento de WebApp y Cosmos DB local.                                                    |
| `.env`                      | Configuración local activa usada por la aplicación.                                           |
| `.env.local`                | Plantilla o referencia de estructura de variables.                                            |
| Acceso a servicios externos | Requerido si se prueban integraciones reales con Azure, SharePoint/DataEntry o autenticación. |

## Archivos relevantes para ejecución local

| Archivo / carpeta                                     | Uso                                                                             |
|-------------------------------------------------------| ------------------------------------------------------------------------------- |
| `app.py`                                              | Entry point principal de la WebApp.                                             |
| `.env`                                                | Archivo activo de configuración local.                                          |
| `.env.local`                                          | Plantilla de estructura de variables.                                           |
| `requirements.txt`                                    | Dependencias Python.                                                            |
| `Dockerfile`                                          | Imagen base transversal para local y despliegue.                                |
| `docker-compose.app.local.yml`                        | Levanta la WebApp local mediante Docker Compose.                                |
| `docker-compose.cosmos.local.yml`                     | Levanta Cosmos DB local para pruebas de integración.                            |
| `gunicorn.config.py`                                  | Configuración de Gunicorn para ejecución contenerizada o similar al despliegue. |
| `docker_files/linux_macos/app.docker_deploy.sh`       | Script auxiliar para levantar la WebApp en Linux/macOS.                         |
| `docker_files/linux_macos/cosmos.docker_deploy.sh`    | Script auxiliar para levantar Cosmos DB local en Linux/macOS.                   |
| `docker_files/windows/app.docker_deploy.bat`          | Script auxiliar para levantar la WebApp en Windows.                             |
| `docker_files/windows/cosmos.docker_deploy.bat`       | Script auxiliar para levantar Cosmos DB local en Windows.                       |
| `docker_files/linux_macos/cosmosdb.configuration.txt` | Configuración de referencia para Cosmos DB local en Linux/macOS.                |
| `docker_files/windows/cosmosdb.configuration.txt`     | Configuración de referencia para Cosmos DB local en Windows.                    |
| `docker_files/cosmosdb.information.txt`               | Información general asociada a Cosmos DB local.                                 |

## Entorno virtual

La creación y activación del entorno virtual depende del sistema operativo.

### Linux/macOS

Crear entorno virtual:

```bash
python3.14 -m venv .venv
```

Activar entorno virtual:

```bash
source .venv/bin/activate
```

### Windows PowerShell

Crear entorno virtual:

```powershell
py -3.14 -m venv .venv
```

Activar entorno virtual:

```powershell
.venv\Scripts\Activate.ps1
```

### Windows CMD

Crear entorno virtual:

```bat
py -3.14 -m venv .venv
```

Activar entorno virtual:

```bat
.venv\Scripts\activate.bat
```

## Validar versión de Python

Con el entorno virtual activo, validar la versión de Python:

```bash
python --version
```

Versión esperada:

```text
Python 3.14.2
```

Si la versión no corresponde, revisar la instalación local de Python y la forma en que se creó el entorno virtual.

## Instalar dependencias

Con el entorno virtual activo, instalar dependencias:

```bash
pip install -r requirements.txt
```

Si se actualiza `requirements.txt`, volver a ejecutar el comando para sincronizar el entorno local.

## Configuración local

La WebApp utiliza `.env` como archivo activo para ejecución local.

```text
.env        -> configuración local activa
.env.local  -> plantilla / referencia de estructura
```

El archivo `.env.local` no debe considerarse la configuración activa. Su objetivo es indicar qué variables deben existir y servir como base para crear `.env`.

El archivo `.env` puede contener valores sensibles, por lo que no debe versionarse si incluye secretos, claves o connection strings.

## Estructura base de `.env`

La estructura esperada para ejecución local es:

```env
# AZURE MONITOR
APPLICATION_INSIGHTS_CONNECTION_STRING="LOCAL"

# COSMOS DB
# LOCAL  -> Cosmos DB local levantado con Docker
# REMOTE -> Cosmos DB remoto en Azure
COSMOS_CONNECTION_MODE="REMOTE"

COSMOS_DATABASE_NAME=""
COSMOS_ACCOUNT_KEY=""
COSMOS_ACCOUNT_URI=""
# COSMOS_CONNECTION_STRING=""

# SHAREPOINT / DATAENTRY
# Ruta raíz funcional de la aplicación dentro de SharePoint/DataEntry
SHAREPOINT_ROOT_PATH=""

# APP INFORMATION
APP_NAME=""
APP_SHORT_NAME=""
SECRET_KEY=""

# ENVIRONMENT
# LOCAL - DEV - UAT - PROD
FLASK_ENV="LOCAL"
```

## Cosmos DB remoto o local

La variable `COSMOS_CONNECTION_MODE` define el origen de Cosmos DB usado por la WebApp.

### Cosmos DB remoto

Usar:

```env
COSMOS_CONNECTION_MODE="REMOTE"
```

cuando la WebApp debe conectarse a Cosmos DB en Azure.

En este caso, las variables deben apuntar al recurso correspondiente del ambiente configurado:

```env
COSMOS_DATABASE_NAME=""
COSMOS_ACCOUNT_URI=""
COSMOS_ACCOUNT_KEY=""
```

### Cosmos DB local

Usar:

```env
COSMOS_CONNECTION_MODE="LOCAL"
```

cuando se levanta Cosmos DB local mediante Docker.

En este caso, las variables deben apuntar al servicio local:

```env
COSMOS_DATABASE_NAME=""
COSMOS_ACCOUNT_URI="http://localhost:8081/"
COSMOS_ACCOUNT_KEY=""
```

La configuración específica de Cosmos DB local se encuentra en:

```text
docker_files/linux_macos/cosmosdb.configuration.txt
docker_files/windows/cosmosdb.configuration.txt
docker_files/cosmosdb.information.txt
```

Cuando se use `docker-compose.cosmos.local.yml`, validar que `.env` apunte al Cosmos local y no a recursos Azure.

## Primera ejecución local

Cuando se levanta la aplicación por primera vez o cuando se necesita inicializar la configuración base, se debe ejecutar:

```bash
python app.py --first-load
```

Esta acción inicializa la estructura mínima requerida para operar la WebApp.

Responsabilidades principales de `--first-load`:

| Inicialización                             | Descripción                                                                  |
| ------------------------------------------ | ---------------------------------------------------------------------------- |
| Configuración base en SharePoint/DataEntry | Crea o actualiza artefactos base requeridos por la aplicación.               |
| Menú y navegación                          | Inicializa configuración base de menú, rutas y navegación global.            |
| Proyección en Cosmos DB                    | Publica o sincroniza configuración mínima requerida por la WebApp.           |
| Usuarios administradores principales       | Crea o asegura usuarios/perfiles administradores iniciales de la aplicación. |

Antes de ejecutar este comando, revisar cuidadosamente el archivo `.env`.

Si `.env` apunta a recursos remotos, `--first-load` puede modificar SharePoint/DataEntry y Cosmos DB del ambiente configurado.

## Ejecutar la WebApp localmente

Después de la primera carga, levantar la aplicación con:

```bash
python app.py
```

La URL local normalmente es:

```text
http://localhost:8000
```

La URL exacta puede variar si la configuración de Flask/Dash define otro host o puerto.

## Ejecución local y Gunicorn

En ejecución local directa con:

```bash
python app.py
```

la aplicación se levanta desde el entry point principal del proyecto.

Cuando la WebApp se ejecuta mediante Docker o en un contexto similar al despliegue, puede utilizar la configuración definida en:

```text
gunicorn.config.py
```

Esta configuración define parámetros runtime del servidor WSGI:

| Parámetro      | Valor          | Uso                                                    |
| -------------- | -------------- | ------------------------------------------------------ |
| `bind`         | `0.0.0.0:8000` | Expone la aplicación dentro del contenedor.            |
| `worker_class` | `gthread`      | Usa workers con threads.                               |
| `loglevel`     | `info`         | Nivel de logs de Gunicorn.                             |
| `timeout`      | `90`           | Tiempo máximo antes de considerar un worker bloqueado. |
| `keepalive`    | `5`            | Tiempo de keep-alive para conexiones persistentes.     |

La cantidad de workers y threads depende de `FLASK_ENV`:

| `FLASK_ENV` | Workers | Threads |
| ----------- | ------: | ------: |
| `DEV`       |       1 |       2 |
| `UAT`       |       3 |       2 |
| Otro valor  |       1 |       2 |

Para ejecución local con `FLASK_ENV="LOCAL"`, la configuración cae en el comportamiento genérico: `1` worker y `2` threads.

Si se requiere probar un comportamiento más cercano al despliegue real, usar la ejecución Docker definida por los scripts locales.

## Ejecución local con Docker

El proyecto incluye scripts auxiliares para levantar la WebApp mediante Docker.

El `Dockerfile` es transversal: se usa tanto para ejecución local como para despliegue del servicio.

### Linux/macOS

Levantar la WebApp:

```bash
sh docker_files/linux_macos/app.docker_deploy.sh
```

### Windows

Levantar la WebApp:

```bat
docker_files\windows\app.docker_deploy.bat
```

Estos scripts utilizan la configuración definida en `.env`.

## Cosmos DB local con Docker

Para pruebas de integración, se puede levantar Cosmos DB local mediante Docker.

### Linux/macOS

```bash
sh docker_files/linux_macos/cosmos.docker_deploy.sh
```

### Windows

```bat
docker_files\windows\cosmos.docker_deploy.bat
```

También puede utilizarse Docker Compose directamente si se requiere depurar manualmente:

```bash
docker compose -f docker-compose.cosmos.local.yml up --build
```

Antes de levantar Cosmos DB local, revisar:

```text
docker_files/linux_macos/cosmosdb.configuration.txt
docker_files/windows/cosmosdb.configuration.txt
docker_files/cosmosdb.information.txt
```

## Validaciones rápidas después de levantar la app

Después de ejecutar la WebApp localmente, validar:

| Validación                   | Resultado esperado                                                           |
| ---------------------------- |------------------------------------------------------------------------------|
| App inicia sin errores       | No existen errores críticos en consola.                                      |
| URL local responde           | `http://localhost:8000` carga correctamente.                                 |
| Variables cargadas           | `.env` contiene los valores requeridos.                                      |
| Navegación carga             | El menú se muestra según configuración y perfil.                             |
| Cosmos conecta               | La WebApp puede consultar contenedores requeridos.                           |
| SharePoint/DataEntry conecta | La ruta `SHAREPOINT_ROOT_PATH` es accesible si la funcionalidad la requiere. |
| Logs aparecen                | La consola muestra trazas esperadas de ejecución.                            |

## Problemas frecuentes

### La app no inicia

Revisar:

* versión de Python;
* entorno virtual activo;
* dependencias instaladas;
* archivo `.env`;
* errores de importación;
* puerto ocupado.

### No carga navegación

Revisar:

* si se ejecutó `python app.py --first-load`;
* configuración en SharePoint/DataEntry;
* contenedor `navigation_configuration`;
* perfil del usuario;
* logs de arranque.

### Falla conexión a Cosmos DB

Revisar:

* `COSMOS_CONNECTION_MODE`;
* `COSMOS_DATABASE_NAME`;
* `COSMOS_ACCOUNT_URI`;
* `COSMOS_ACCOUNT_KEY`;
* si se está usando Cosmos local o remoto;
* disponibilidad del contenedor local o recurso Azure.

### Falla Cosmos DB local

Revisar:

* `docker-compose.cosmos.local.yml`;
* scripts en `docker_files/`;
* configuración en `cosmosdb.configuration.txt`;
* puerto `8081`;
* variables activas en `.env`.

### Falla SharePoint/DataEntry

Revisar:

* `SHAREPOINT_ROOT_PATH`;
* credenciales;
* permisos;
* disponibilidad del servicio;
* ruta funcional configurada.

### `--first-load` inicializó el ambiente incorrecto

Revisar inmediatamente el `.env` usado durante la ejecución.

Si apuntaba a un ambiente remoto, validar los artefactos modificados en SharePoint/DataEntry y Cosmos DB. Según el caso, puede ser necesario corregir configuración, republicar artefactos o limpiar datos inicializados por error.

## Reglas importantes

* `.env` es la configuración local activa.
* `.env.local` es solo una plantilla.
* No versionar `.env` con secretos.
* No ejecutar `python app.py --first-load` sin revisar el ambiente configurado.
* Para Cosmos local, usar `COSMOS_CONNECTION_MODE="LOCAL"`.
* Para Cosmos Azure, usar `COSMOS_CONNECTION_MODE="REMOTE"`.
* `FLASK_ENV` afecta la configuración de workers y threads cuando se ejecuta mediante Gunicorn.
* Las pruebas visuales pueden funcionar parcialmente sin servicios externos, pero las vistas con datos reales requieren conexión válida.
