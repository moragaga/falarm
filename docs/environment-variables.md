# Variables de entorno

## Propósito

Este documento describe las variables de entorno utilizadas por ADA WebApp para resolver configuración local, integración con Cosmos DB, SharePoint/DataEntry, observabilidad, datos generales de la aplicación y despliegue por ambiente.

La WebApp debe obtener su configuración desde archivos locales, variables seguras del entorno, Key Vault o configuración inyectada por el pipeline, según corresponda al modo de ejecución.

Este documento no describe cómo levantar la aplicación localmente. Esa información se encuentra en `docs/local-development.md`.

## Archivos de configuración

La WebApp utiliza distintos archivos de configuración dependiendo del contexto.

| Archivo               | Uso                                                                         |
| --------------------- | --------------------------------------------------------------------------- |
| `.env`                | Configuración local activa usada por la aplicación durante ejecución local. |
| `.env.local`          | Plantilla o referencia de estructura para crear `.env`.                     |
| `dev.mapping-env.csv` | Configuración inyectada durante despliegues DEV.                            |
| `uat.mapping-env.csv` | Configuración inyectada durante despliegues UAT.                            |
| `prd.mapping-env.csv` | Configuración inyectada durante despliegues PRD.                            |

## `.env`

El archivo `.env` es el archivo activo para ejecución local.

Debe contener los valores reales que la WebApp usará al ejecutar:

```bash
python app.py
```

o:

```bash
python app.py --first-load
```

Este archivo puede contener secretos, claves o connection strings. Por esa razón, no debe versionarse si contiene valores sensibles.

Uso esperado:

```text
.env -> configuración local activa
```

## `.env.local`

El archivo `.env.local` debe utilizarse como plantilla o referencia de estructura.

No representa necesariamente la configuración activa de ejecución.

Uso esperado:

```text
.env.local -> plantilla / referencia de variables
```

La práctica recomendada es copiar o replicar la estructura de `.env.local` en `.env`, completando los valores reales solo en el archivo `.env`.

## Variables principales

| Variable                                 | Descripción                                                                                                            | Valores esperados                                       |
| ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| `APPLICATION_INSIGHTS_CONNECTION_STRING` | Connection string de Application Insights. En local puede quedar como `LOCAL`.                                         | `LOCAL` o connection string del recurso Azure.          |
| `COSMOS_CONNECTION_MODE`                 | Define si la WebApp usa Cosmos DB local o Cosmos DB remoto en Azure.                                                   | `LOCAL`, `REMOTE`                                       |
| `COSMOS_DATABASE_NAME`                   | Nombre de la base de datos Cosmos DB.                                                                                  | Base local o base del ambiente Azure.                   |
| `COSMOS_ACCOUNT_URI`                     | URI del servicio Cosmos DB.                                                                                            | URI Azure o `http://localhost:8081/` para Cosmos local. |
| `COSMOS_ACCOUNT_KEY`                     | Clave de acceso a Cosmos DB.                                                                                           | Valor seguro según ambiente.                            |
| `COSMOS_CONNECTION_STRING`               | Connection string completa de Cosmos DB, si la implementación la utiliza.                                              | Opcional según configuración.                           |
| `SHAREPOINT_ROOT_PATH`                   | Ruta raíz funcional de la aplicación dentro de SharePoint/DataEntry.                                                   | Ruta de app en SharePoint.                              |
| `APP_NAME`                               | Nombre visible de la aplicación.                                                                                       | Nombre funcional de la app.                             |
| `APP_SHORT_NAME`                         | Nombre corto visible de la aplicación.                                                                                 | Abreviatura funcional de la app.                        |
| `SECRET_KEY`                             | Clave secreta usada por Flask para sesión y seguridad interna.                                                         | Valor secreto seguro.                                   |
| `FLASK_ENV`                              | Ambiente lógico de ejecución Flask. También afecta la cantidad de workers y threads definidos en `gunicorn.config.py`. | `LOCAL`, `DEV`, `UAT`, `PROD`                           |

## Estructura base de `.env.local`

El archivo `.env.local` debe contener solo la estructura esperada y valores vacíos o seguros.

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

## Cosmos DB

La WebApp puede conectarse a Cosmos DB remoto en Azure o a Cosmos DB local levantado mediante Docker.

La variable que define el modo de conexión es:

```env
COSMOS_CONNECTION_MODE=""
```

### Cosmos DB remoto

