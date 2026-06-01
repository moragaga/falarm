# Troubleshooting

## Propósito

Este documento reúne revisiones rápidas para diagnosticar problemas frecuentes en ADA WebApp durante ejecución local, despliegue o validación funcional.

El objetivo es ayudar a identificar si un problema proviene de:

* configuración local;
* variables de entorno;
* Cosmos DB;
* SharePoint/DataEntry;
* autenticación;
* Dash callbacks;
* Gunicorn;
* despliegue;
* observabilidad;
* configuración publicada.

Este documento no reemplaza los logs técnicos, pero sirve como primera guía de diagnóstico.

## Revisión rápida inicial

Antes de revisar casos específicos, validar lo siguiente:

| Validación               | Resultado esperado                                           |
| ------------------------ | ------------------------------------------------------------ |
| Python                   | Versión `3.14.2` activa en local.                            |
| `.env`                   | Existe y contiene configuración local activa.                |
| `FLASK_ENV`              | Tiene un valor esperado: `LOCAL`, `DEV`, `UAT` o `PROD`.     |
| `COSMOS_CONNECTION_MODE` | Tiene valor `LOCAL` o `REMOTE`.                              |
| `SHAREPOINT_ROOT_PATH`   | Apunta a la ruta funcional correcta en DataEntry.            |
| `SECRET_KEY`             | Está definido.                                               |
| Dependencias             | Instaladas desde `requirements.txt`.                         |
| Logs                     | No muestran errores críticos de importación o configuración. |

## La app no inicia localmente

Revisar:

* entorno virtual activo;
* versión de Python;
* dependencias instaladas;
* archivo `.env`;
* valores obligatorios vacíos;
* errores de importación;
* puerto ocupado;
* errores de conexión inicial a servicios externos.

Comandos útiles:

```bash
python --version
pip install -r requirements.txt
python app.py
```

Si el problema ocurre durante la primera carga:

```bash
python app.py --first-load
```

validar antes que `.env` apunte al ambiente correcto.

## Error de versión de Python

La versión esperada es:

```text
Python 3.14.2
```

Validar con:

```bash
python --version
```

Si la versión no corresponde, recrear el entorno virtual usando Python 3.14.

Linux/macOS:

```bash
python3.14 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
py -3.14 -m venv .venv
.venv\Scripts\Activate.ps1
```

## Faltan dependencias

Síntomas comunes:

* `ModuleNotFoundError`;
* `ImportError`;
* errores al iniciar Flask;
* errores al importar Dash o componentes.

Revisar:

```bash
pip install -r requirements.txt
```

Si el entorno está inconsistente, recrear `.venv`.

## Problemas con `.env`

La ejecución local usa `.env`, no `.env.local`.

| Archivo      | Uso                                   |
| ------------ | ------------------------------------- |
| `.env`       | Configuración activa local.           |
| `.env.local` | Plantilla o referencia de estructura. |

Revisar que `.env` tenga al menos:

```env
APPLICATION_INSIGHTS_CONNECTION_STRING="LOCAL"
COSMOS_CONNECTION_MODE="REMOTE"
COSMOS_DATABASE_NAME=""
COSMOS_ACCOUNT_KEY=""
COSMOS_ACCOUNT_URI=""
SHAREPOINT_ROOT_PATH=""
APP_NAME=""
APP_SHORT_NAME=""
SECRET_KEY=""
FLASK_ENV="LOCAL"
```

Problemas frecuentes:

* `.env` no existe;
* se completó `.env.local` pero no `.env`;
* `COSMOS_CONNECTION_MODE` apunta a `LOCAL` pero Cosmos local no está levantado;
* `COSMOS_CONNECTION_MODE` apunta a `REMOTE` pero las credenciales remotas están vacías;
* `SHAREPOINT_ROOT_PATH` apunta a una ruta incorrecta;
* `SECRET_KEY` está vacío.

## Error con `--first-load`

La primera carga se ejecuta con:

```bash
python app.py --first-load
```

Esta acción puede crear o actualizar:

* configuración base en SharePoint/DataEntry;
* navegación;
* proyección mínima en Cosmos DB;
* usuarios/perfiles administradores iniciales.

Antes de ejecutarla, validar:

| Variable                 | Qué revisar                       |
| ------------------------ | --------------------------------- |
| `FLASK_ENV`              | Ambiente esperado.                |
| `COSMOS_CONNECTION_MODE` | Local o remoto según corresponda. |
| `COSMOS_ACCOUNT_URI`     | Cosmos correcto.                  |
| `COSMOS_DATABASE_NAME`   | Base correcta.                    |
| `SHAREPOINT_ROOT_PATH`   | Ruta correcta en DataEntry.       |
| `APP_NAME`               | Aplicación correcta.              |
| `APP_SHORT_NAME`         | Abreviatura correcta.             |

Si se ejecutó contra el ambiente equivocado:

1. detener la app;
2. revisar `.env`;
3. identificar artefactos creados o modificados;
4. validar SharePoint/DataEntry;
5. validar Cosmos DB;
6. corregir configuración o republicar si corresponde.

## No carga navegación

Revisar:

* si se ejecutó `python app.py --first-load`;
* si existe configuración base en SharePoint/DataEntry;
* si existe proyección en `navigation_configuration`;
* si el usuario tiene perfil válido;
* si la navegación está publicada;
* si el callback o servicio de navegación muestra errores.

Contenedor relevante:

```text
navigation_configuration
```

También revisar:

* permisos del usuario;
* rutas configuradas;
* perfil asociado;
* logs de bootstrap;
* logs de navegación.

## No aparecen dashboards

Revisar:

* página registrada en `src/pages/dashboards`;
* layout disponible;
* contrato base `src/features/dashboards/home`;
* builders generales importados desde `{project_name}/areas`;
* callbacks registrados en `src/app/bootstrap/callback_registry.py`;
* snapshots runtime disponibles;
* conexión a Cosmos DB;
* errores en callbacks Dash.

Contenedores relevantes:

```text
kpi_runtime_snapshot
kpi_configuration
navigation_configuration
```

Si el problema ocurre al agregar una nueva UI, revisar el flujo:

```text
{project_name}/areas/{area_name}/builders/{area_name}_builder.py
        ↓
home/sections/{region}/...
        ↓
home/composition/dashboard_content_layout.py
        ↓
home/layout.py
        ↓
src/pages/dashboards/...
```

## No aparecen alarmas

Revisar:

* snapshot runtime de alarmas;
* configuración de alarmas;
* permisos del usuario;
* callbacks registrados;
* servicios internos de consulta;
* logs de Dash;
* errores de renderizado.

Contenedores relevantes:

```text
alarm_configuration
alarm_runtime_snapshot
alarm_management_messages
alarm_management_actions
```

Si el panel aparece vacío, distinguir entre:

| Caso                   | Revisión                       |
| ---------------------- | ------------------------------ |
| No hay alarmas activas | Validar snapshot runtime.      |
| Error de consulta      | Revisar Cosmos DB y logs.      |
| Error de renderizado   | Revisar callbacks/componentes. |
| Usuario sin permisos   | Revisar perfil/navegación.     |

## Falla conexión a Cosmos DB

Revisar variables:

```env
COSMOS_CONNECTION_MODE=""
COSMOS_DATABASE_NAME=""
COSMOS_ACCOUNT_URI=""
COSMOS_ACCOUNT_KEY=""
```

Casos frecuentes:

| Caso                              | Posible causa                                                   |
| --------------------------------- | --------------------------------------------------------------- |
| `COSMOS_CONNECTION_MODE="LOCAL"`  | Cosmos local no está levantado o puerto incorrecto.             |
| `COSMOS_CONNECTION_MODE="REMOTE"` | Credenciales Azure incorrectas o vacías.                        |
| URI local incorrecta              | Debe apuntar a `http://localhost:8081/` si se usa Cosmos local. |
| Base inexistente                  | `COSMOS_DATABASE_NAME` no coincide.                             |
| Contenedor inexistente            | Falta inicialización o publicación.                             |
| Key incorrecta                    | `COSMOS_ACCOUNT_KEY` inválida.                                  |

