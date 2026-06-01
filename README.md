# ADA WebApp - Arquitectura General - MLP

## Descripción

Aplicación web construida con Flask + Dash para entregar una experiencia visual centralizada sobre información operacional, configuración, dashboards, alarmas, analítica básica y administración funcional.

La aplicación está diseñada como una WebApp transversal para distintos ambientes y aplicaciones MLP. Su arquitectura permite reutilizar la misma base de código y documentación en ambientes DEV, UAT y PRD, ajustando únicamente la configuración, las variables de entorno y la abreviatura correspondiente de cada aplicación.

## Alcance de este README

Este README describe únicamente la aplicación web Flask + Dash: su propósito, estructura, dependencias principales, forma de ejecución, configuración y convenciones generales de desarrollo.

No describe en detalle los procesos backend externos de ingesta, cálculo, compactación o procesamiento pesado. La WebApp consume información ya preparada desde servicios y artefactos publicados, principalmente desde Azure Cosmos DB y SharePoint/DataEntry.

## Arquitectura general

La aplicación web se despliega como una WebApp Flask + Dash sobre Microsoft Azure. La arquitectura está pensada para ser transversal entre ambientes y aplicaciones, por lo que los nombres de recursos se representan de forma genérica usando el patrón:

```text
MLP-{Ambiente}-{Recurso}-{AbrevAPP}
```

Donde:

* `{Ambiente}` corresponde al ambiente de despliegue: `DEV`, `UAT` o `PRD`.
* `{Recurso}` corresponde al tipo de recurso Azure: `RG`, `APP`, `ASP`, `COSMOS`, `KV`, `APPI`, `LAW`, entre otros.
* `{AbrevAPP}` corresponde a la abreviatura única de la aplicación.

La WebApp recibe acceso desde el navegador del usuario, utiliza Microsoft Entra ID para autenticación y perfilamiento, consume configuración y artefactos desde SharePoint/DataEntry, y consulta datos runtime desde Azure Cosmos DB. Los secretos y conexiones se administran mediante Azure Key Vault, mientras que la observabilidad de la aplicación se apoya en Application Insights y Log Analytics.

![ADA WebApp - Arquitectura General - MLP](docs/images/architecture/web-architecture-general.png)

Componentes principales:

| Componente             | Rol dentro de la WebApp                                                                           |
| ---------------------- | ------------------------------------------------------------------------------------------------- |
| Navegador web          | Punto de acceso para operadores, administradores y usuarios.                                      |
| Microsoft Entra ID     | Autenticación, autorización, perfiles y roles de usuario.                                         |
| SharePoint / DataEntry | Fuente de configuración y artefactos administrativos.                                             |
| App Service Plan       | Define la capacidad de alojamiento de la aplicación: CPU, memoria, escala y región.               |
| App Service            | Ejecuta la WebApp Flask + Dash.                                                                   |
| Azure Cosmos DB        | Almacena configuración publicada, snapshots runtime, sesiones y datos consultables por la WebApp. |
| Azure Key Vault        | Centraliza secretos, claves y cadenas de conexión.                                                |
| Application Insights   | Registra métricas, trazas y monitoreo de la aplicación.                                           |
| Log Analytics          | Centraliza logs, consultas y análisis operacional.                                                |

La WebApp no ejecuta procesos pesados de ingesta ni cálculo. Su responsabilidad principal es servir la experiencia visual, resolver identidad y navegación, consultar contratos ya preparados y renderizar la información mediante layouts y callbacks Dash.

## Stack tecnológico

La WebApp está construida sobre un stack Python orientado a aplicaciones web interactivas, con Flask como servidor base y Dash como framework principal para la construcción de interfaces, páginas, dashboards y callbacks.

| Categoría               | Tecnología / Servicio                | Uso principal                                                                                             |
| ----------------------- | ------------------------------------ | --------------------------------------------------------------------------------------------------------- |
| Lenguaje                | Python                               | Desarrollo principal de la aplicación web.                                                                |
| Servidor web            | Flask                                | Inicialización de la aplicación, rutas, middlewares, autenticación y configuración base.                  |
| Framework visual        | Dash                                 | Construcción de layouts, páginas, callbacks y componentes interactivos.                                   |
| Componentes UI          | Dash Bootstrap Components            | Componentes visuales basados en Bootstrap.                                                                |
| Tablas y administración | Dash AG Grid                         | Grillas administrativas, edición de datos y visualización tabular avanzada.                               |
| Visualización           | Plotly                               | Gráficos, tendencias, indicadores y visualizaciones operacionales.                                        |
| Estilos                 | CSS / Bootstrap                      | Estilos globales, layout responsive, temas visuales y personalización de componentes.                     |
| Scripts frontend        | JavaScript                           | Funcionalidades complementarias en `assets`, control de loader, eventos de UI y utilidades del navegador. |
| Configuración externa   | SharePoint / DataEntry               | Fuente de configuración, catálogos y artefactos administrables.                                           |
| Datos runtime           | Azure Cosmos DB                      | Snapshots, configuración publicada, sesiones, analítica básica y datos consultados por la WebApp.         |
| Seguridad               | Azure Key Vault                      | Gestión de secretos, claves y cadenas de conexión.                                                        |
| Identidad               | Microsoft Entra ID                   | Autenticación, autorización, perfiles y roles.                                                            |
| Observabilidad          | Application Insights / Log Analytics | Métricas, trazas, logs centralizados, diagnóstico y monitoreo.                                            |
| Despliegue              | Azure App Service                    | Ejecución de la WebApp Flask + Dash.                                                                      |
| Empaquetado             | Docker                               | Construcción y despliegue reproducible de la aplicación.                                                  |