Usar Cosmos DB remoto cuando la WebApp debe conectarse a los recursos Azure de un ambiente.

```env
COSMOS_CONNECTION_MODE="REMOTE"
```

Variables requeridas:

```env
COSMOS_DATABASE_NAME=""
COSMOS_ACCOUNT_URI=""
COSMOS_ACCOUNT_KEY=""
```

`COSMOS_ACCOUNT_URI` debe apuntar al endpoint del recurso Cosmos DB en Azure.

### Cosmos DB local

Usar Cosmos DB local cuando se trabaja con el contenedor local para pruebas de integración.

```env
COSMOS_CONNECTION_MODE="LOCAL"
```

Variables esperadas:

```env
COSMOS_DATABASE_NAME=""
COSMOS_ACCOUNT_URI="http://localhost:8081/"
COSMOS_ACCOUNT_KEY=""
```

La configuración específica de Cosmos local se documenta en:

```text
docker_files/linux_macos/cosmosdb.configuration.txt
docker_files/windows/cosmosdb.configuration.txt
docker_files/cosmosdb.information.txt
```

Cuando se use Cosmos DB local, validar que `.env` apunte a `LOCAL` antes de ejecutar la aplicación.

## SharePoint / DataEntry

`SHAREPOINT_ROOT_PATH` define la ruta funcional de la aplicación dentro de SharePoint/DataEntry.

```env
SHAREPOINT_ROOT_PATH=""
```

Este valor debe apuntar a la ruta raíz donde se administran o consultan los artefactos funcionales de la aplicación.

Ejemplo conceptual:

```text
DataEntry/{SHAREPOINT_ROOT_PATH}/...
```

La ruta exacta puede variar según la estructura definida para cada aplicación.

## Application Insights

`APPLICATION_INSIGHTS_CONNECTION_STRING` define la integración con Application Insights.

Para ejecución local sin envío real de telemetría:

```env
APPLICATION_INSIGHTS_CONNECTION_STRING="LOCAL"
```

Para ambientes desplegados, debe contener la connection string real del recurso Application Insights correspondiente.

```env
APPLICATION_INSIGHTS_CONNECTION_STRING="<connection-string-application-insights>"
```

La observabilidad debe apuntar principalmente al App Service, ya que ahí se ejecutan Flask, Dash, callbacks y servicios internos.

## Variables de aplicación

### `APP_NAME`

Nombre visible de la aplicación.

```env
APP_NAME=""
```

Ejemplo conceptual:

```env
APP_NAME="Flotación Selectiva"
```

### `APP_SHORT_NAME`

Nombre corto visible de la aplicación.

```env
APP_SHORT_NAME=""
```

Ejemplo conceptual:

```env
APP_SHORT_NAME="ADA N1 FS"
```

### `SECRET_KEY`

Clave secreta usada por Flask para sesión y seguridad interna.

```env
SECRET_KEY=""
```

Debe ser un valor seguro y no debe quedar expuesto en documentación, repositorio ni archivos compartidos.

### `FLASK_ENV`

Ambiente lógico de ejecución Flask.

```env
FLASK_ENV="LOCAL"
```

Valores esperados:

| Valor   | Uso                                |
| ------- | ---------------------------------- |
| `LOCAL` | Ejecución local.                   |
| `DEV`   | Ambiente de desarrollo desplegado. |
| `UAT`   | Ambiente de validación.            |
| `PROD`  | Ambiente productivo.               |

`FLASK_ENV` también afecta la configuración runtime de Gunicorn definida en `gunicorn.config.py`.

Configuración actual:

| `FLASK_ENV` | Workers | Threads |
| ----------- | ------: | ------: |
| `DEV`       |       1 |       2 |
| `UAT`       |       3 |       2 |
| Otro valor  |       1 |       2 |

Actualmente `PROD` no tiene un bloque específico en el ejemplo de `gunicorn.config.py`; por lo tanto, si no se define explícitamente, cae en el comportamiento genérico del bloque `else`.

Si producción requiere una configuración distinta, debe declararse explícitamente en `gunicorn.config.py`.

## Mapping de despliegue por ambiente

Los archivos de mapping se utilizan durante el despliegue para inyectar configuración según ambiente.

```text
dev.mapping-env.csv
uat.mapping-env.csv
prd.mapping-env.csv
```

Estos archivos pueden contener datos crudos o referencias necesarias para el pipeline, por ejemplo:

* nombres de Key Vault;
* nombres de recursos Azure;
* variables del ambiente;
* parámetros de despliegue;
* nombres lógicos de servicios;
* valores no secretos requeridos por la aplicación.

Los archivos de mapping pertenecen al proceso de despliegue. No reemplazan Key Vault ni variables seguras del servicio.

## Relación entre configuración local y despliegue

| Contexto        | Fuente principal                             |
| --------------- | -------------------------------------------- |
| Ejecución local | `.env`                                       |
| Plantilla local | `.env.local`                                 |
| Despliegue DEV  | `dev.mapping-env.csv` + Key Vault + pipeline |
| Despliegue UAT  | `uat.mapping-env.csv` + Key Vault + pipeline |
| Despliegue PRD  | `prd.mapping-env.csv` + Key Vault + pipeline |

La WebApp debe comportarse igual estructuralmente en todos los ambientes. Lo que cambia son las variables y recursos resueltos por configuración externa.

## Seguridad de secretos

Reglas obligatorias:

* no versionar `.env` si contiene secretos;
* no dejar claves reales en `.env.local`;
* no documentar `COSMOS_ACCOUNT_KEY`, `SECRET_KEY` ni connection strings productivas;
* usar Key Vault o configuración segura del servicio en ambientes desplegados;
* no hardcodear secretos en código fuente;
* rotar cualquier clave que haya sido compartida o publicada accidentalmente.

## Checklist de configuración

Antes de ejecutar localmente, validar:

| Validación                                             | Resultado esperado                              |
| ------------------------------------------------------ | ----------------------------------------------- |
| `.env` existe                                          | La WebApp tiene configuración activa.           |
| `FLASK_ENV` está definido                              | Debe indicar `LOCAL`, `DEV`, `UAT` o `PROD`.    |
| `COSMOS_CONNECTION_MODE` está definido                 | Debe ser `LOCAL` o `REMOTE`.                    |
| Cosmos apunta al origen correcto                       | Local si se usa Docker, remoto si se usa Azure. |
| `SHAREPOINT_ROOT_PATH` está definido                   | Debe apuntar a la ruta funcional de la app.     |
| `SECRET_KEY` está definido                             | Debe existir para sesión Flask.                 |
| `APPLICATION_INSIGHTS_CONNECTION_STRING` está definido | Puede ser `LOCAL` en desarrollo local.          |
| No hay secretos versionados                            | `.env` no debe subirse al repositorio.          |

## Ejemplo de `.env` para desarrollo local con Cosmos remoto

```env
APPLICATION_INSIGHTS_CONNECTION_STRING="LOCAL"

COSMOS_CONNECTION_MODE="REMOTE"
COSMOS_DATABASE_NAME=""
COSMOS_ACCOUNT_KEY=""
COSMOS_ACCOUNT_URI=""
# COSMOS_CONNECTION_STRING=""

SHAREPOINT_ROOT_PATH=""

APP_NAME=""
APP_SHORT_NAME=""
SECRET_KEY=""

FLASK_ENV="LOCAL"
```

## Ejemplo de `.env` para desarrollo local con Cosmos local

```env
APPLICATION_INSIGHTS_CONNECTION_STRING="LOCAL"

COSMOS_CONNECTION_MODE="LOCAL"
COSMOS_DATABASE_NAME=""
COSMOS_ACCOUNT_URI="http://localhost:8081/"
COSMOS_ACCOUNT_KEY=""
# COSMOS_CONNECTION_STRING=""

SHAREPOINT_ROOT_PATH=""

APP_NAME=""
APP_SHORT_NAME=""
SECRET_KEY=""

FLASK_ENV="LOCAL"
```

## Notas importantes

* `.env` es el único archivo considerado configuración local activa.
* `.env.local` solo define estructura o plantilla.
* `COSMOS_CONNECTION_MODE="LOCAL"` debe usarse solo para Cosmos local.
* `COSMOS_CONNECTION_MODE="REMOTE"` debe usarse para Cosmos Azure.
* `SHAREPOINT_ROOT_PATH` debe apuntar a la ruta funcional de la aplicación en DataEntry.
* `dev.mapping-env.csv`, `uat.mapping-env.csv` y `prd.mapping-env.csv` participan en despliegue, no en la ejecución local directa.
* `FLASK_ENV` afecta tanto el ambiente lógico como la configuración de workers y threads en Gunicorn.
* Nunca ejecutar `python app.py --first-load` sin validar primero las variables activas en `.env`.