Contenedores esperados:

```text
active_user_sessions
alarm_configuration
alarm_management_actions
alarm_management_messages
alarm_runtime_snapshot
basic_analytics
kpi_configuration
kpi_runtime_snapshot
navigation_configuration
publication_state
```

## Falla Cosmos DB local

Levantar Cosmos local con:

Linux/macOS:

```bash
sh docker_files/linux_macos/cosmos.docker_deploy.sh
```

Windows:

```bat
docker_files\windows\cosmos.docker_deploy.bat
```

O manualmente:

```bash
docker compose -f docker-compose.cosmos.local.yml up --build
```

Revisar:

* `docker-compose.cosmos.local.yml`;
* puerto `8081`;
* contenedor Docker activo;
* configuración en `cosmosdb.configuration.txt`;
* variables activas en `.env`;
* `COSMOS_CONNECTION_MODE="LOCAL"`;
* `COSMOS_ACCOUNT_URI="http://localhost:8081/"`.

Archivos de referencia:

```text
docker_files/linux_macos/cosmosdb.configuration.txt
docker_files/windows/cosmosdb.configuration.txt
docker_files/cosmosdb.information.txt
```

## Falla SharePoint / DataEntry

Revisar variable:

```env
SHAREPOINT_ROOT_PATH=""
```

Posibles causas:

* ruta funcional incorrecta;
* permisos insuficientes;
* servicio no disponible;
* artefacto inexistente;
* configuración base no inicializada;
* error en integración o cliente SharePoint.

Revisar también:

* usuario o credencial usada;
* permisos sobre DataEntry;
* nombre de carpeta esperado;
* logs del servicio SharePoint/DataEntry.

## Falla autenticación

Revisar:

* Microsoft Entra ID;
* permisos del usuario;
* perfil asociado;
* rutas protegidas;
* middlewares;
* carga de identidad;
* sesión Flask;
* `SECRET_KEY`.

Síntomas comunes:

| Síntoma                       | Revisión                                 |
| ----------------------------- | ---------------------------------------- |
| Loop de login                 | Configuración de autenticación o sesión. |
| Usuario entra pero no ve menú | Perfil/navegación.                       |
| Usuario no autorizado         | Roles o permisos.                        |
| Error de sesión               | `SECRET_KEY` o cookies.                  |

## Error en callbacks Dash

Revisar:

* outputs duplicados;
* IDs inexistentes;
* stores no montados;
* callbacks no registrados;
* imports circulares;
* errores de serialización;
* exceptions en servicios llamados por el callback.

Reglas de diagnóstico:

1. identificar callback en error;
2. revisar `Input`, `State` y `Output`;
3. validar que los IDs existan en layout;
4. revisar si el callback se registró más de una vez;
5. mover lógica compleja a servicios si el callback es demasiado grande.

## Error de outputs duplicados

Síntomas:

* Dash indica que un output ya está siendo actualizado por otro callback;
* callbacks de módulos alternativos escriben al mismo componente.

Revisar:

* `src/app/bootstrap/callback_registry.py`;
* callbacks genéricos vs callbacks específicos;
* callbacks de dashboards;
* callbacks de alarmas;
* callbacks de administración.

Regla:

```text
Solo debe existir un callback activo por output, salvo que se use un patrón explícito permitido por Dash.
```

## No se registran callbacks nuevos

Revisar:

* que el callback esté en la función `register_*`;
* que esa función se invoque desde `callback_registry.py`;
* que no dependa de import por side effect;
* que no exista error de importación silencioso;
* que el layout contenga los IDs esperados.

Flujo recomendado:

```text
feature/callbacks.py
        ↓
register_feature_callbacks(app)
        ↓
src/app/bootstrap/callback_registry.py
```

## Problemas con contrato UI de dashboards

Si una nueva UI o dashboard no carga correctamente, revisar la separación:

```text
src/features/dashboards/
├── home/
└── {project_name}/
```

Recordar:

* `home` es contrato base;
* `{project_name}` aporta áreas/builders;
* `home` no vive dentro de `{project_name}`;
* `home/sections` importa builders generales desde `{project_name}/areas`;
* callbacks deben registrarse en bootstrap.

Errores frecuentes:

| Problema                       | Revisión                                           |
| ------------------------------ | -------------------------------------------------- |
| Import incorrecto              | Revisar ruta del builder general.                  |
| Builder no existe              | Crear función de alto nivel en área.               |
| Se importó componente profundo | Usar builder general del área.                     |
| Layout no aparece              | Revisar `home/layout.py` y `src/pages/dashboards`. |
| Callback no corre              | Revisar `callback_registry.py`.                    |

## Error 504 Gateway Timeout

Un 504 puede ocurrir cuando una petición tarda demasiado o el gateway/App Service no recibe respuesta a tiempo.

Revisar:

* callbacks lentos;
* consultas pesadas a Cosmos DB;
* llamadas lentas a SharePoint/DataEntry;
* timeouts de Gunicorn;
* capacidad del App Service Plan;
* Application Gateway si aplica;
* cantidad de workers y threads;
* operaciones pesadas dentro de callbacks.

Configuración actual en `gunicorn.config.py`:

```python
timeout = 90
```

Regla recomendada:

```text
La WebApp no debe ejecutar procesos pesados dentro de callbacks.
```

Si un callback tarda demasiado, evaluar:

* mover lógica a backend externo;
* usar snapshots preparados;
* reducir payload;
* optimizar consulta;
* devolver respuesta parcial;
* cachear contratos livianos;
* evitar reprocesar datos en Dash.

## Problemas con Gunicorn

Revisar archivo:

```text
gunicorn.config.py
```

Configuración base:

```python
bind = '0.0.0.0:8000'
worker_class = 'gthread'
loglevel = 'info'
timeout = 90
keepalive = 5
```

Workers y threads dependen de:

```env
FLASK_ENV=""
```

Configuración actual:

| `FLASK_ENV` | Workers | Threads |
| ----------- | ------: | ------: |
| `DEV`       |       1 |       2 |
| `UAT`       |       3 |       2 |
| Otro valor  |       1 |       2 |

Si los workers no corresponden:

* revisar `FLASK_ENV`;
* revisar variables inyectadas;
* revisar mapping file;
* revisar logs de arranque.

Logs esperados:

```text
[INFO] GUNICORN STARTUP
[INFO] ENV: <ambiente>
```

## No llegan logs a Application Insights

Revisar:

```env
APPLICATION_INSIGHTS_CONNECTION_STRING=""
```

En local puede ser:

```env
APPLICATION_INSIGHTS_CONNECTION_STRING="LOCAL"
```

En despliegue debe apuntar al recurso real.

Revisar además:

* configuración del App Service;
* recurso Application Insights correcto;
* integración con Log Analytics;
* permisos;
* errores de inicialización de logging.

## Problemas con despliegue

Revisar:

* `azure-pipelines.yml`;
* mapping file correcto;
* `dev.mapping-env.csv`;
* `uat.mapping-env.csv`;
* `prd.mapping-env.csv`;
* imagen Docker;
* variables inyectadas;
* Key Vault;
* logs del pipeline;
* logs del App Service.

Validar ambiente:

| Contexto | Valor esperado                             |
| -------- | ------------------------------------------ |
| DEV      | `dev.mapping-env.csv` + `FLASK_ENV="DEV"`  |
| UAT      | `uat.mapping-env.csv` + `FLASK_ENV="UAT"`  |
| PRD      | `prd.mapping-env.csv` + `FLASK_ENV="PROD"` |