El stack está orientado a mantener una separación clara entre presentación, servicios internos, infraestructura compartida y configuración externa. La WebApp debe mantenerse liviana: los callbacks Dash deben consultar servicios y contratos preparados, evitando incorporar procesos pesados de cálculo, ingesta o transformación intensiva dentro de la capa visual.

## Organización del proyecto

El proyecto está organizado por capas y responsabilidades, separando la inicialización de la aplicación, las funcionalidades de negocio, las páginas Dash, los componentes compartidos y los archivos de despliegue.

```text
.
├── app.py
├── Dockerfile
├── azure-pipelines.yml
├── gunicorn.config.py
├── requirements.txt
├── ruff.toml
├── setup.py
├── docker_files/
└── src/
    ├── app/
    ├── features/
    ├── pages/
    └── shared/
```

### `src/app`

Contiene la capa de arranque y configuración de la WebApp Flask + Dash.

```text
src/app/
├── auth/
├── blueprints/
├── bootstrap/
├── dash/
├── navigation/
├── dependencies.py
├── env_configuration.py
├── extensions.py
├── factory.py
├── logging_config.py
├── middlewares.py
├── routes.py
└── server.py
```

Responsabilidades principales:

* Crear e inicializar la aplicación Flask.
* Inicializar Dash y registrar layouts/callbacks.
* Configurar middlewares, rutas, autenticación y navegación global.
* Inicializar servicios compartidos en `extensions.py`.
* Exponer dependencias mediante `dependencies.py`.
* Centralizar configuración de entorno y logging.

### `src/features`

Contiene las funcionalidades principales de la WebApp. Cada feature agrupa su lógica, servicios, modelos, componentes o callbacks relacionados con un dominio funcional específico.

```text
src/features/
├── admin_framework/
├── alarm_management/
├── alarm_monitor/
├── alarm_runtime/
├── basic_analytics_runtime/
├── configuration/
├── dashboard_runtime/
├── dashboards/
├── identity/
├── navigation/
└── user_sessions/
```

Responsabilidades principales:

* Agrupar funcionalidades por dominio.
* Mantener aislada la lógica propia de dashboards, alarmas, configuración, navegación, identidad y sesiones.
* Evitar que los callbacks Dash concentren lógica pesada.
* Facilitar la reutilización y evolución independiente de cada módulo.

### `src/pages`

Contiene las páginas Dash expuestas por la aplicación. Esta capa conecta rutas o páginas visibles con los layouts correspondientes.

```text
src/pages/
├── admin_panels/
├── analytics/
└── dashboards/
```

Responsabilidades principales:

* Definir páginas navegables de la WebApp.
* Conectar layouts de alto nivel con las features correspondientes.
* Mantener separada la definición de páginas respecto de la lógica interna de cada feature.

### `src/shared`

Contiene código transversal reutilizable por distintas partes de la aplicación.

```text
src/shared/
├── formatters/
├── infrastructure/
├── runtime/
├── time/
└── ui/
```

Responsabilidades principales:

* Centralizar infraestructura compartida, como clientes, repositorios o servicios comunes.
* Agrupar componentes UI reutilizables.
* Mantener utilidades transversales de formato, tiempo y runtime.
* Evitar duplicación de código entre features.

### Archivos raíz relevantes

| Archivo / carpeta     | Propósito                                                    |
|-----------------------| ------------------------------------------------------------ |
| `app.py`              | Entry point principal para levantar la WebApp.               |
| `Dockerfile`          | Imagen de contenedor para despliegue.                        |
| `azure-pipelines.yml` | Definición de pipeline CI/CD.                                |
| `gunicorn.config.py`  | Configuración de Gunicorn para ejecución productiva.         |
| `requirements.txt`    | Dependencias Python del proyecto.                            |
| `ruff.toml`           | Reglas de linting y formato.                                 |
| `setup.py`            | Configuración base del paquete/proyecto.                     |
| `docker_files/`       | Archivos auxiliares para construcción o ejecución en Docker. |

No deben considerarse parte de la arquitectura funcional carpetas locales, virtual environments, cachés o archivos generados temporalmente, como `venv/`, `.ruff_cache/`, `__pycache__/` o carpetas runtime/cache locales.

## Servicios externos e infraestructura

La WebApp depende de servicios externos y recursos Azure para resolver autenticación, configuración, persistencia runtime, seguridad, observabilidad y alojamiento. Estos servicios son transversales al ambiente donde se despliegue la aplicación.

| Servicio / Recurso     | Rol principal                                        | Relación con la WebApp                                                                                      |
| ---------------------- | ---------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| Microsoft Entra ID     | Autenticación, autorización, perfiles y roles.       | Permite identificar al usuario, resolver su perfil y controlar acceso a páginas o funcionalidades.          |
| SharePoint / DataEntry | Fuente de configuración y artefactos administrables. | La WebApp lee y/o escribe configuración, catálogos y artefactos funcionales administrados desde DataEntry.  |
| Azure App Service      | Hosting de la aplicación web.                        | Ejecuta la WebApp Flask + Dash y expone la interfaz a los usuarios.                                         |
| App Service Plan       | Capacidad de alojamiento.                            | Define CPU, memoria, escala, región y características de ejecución del App Service.                         |
| Azure Cosmos DB        | Persistencia runtime y datos publicados.             | Almacena snapshots, configuración publicada, sesiones, analítica básica y datos consultables por la WebApp. |
| Azure Key Vault        | Gestión de secretos.                                 | Centraliza claves, cadenas de conexión, tokens y secretos requeridos por la aplicación.                     |
| Application Insights   | Monitoreo de aplicación.                             | Registra métricas, trazas, errores y comportamiento runtime de la WebApp.                                   |
| Log Analytics          | Centralización y consulta de logs.                   | Permite analizar logs, eventos, consultas, alertas y diagnósticos operacionales.                            |

### Azure Cosmos DB

Cosmos DB se utiliza como almacenamiento runtime liviano para información que la WebApp necesita consultar de forma rápida. En el contexto actual, los contenedores principales son:

| Contenedor                  | Uso esperado                                                  |
| --------------------------- | ------------------------------------------------------------- |
| `active_user_sessions`      | Registro de sesiones activas o recientes de usuarios.         |
| `alarm_configuration`       | Configuración funcional relacionada con alarmas.              |
| `alarm_management_actions`  | Acciones de gestión de alarmas realizadas desde la WebApp.    |
| `alarm_management_messages` | Mensajes configurables asociados a la gestión de alarmas.     |
| `alarm_runtime_snapshot`    | Snapshot runtime de alarmas listo para consumo visual.        |
| `basic_analytics`           | Datos agregados para analítica básica de la aplicación.       |
| `kpi_configuration`         | Configuración funcional relacionada con KPIs.                 |
| `kpi_runtime_snapshot`      | Snapshot runtime de KPIs listo para consumo visual.           |
| `navigation_configuration`  | Configuración publicada de navegación, menú y rutas visibles. |
| `publication_state`         | Estado de publicación de artefactos de configuración.         |

Los contenedores pueden variar según la aplicación y el ambiente, pero deben mantener el mismo criterio: Cosmos DB representa información publicada, runtime o consultable por la WebApp; no debe usarse como fuente manual no controlada de configuración si la fuente oficial es SharePoint/DataEntry.

### Observabilidad

La observabilidad apunta principalmente al App Service, ya que la WebApp es el proceso que ejecuta Flask, Dash, callbacks, rutas y servicios internos. Application Insights y Log Analytics deben permitir responder preguntas como:

* si la aplicación está disponible;
* si existen errores en rutas o callbacks;
* cuánto demoran las consultas o renderizados;
* qué excepciones se están generando;
* qué comportamiento tienen los usuarios y sesiones;
* qué eventos requieren diagnóstico operacional.

### Seguridad

Los secretos no deben almacenarse en el código fuente ni en archivos versionados. La WebApp debe resolver credenciales, claves y cadenas de conexión mediante Key Vault o variables de entorno seguras según el ambiente de despliegue.

## Configuración por ambiente

La WebApp está diseñada para ejecutarse en distintos ambientes sin modificar la estructura del código ni la documentación base. El mismo README aplica para ambientes `DEV`, `UAT` y `PRD`, utilizando nombres genéricos y variables de entorno para resolver los recursos correspondientes.

Los recursos deben interpretarse usando el siguiente patrón:

```text
MLP-{Ambiente}-{Recurso}-{AbrevAPP}
```

Donde:

| Variable     | Descripción                                  | Ejemplo                                           |
| ------------ | -------------------------------------------- | ------------------------------------------------- |
| `{Ambiente}` | Ambiente donde se despliega la aplicación.   | `DEV`, `UAT`, `PRD`                               |
| `{Recurso}`  | Tipo de recurso Azure o componente asociado. | `RG`, `APP`, `ASP`, `COSMOS`, `KV`, `APPI`, `LAW` |
| `{AbrevAPP}` | Abreviatura única de la aplicación.          | `ADAN1FS`, `ADA`, u otra abreviatura definida     |

Ejemplo de interpretación:

```text
MLP-DEV-RG-ADAN1FS
MLP-UAT-APP-ADAN1FS
MLP-PRD-COSMOS-ADAN1FS
```

Cada ambiente debe contar con sus propios recursos de ejecución, configuración runtime, secretos y observabilidad. Esto permite aislar pruebas, validaciones y operación productiva sin mezclar datos ni conexiones entre ambientes.