## Problemas con Key Vault

Revisar:

* nombre de Key Vault usado por mapping;
* permisos del App Service;
* referencias configuradas;
* secretos existentes;
* nombres de secretos;
* acceso desde el ambiente;
* logs del App Service.

Síntomas:

* variables vacías;
* errores de conexión;
* claves no resueltas;
* app inicia pero falla al consultar servicios.

## Cambios de configuración no se reflejan

Revisar:

* configuración guardada en SharePoint/DataEntry;
* publicación hacia Cosmos DB;
* `publication_state`;
* ambiente correcto;
* caché o refresh pendiente;
* contenedor correcto;
* logs de consulta.

Contenedores frecuentes:

```text
publication_state
navigation_configuration
kpi_configuration
alarm_configuration
```

## Cosmos DB tiene datos distintos a SharePoint/DataEntry

Posibles causas:

* publicación pendiente;
* publicación fallida;
* Cosmos modificado manualmente;
* WebApp apuntando a otro ambiente;
* `SHAREPOINT_ROOT_PATH` incorrecto;
* `COSMOS_DATABASE_NAME` incorrecto.

Regla:

```text
SharePoint/DataEntry es la fuente administrable.
Cosmos DB es proyección publicada o runtime.
```

## La app carga pero se ve incompleta

Revisar:

* assets cargados;
* CSS;
* JavaScript;
* errores en consola del navegador;
* rutas de imágenes;
* permisos del usuario;
* callbacks fallidos;
* stores vacíos;
* configuración no publicada.

También revisar DevTools del navegador:

* errores JavaScript;
* recursos 404;
* errores de red;
* respuestas 500;
* callbacks fallidos.

## Problemas con assets

Revisar:

* carpeta `assets`;
* nombres de archivos;
* rutas relativas;
* caché del navegador;
* service worker si aplica;
* orden de carga CSS;
* errores en JavaScript.

Si un cambio visual no aparece:

* limpiar caché;
* reiniciar app;
* revisar nombre del archivo;
* validar que el archivo esté bajo `assets`.

## Problemas con sesiones de usuario

Revisar contenedor:

```text
active_user_sessions
```

Posibles causas:

* Cosmos no conecta;
* usuario no identificado;
* heartbeat no llega;
* ruta de sesión no responde;
* permisos o perfil incompleto;
* error en callbacks/client-side scripts.

## Checklist de diagnóstico rápido

| Pregunta                          | Archivo / lugar a revisar                     |
| --------------------------------- | --------------------------------------------- |
| ¿La app inicia?                   | Consola, logs App Service, Gunicorn.          |
| ¿El ambiente es correcto?         | `.env`, `FLASK_ENV`, mapping file.            |
| ¿Cosmos conecta?                  | Variables Cosmos, contenedores, logs.         |
| ¿SharePoint/DataEntry responde?   | `SHAREPOINT_ROOT_PATH`, permisos, logs.       |
| ¿La navegación existe?            | `navigation_configuration`, `--first-load`.   |
| ¿El usuario tiene perfil?         | Microsoft Entra ID, identidad, navegación.    |
| ¿Los callbacks están registrados? | `callback_registry.py`.                       |
| ¿Hay error 504?                   | callbacks lentos, Gunicorn, App Service Plan. |
| ¿Hay logs?                        | Application Insights, Log Analytics.          |
| ¿Cambios no aparecen?             | publicación, `publication_state`, ambiente.   |

## Reglas finales

* Revisar `.env` antes de ejecutar localmente.
* Revisar `FLASK_ENV` antes de diagnosticar workers o threads.
* No ejecutar `--first-load` sin validar destino.
* No manipular Cosmos DB como fuente primaria si SharePoint/DataEntry es la fuente oficial.
* No mover lógica pesada a callbacks para resolver timeouts.
* No registrar callbacks por side effects.
* No hardcodear secretos ni recursos.
* Revisar logs antes de modificar código.