La WebApp debe resolver sus conexiones mediante configuración de entorno. Por esta razón, no se deben hardcodear nombres reales de recursos, cadenas de conexión, secretos ni endpoints dentro del código fuente.

### Relación entre SharePoint/DataEntry y Cosmos DB

SharePoint/DataEntry actúa como fuente administrable de configuración y artefactos funcionales. Desde ahí se gestionan datos como navegación, catálogos, configuración de KPIs, configuración de alarmas u otros artefactos definidos por la aplicación.

Azure Cosmos DB representa la información publicada o runtime disponible para la WebApp en el ambiente actual. Esto significa que la aplicación consulta Cosmos DB para obtener datos listos para renderizar o consumir desde la capa visual.

En términos generales:

| Fuente                           | Responsabilidad                                                                |
| -------------------------------- | ------------------------------------------------------------------------------ |
| SharePoint / DataEntry           | Fuente de configuración administrable.                                         |
| Cosmos DB                        | Configuración publicada, snapshots runtime y datos consultables por la WebApp. |
| Variables de entorno / Key Vault | Resolución segura de conexiones, secretos y parámetros por ambiente.           |

La WebApp no debe asumir que un recurso pertenece a un ambiente específico por su nombre en el código. El ambiente debe resolverse mediante configuración externa, manteniendo el README y la arquitectura como referencias transversales para todas las aplicaciones basadas en esta estructura.

## Ejecución local

La WebApp puede ejecutarse localmente para desarrollo, validación visual y pruebas de integración. Algunas funcionalidades pueden requerir acceso a servicios externos como Azure Cosmos DB, SharePoint/DataEntry, Microsoft Entra ID o Key Vault, según la configuración utilizada.

### Requisitos previos

Antes de levantar la aplicación localmente, validar que el entorno cuente con:

| Requisito                   | Uso                                                                                            |
| --------------------------- | ---------------------------------------------------------------------------------------------- |
| Python 3.14.2               | Versión base requerida para ejecutar la WebApp Flask + Dash.                                   |
| Entorno virtual             | Aislamiento de dependencias del proyecto.                                                      |
| Dependencias del proyecto   | Instaladas desde `requirements.txt`.                                                           |
| Variables de entorno        | Configuración local de ambiente, servicios y secretos.                                         |
| Acceso a servicios externos | Requerido si se probarán integraciones reales con Azure, SharePoint/DataEntry o autenticación. |
| Docker                      | Opcional, para ejecutar la aplicación en contenedor.                                           |

### Instalación local

La creación del entorno virtual depende del sistema operativo utilizado.

Linux/macOS:

```bash
python3.14 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
py -3.14 -m venv .venv
.venv/Scripts/Activate.ps1
```

Windows CMD:

```bat
py -3.14 -m venv .venv
.venv/Scripts/activate.bat
```

Uso de cada comando:

| Comando                      | Uso                                                           |
| ---------------------------- | ------------------------------------------------------------- |
| `python3.14 -m venv .venv`   | Crea el entorno virtual en Linux/macOS usando Python 3.14.2.  |
| `py -3.14 -m venv .venv`     | Crea el entorno virtual en Windows usando el Python Launcher. |
| `source .venv/bin/activate`  | Activa el entorno virtual en Linux/macOS.                     |
| `.venv/Scripts/Activate.ps1` | Activa el entorno virtual en Windows PowerShell.              |
| `.venv/Scripts/activate.bat` | Activa el entorno virtual en Windows CMD.                     |

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Validar versión de Python activa:

```bash
python --version
```

La versión esperada es:

```text
Python 3.14.2
```

### Configuración local

Antes de ejecutar la aplicación, se deben definir las variables de entorno requeridas por el proyecto.

Para ejecución local, el archivo usado por la aplicación es `.env`. Este archivo contiene los valores reales locales y no debe versionarse si incluye secretos, claves o cadenas de conexión.

El archivo `.env.local` se usa solo como referencia de estructura o plantilla para indicar qué variables deben existir. No representa necesariamente la configuración activa de ejecución.

### Primera ejecución local

Cuando se levanta la aplicación por primera vez en un ambiente local o cuando se necesita inicializar la configuración base, se debe ejecutar:

```bash
python app.py --first-load
```

Esta ejecución realiza la carga inicial necesaria para dejar disponible la estructura mínima de operación de la WebApp.

Responsabilidades principales del `--first-load`:

| Inicialización                             | Descripción                                                                                              |
| ------------------------------------------ | -------------------------------------------------------------------------------------------------------- |
| Configuración base en SharePoint/DataEntry | Crea o actualiza los artefactos base requeridos por la aplicación.                                       |
| Menú y navegación                          | Inicializa la configuración base del menú, rutas y navegación global.                                    |
| Proyección en Cosmos DB                    | Publica o sincroniza la configuración mínima necesaria para que la WebApp pueda consultar datos runtime. |
| Usuarios administradores principales       | Crea o asegura los usuarios/perfiles administradores iniciales de la aplicación.                         |

Antes de ejecutar `--first-load`, validar que el archivo `.env` apunte correctamente a los servicios que se quieren inicializar. Si se está trabajando contra recursos remotos, la ejecución puede modificar configuración en SharePoint/DataEntry y Cosmos DB del ambiente configurado.

### Ejecutar la WebApp

Después de la primera carga, la aplicación puede levantarse normalmente desde el entry point principal:

```bash
python app.py
```

La URL local dependerá de la configuración de Flask/Dash, pero normalmente se expone en:

```text
http://localhost:8000
```

### Ejecutar con Docker

El proyecto incluye configuración Docker para levantar la WebApp localmente y para validar integraciones con Cosmos DB en entorno local.

El `Dockerfile` es transversal: se utiliza como base tanto para pruebas locales como para el despliegue del servicio. La configuración específica de ejecución local se encuentra en los archivos `docker-compose` y scripts auxiliares dentro de `docker_files/`.

Archivos principales:

| Archivo / carpeta                                  | Uso                                                                 |
|----------------------------------------------------| ------------------------------------------------------------------- |
| `Dockerfile`                                       | Imagen base de la WebApp. Es transversal para local y despliegue.   |
| `docker-compose.app.local.yml`                     | Levanta la WebApp en local usando Docker Compose.                   |
| `docker-compose.cosmos.local.yml`                  | Levanta Cosmos DB local para pruebas de integración.                |
| `docker_files/linux_macos/app.docker_deploy.sh`    | Script auxiliar para levantar o desplegar la WebApp en Linux/macOS. |
| `docker_files/linux_macos/cosmos.docker_deploy.sh` | Script auxiliar para levantar Cosmos DB local en Linux/macOS.       |
| `docker_files/windows/app.docker_deploy.bat`       | Script auxiliar para levantar o desplegar la WebApp en Windows.     |
| `docker_files/windows/cosmos.docker_deploy.bat`    | Script auxiliar para levantar Cosmos DB local en Windows.           |
| `docker_files/*/cosmosdb.configuration.txt`        | Referencia de configuración requerida para Cosmos DB local.         |
| `docker_files/cosmosdb.information.txt`            | Información general asociada a Cosmos DB local.                     |

Para levantar la WebApp localmente mediante Docker Compose:

```bash
docker compose -f docker-compose.app.local.yml up --build
```

Para levantar Cosmos DB local para pruebas:

```bash
docker compose -f docker-compose.cosmos.local.yml up --build
```

En Linux/macOS también pueden utilizarse los scripts auxiliares:

```bash
sh docker_files/linux_macos/app.docker_deploy.sh
sh docker_files/linux_macos/cosmos.docker_deploy.sh
```

En Windows pueden utilizarse los scripts auxiliares equivalentes:

```bat
docker_files/windows/app.docker_deploy.bat
docker_files/windows/cosmos.docker_deploy.bat
```

Antes de ejecutar la WebApp o Cosmos DB local, se debe revisar y ajustar el archivo `.env` con las variables correspondientes. En particular, cuando se use `docker-compose.cosmos.local.yml`, las variables de conexión deben apuntar al Cosmos local y no a los recursos Azure de `DEV`, `UAT` o `PRD`. El archivo `.env.local` queda como plantilla o referencia de estructura.

### Consideraciones locales

* La ejecución local puede funcionar parcialmente si no existen credenciales válidas hacia Azure, Cosmos DB, SharePoint/DataEntry o Microsoft Entra ID.
* Las pruebas visuales de layouts y componentes pueden realizarse localmente, pero las vistas que consumen datos reales requieren configuración de servicios externos.
* No se deben commitear secretos ni archivos locales de configuración sensible.
* La configuración usada localmente debe respetar el mismo contrato esperado por los ambientes `DEV`, `UAT` y `PRD`.

## Variables de entorno

La WebApp se configura mediante variables de entorno. Estas variables permiten definir el ambiente de ejecución, la conexión a Cosmos DB, la integración con SharePoint/DataEntry, la observabilidad y los datos generales de la aplicación.

Para ejecución local, la WebApp utiliza el archivo `.env`. El archivo `.env.local` se mantiene como referencia de estructura o plantilla de variables. El archivo `.env` no debe versionarse si contiene secretos, claves, connection strings o valores sensibles.

### Variables principales

| Variable                                 | Descripción                                                                    | Valores esperados                                       |
| ---------------------------------------- | ------------------------------------------------------------------------------ | ------------------------------------------------------- |
| `APPLICATION_INSIGHTS_CONNECTION_STRING` | Connection string de Application Insights. En local puede quedar como `LOCAL`. | `LOCAL` o connection string del recurso Azure.          |
| `COSMOS_CONNECTION_MODE`                 | Define si la WebApp usa Cosmos DB local o Cosmos DB remoto en Azure.           | `LOCAL`, `REMOTE`                                       |
| `COSMOS_DATABASE_NAME`                   | Nombre de la base de datos Cosmos DB.                                          | Base local o base del ambiente Azure.                   |
| `COSMOS_ACCOUNT_URI`                     | URI del servicio Cosmos DB.                                                    | URI Azure o `http://localhost:8081/` para Cosmos local. |
| `COSMOS_ACCOUNT_KEY`                     | Clave de acceso a Cosmos DB.                                                   | Valor seguro según ambiente.                            |
| `COSMOS_CONNECTION_STRING`               | Connection string completa de Cosmos DB, si la implementación la utiliza.      | Opcional según configuración.                           |
| `SHAREPOINT_ROOT_PATH`                   | Ruta raíz funcional de la aplicación dentro de SharePoint/DataEntry.           | Ruta de app en SharePoint.                              |
| `APP_NAME`                               | Nombre visible de la aplicación.                                               | Nombre funcional de la app.                             |
| `APP_SHORT_NAME`                         | Nombre corto visible de la aplicación.                                         | Abreviatura funcional de la app.                        |
| `SECRET_KEY`                             | Clave secreta usada por Flask para sesión y seguridad interna.                 | Valor secreto seguro.                                   |
| `FLASK_ENV`                              | Ambiente lógico de ejecución de Flask.                                         | `LOCAL`, `DEV`, `UAT`, `PROD`                           |

### Estructura base de `.env.local`

El archivo `.env.local` debe usarse como referencia de estructura. Para ejecutar localmente, copiar o replicar esa estructura en `.env` y completar los valores reales según el modo de conexión requerido.

```env
# AZURE MONITOR
APPLICATION_INSIGHTS_CONNECTION_STRING="LOCAL"

# COSMOS DB
COSMOS_CONNECTION_MODE="REMOTE"
COSMOS_DATABASE_NAME=""
COSMOS_ACCOUNT_KEY=""
COSMOS_ACCOUNT_URI=""
# COSMOS_CONNECTION_STRING=""

# SHAREPOINT / DATAENTRY
SHAREPOINT_ROOT_PATH=""

# APP INFORMATION
APP_NAME=""
APP_SHORT_NAME=""
SECRET_KEY=""

# ENVIRONMENT
FLASK_ENV="LOCAL"
```

### Cosmos DB remoto y local

La variable `COSMOS_CONNECTION_MODE` determina el origen de Cosmos DB usado por la WebApp.

```env
COSMOS_CONNECTION_MODE="REMOTE"
```

Usar `REMOTE` cuando la WebApp debe conectarse a Cosmos DB en Azure, por ejemplo en ambientes `DEV`, `UAT` o `PROD`.

```env
COSMOS_CONNECTION_MODE="LOCAL"
```

Usar `LOCAL` cuando se levanta Cosmos DB local mediante Docker para pruebas de integración.

La configuración específica de Cosmos DB local se encuentra en los archivos de apoyo:

```text
docker_files/linux_macos/cosmosdb.configuration.txt
docker_files/windows/cosmosdb.configuration.txt
docker_files/cosmosdb.information.txt
```

Cuando se use `docker-compose.cosmos.local.yml`, las variables activas del `.env` deben apuntar al Cosmos local y no a recursos Azure. El archivo `.env.local` solo documenta la estructura esperada.

### Ejecución mediante scripts locales

Para ejecución local con Docker, la WebApp y Cosmos DB local deben levantarse usando los scripts correspondientes al sistema operativo.

Linux/macOS:

```bash
sh docker_files/linux_macos/app.docker_deploy.sh
sh docker_files/linux_macos/cosmos.docker_deploy.sh
```

Windows:

```bat
docker_files/windows/app.docker_deploy.bat
docker_files/windows/cosmos.docker_deploy.bat
```

Estos scripts utilizan la configuración local disponible en el repositorio y las variables definidas en `.env`.

### Configuración de despliegue por ambiente

Los archivos:

```text
dev.mapping-env.csv
uat.mapping-env.csv
prd.mapping-env.csv
```

contienen la configuración que será inyectada durante el despliegue de la aplicación en cada ambiente. Estos archivos pueden incluir datos crudos o referencias necesarias para resolver recursos, como nombres de Key Vault, nombres de servicios, variables del ambiente o parámetros usados por el pipeline.

Esta configuración pertenece al proceso de despliegue y no reemplaza el uso de variables seguras, Key Vault o configuración protegida del servicio. Los secretos no deben quedar expuestos en archivos versionados.

### SharePoint / DataEntry

`SHAREPOINT_ROOT_PATH` define la ruta funcional de la aplicación dentro de SharePoint/DataEntry.

```env
SHAREPOINT_ROOT_PATH=""
```

Este valor debe apuntar a la carpeta o ruta raíz de configuración correspondiente a la aplicación.

### Seguridad de variables

* No versionar el archivo `.env` si contiene secretos.
* No dejar claves reales, connection strings productivas en documentación.
* Las claves y secretos de ambientes desplegados deben resolverse desde Key Vault o desde variables seguras del servicio.
* Si una clave real fue compartida o publicada accidentalmente, debe rotarse.

## Despliegue

La WebApp se despliega como una aplicación contenerizada sobre Azure App Service. El flujo de despliegue debe mantener la misma base de código para los ambientes `DEV`, `UAT` y `PROD`, resolviendo las diferencias mediante variables, archivos de mapping, Key Vault y configuración propia del ambiente.

### Estrategia general

| Elemento              | Responsabilidad                                                                       |
| --------------------- | ------------------------------------------------------------------------------------- |
| `Dockerfile`          | Define la imagen base de la WebApp. Es transversal para ejecución local y despliegue. |
| `azure-pipelines.yml` | Orquesta el proceso de CI/CD.                                                         |
| `dev.mapping-env.csv` | Define la configuración que se inyecta en despliegues DEV.                            |
| `uat.mapping-env.csv` | Define la configuración que se inyecta en despliegues UAT.                            |
| `prd.mapping-env.csv` | Define la configuración que se inyecta en despliegues PROD.                           |
| Azure Key Vault       | Centraliza secretos y referencias sensibles por ambiente.                             |
| Azure App Service     | Ejecuta la WebApp desplegada.                                                         |

### Archivos de mapping por ambiente

Los archivos `dev.mapping-env.csv`, `uat.mapping-env.csv` y `prd.mapping-env.csv` contienen información usada por el pipeline para inyectar configuración durante el despliegue.

Estos archivos pueden incluir referencias como:

* nombres de Key Vault;
* nombres de recursos Azure;
* variables requeridas por ambiente;
* parámetros de despliegue;
* valores crudos no secretos necesarios para configurar la WebApp.

Los secretos, claves y connection strings sensibles no deben quedar expuestos en estos archivos si corresponden a valores protegidos. Para esos casos se debe utilizar Key Vault o configuración segura del servicio.

### Validaciones posteriores al despliegue

Después de desplegar la WebApp, validar al menos:

| Validación           | Resultado esperado                                                    |
| -------------------- | --------------------------------------------------------------------- |
| App Service activo   | La WebApp responde correctamente.                                     |
| Autenticación        | Microsoft Entra ID permite iniciar sesión.                            |
| Navegación           | El menú y las rutas cargan según perfil.                              |
| Cosmos DB            | La aplicación consulta snapshots, configuración publicada y sesiones. |
| SharePoint/DataEntry | La aplicación accede a la ruta configurada en `SHAREPOINT_ROOT_PATH`. |
| Key Vault            | Los secretos se resuelven correctamente.                              |
| Application Insights | Se registran trazas, errores y métricas.                              |
| Log Analytics        | Los logs quedan disponibles para consulta operacional.                |

## Convenciones de desarrollo

La WebApp debe mantenerse organizada, modular y fácil de extender. Las siguientes convenciones ayudan a evitar acoplamiento innecesario y a mantener responsabilidades claras.

### Reglas principales

* Los callbacks Dash deben mantenerse delgados.
* La lógica de negocio debe vivir en servicios, builders, mappers, repositories o modelos de dominio.
* Los servicios globales deben inicializarse en `src/app/extensions.py`.
* El acceso a servicios compartidos debe realizarse mediante `src/app/dependencies.py`.
* Las features deben agrupar su propia lógica funcional.
* Los componentes visuales reutilizables deben vivir en `src/shared/ui`.
* La infraestructura transversal debe vivir en `src/shared/infrastructure`.
* Los callbacks deben registrarse de forma explícita desde la capa de bootstrap.
* No se deben usar imports por side effect para activar comportamiento crítico.
* No se deben hardcodear nombres de recursos Azure, rutas de ambiente ni secretos en el código fuente.

### Separación de responsabilidades

| Capa           | Responsabilidad                                                                       |
| -------------- | ------------------------------------------------------------------------------------- |
| `src/app`      | Inicialización Flask/Dash, extensiones, dependencias, rutas, middlewares y bootstrap. |
| `src/pages`    | Páginas navegables y conexión con layouts de alto nivel.                              |
| `src/features` | Funcionalidades de negocio o UI agrupadas por dominio.                                |
| `src/shared`   | Infraestructura, componentes y utilidades reutilizables.                              |
| `assets`       | CSS, JavaScript, imágenes, manifest e iconos servidos por Dash.                       |

La presentación, el runtime y la configuración deben mantenerse separados. La WebApp puede consultar información preparada, pero no debe absorber procesos pesados de ingesta, cálculo o transformación intensiva dentro de callbacks.

## Calidad de código

El proyecto utiliza herramientas de formato y análisis estático para mantener consistencia en el código fuente.

### Ruff

Comandos recomendados:

```bash
ruff check . --fix
ruff format .
```

Criterios esperados:

* imports ordenados;
* formato consistente;
* comillas simples según configuración del proyecto;
* eliminación de imports no usados;
* reducción de errores simples antes de ejecutar la aplicación;
* evitar código legacy o archivos temporales versionados.

### Archivos que no deben versionarse

No deben formar parte del repositorio archivos o carpetas como:

```text
.venv/
venv/
__pycache__/
.ruff_cache/
.mypy_cache/
.env
.env.local con secretos reales
archivos temporales locales
```

El archivo `.env.local` puede mantenerse solo si se usa como plantilla sin secretos reales. El archivo `.env` corresponde a configuración local activa y no debe versionarse si contiene valores sensibles.

## Testing y validación

La estrategia de pruebas debe priorizar las piezas que concentran lógica y contratos internos. Los callbacks Dash deben mantenerse simples para reducir la necesidad de pruebas unitarias directas sobre la capa visual.

### Áreas prioritarias de prueba

| Área               | Qué validar                                                                    |
| ------------------ | ------------------------------------------------------------------------------ |
| Servicios internos | Reglas de negocio, consultas, composición de datos y respuestas esperadas.     |
| Builders           | Construcción correcta de contextos y modelos visuales.                         |
| Mappers            | Transformación entre datos runtime y contratos de UI.                          |
| Repositories       | Acceso a Cosmos DB, SharePoint/DataEntry u otras fuentes usando mocks o fakes. |
| Validadores        | Normalización de configuración, campos obligatorios y errores esperados.       |
| Dash callbacks     | Solo cuando exista lógica relevante que no pueda aislarse en servicios.        |
| Docker local       | Levantamiento de WebApp y Cosmos local para pruebas de integración.            |

### Validaciones manuales recomendadas

Antes de considerar estable una ejecución local o despliegue, validar:

* carga inicial de la WebApp;
* autenticación y perfil de usuario;
* carga de navegación;
* renderizado de dashboards principales;
* carga de vistas de alarmas;
* acceso a paneles administrativos;
* conexión a Cosmos DB;
* conexión a SharePoint/DataEntry;
* recepción de logs en observabilidad cuando aplique.

## Troubleshooting rápido

Esta sección resume revisiones frecuentes ante errores comunes de ejecución local o despliegue.

| Problema                   | Revisar                                                                                                                 |
| -------------------------- |-------------------------------------------------------------------------------------------------------------------------|
| La app no inicia           | Versión de Python, dependencias instaladas, `.env`, logs de arranque.                                                   |
| No carga navegación        | `--first-load`, configuración en SharePoint/DataEntry, proyección en Cosmos, perfil del usuario.                        |
| Falla Cosmos DB            | `COSMOS_CONNECTION_MODE`, `COSMOS_DATABASE_NAME`, `COSMOS_ACCOUNT_URI`, `COSMOS_ACCOUNT_KEY`, contenedores disponibles. |
| Falla Cosmos local         | `docker-compose.cosmos.local.yml`, configuración en `cosmosdb.configuration.txt`, variables activas en `.env`.          |
| Falla SharePoint/DataEntry | `SHAREPOINT_ROOT_PATH`, credenciales, disponibilidad del servicio y ruta configurada.                                   |
| Falla autenticación        | Configuración de Microsoft Entra ID, permisos, perfil del usuario y rutas protegidas.                                   |
| No aparecen dashboards     | Snapshots runtime en Cosmos, configuración publicada, logs del servicio de consulta.                                    |
| No aparecen alarmas        | Snapshot runtime de alarmas, configuración de alarmas y servicios asociados.                                            |
| No llegan logs             | `APPLICATION_INSIGHTS_CONNECTION_STRING`, configuración de Application Insights y Log Analytics.                        |
| Cambios no reflejados      | Revisar si la configuración fue guardada, publicada y consultada desde el ambiente correcto.                            |

### Riesgo con `--first-load`

Antes de ejecutar:

```bash
python app.py --first-load
```

validar cuidadosamente el `.env`. Esta acción puede crear o actualizar configuración base en SharePoint/DataEntry y proyecciones en Cosmos DB. Si las variables apuntan a un ambiente remoto, la inicialización afectará ese ambiente.

## Documentación complementaria

El README general funciona como punto de entrada. La documentación más detallada debe vivir dentro de `/docs`.

Documentos recomendados:

```text
docs/
├── architecture.md
├── local-development.md
├── environment-variables.md
├── configuration-and-publication.md
├── deployment.md
├── development-conventions.md
├── troubleshooting.md
└── images/
    └── architecture/
        └── web-architecture-general.png
```

Referencias sugeridas:

* [Arquitectura web](docs/architecture.md)
* [Ejecución local](docs/local-development.md)
* [Variables de entorno](docs/environment-variables.md)
* [Configuración y publicación](docs/configuration-and-publication.md)
* [Despliegue](docs/deployment.md)
* [Convenciones de desarrollo](docs/development-conventions.md)
* [Troubleshooting](docs/troubleshooting.md)

## Notas importantes

* Este README es transversal para aplicaciones ADA WebApp en ambientes `DEV`, `UAT` y `PROD`.
* La nomenclatura de recursos debe interpretarse mediante el patrón `MLP-{Ambiente}-{Recurso}-{AbrevAPP}`.
* El archivo `.env` es la configuración activa para ejecución local.
* El archivo `.env.local` debe usarse solo como plantilla o referencia de estructura.
* No se deben versionar secretos, claves, connection strings ni valores productivos sensibles.
* Cosmos DB representa información publicada, runtime o consultable por la WebApp.
* SharePoint/DataEntry representa la fuente administrable de configuración y artefactos funcionales.
* La observabilidad debe apuntar principalmente al App Service, porque ahí se ejecutan Flask, Dash, callbacks y servicios internos.
* La primera carga con `python app.py --first-load` debe ejecutarse solo después de validar el ambiente configurado.
