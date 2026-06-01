# Despliegue

## Propósito

Este documento describe el flujo de despliegue de ADA WebApp sobre Azure App Service.

El objetivo es explicar cómo se empaqueta, configura y publica la WebApp en los ambientes disponibles, manteniendo una base transversal para `DEV`, `UAT` y `PRD`.

Este documento no cubre ejecución local detallada, arquitectura general ni troubleshooting. Esos temas se documentan en archivos separados dentro de `/docs`.

## Estrategia general

ADA WebApp se despliega como una aplicación contenerizada sobre Azure App Service.

El despliegue se basa en:

| Elemento              | Rol                                                                         |
| --------------------- | --------------------------------------------------------------------------- |
| `Dockerfile`          | Define la imagen base de la WebApp. Es transversal para local y despliegue. |
| `azure-pipelines.yml` | Orquesta el proceso de CI/CD.                                               |
| `gunicorn.config.py`  | Define la ejecución runtime de la WebApp dentro del contenedor.             |
| `dev.mapping-env.csv` | Configuración inyectada para ambiente DEV.                                  |
| `uat.mapping-env.csv` | Configuración inyectada para ambiente UAT.                                  |
| `prd.mapping-env.csv` | Configuración inyectada para ambiente PRD.                                  |
| Azure App Service     | Ejecuta la WebApp desplegada.                                               |
| App Service Plan      | Define capacidad de cómputo, memoria, región y escala.                      |
| Azure Key Vault       | Centraliza secretos y referencias protegidas.                               |
| Application Insights  | Recibe trazas, errores y métricas de aplicación.                            |
| Log Analytics         | Centraliza logs y consultas operacionales.                                  |

## Ambientes

La WebApp está pensada para desplegarse en tres ambientes principales:

| Ambiente | Uso                                                                      |
| -------- | ------------------------------------------------------------------------ |
| `DEV`    | Desarrollo desplegado e integración temprana.                            |
| `UAT`    | Validación funcional, pruebas de usuario y revisión previa a producción. |
| `PRD`    | Operación productiva.                                                    |

En nombres de recursos y archivos de mapping se utiliza `PRD`.

En la variable `FLASK_ENV`, el valor esperado para producción es:

```env
FLASK_ENV="PROD"
```

Por lo tanto:

| Contexto                             | Valor esperado        |
| ------------------------------------ | --------------------- |
| Archivo de mapping productivo        | `prd.mapping-env.csv` |
| Ambiente lógico Flask productivo     | `FLASK_ENV="PROD"`    |
| Nomenclatura de recursos productivos | `PRD`                 |

## Nomenclatura de recursos

Los recursos Azure deben interpretarse usando el patrón transversal:

```text
MLP-{Ambiente}-{Recurso}-{AbrevAPP}
```

Donde:

| Variable     | Descripción                         | Ejemplo                                           |
| ------------ | ----------------------------------- | ------------------------------------------------- |
| `{Ambiente}` | Ambiente de despliegue.             | `DEV`, `UAT`, `PRD`                               |
| `{Recurso}`  | Tipo de recurso Azure.              | `RG`, `APP`, `ASP`, `COSMOS`, `KV`, `APPI`, `LAW` |
| `{AbrevAPP}` | Abreviatura única de la aplicación. | `ADAN1FS`, `ADA`, u otra definida                 |

Ejemplos conceptuales:

```text
MLP-DEV-RG-ADAN1FS
MLP-UAT-APP-ADAN1FS
MLP-PRD-COSMOS-ADAN1FS
```

El código fuente no debe hardcodear nombres reales de recursos. La resolución debe ocurrir mediante variables, archivos de mapping, Key Vault o configuración del servicio.

## Dockerfile

El `Dockerfile` es transversal y debe servir tanto para ejecución local como para despliegue.

Responsabilidades del `Dockerfile`:

* definir imagen base de Python;
* instalar dependencias del sistema si aplica;
* instalar dependencias Python;
* copiar el código fuente;
* preparar el entry point de ejecución;
* exponer la aplicación para App Service;
* mantener una construcción reproducible.

El `Dockerfile` no debe contener secretos ni valores específicos de ambiente.

Configuraciones como Cosmos, SharePoint/DataEntry, Application Insights o Key Vault deben resolverse por variables externas.

## Gunicorn

La WebApp desplegada se ejecuta mediante Gunicorn usando:

```text
gunicorn.config.py
```

Configuración base actual:

```python
bind = '0.0.0.0:8000'
worker_class = 'gthread'
loglevel = 'info'
timeout = 90
keepalive = 5
```

Significado:

| Parámetro      | Uso                                                              |
| -------------- | ---------------------------------------------------------------- |
| `bind`         | Expone la aplicación en el puerto interno del contenedor.        |
| `worker_class` | Define el tipo de worker Gunicorn.                               |
| `loglevel`     | Controla el nivel de logs.                                       |
| `timeout`      | Define el tiempo máximo antes de considerar un worker bloqueado. |
| `keepalive`    | Mantiene conexiones persistentes por un tiempo limitado.         |

## Workers y threads por ambiente

La cantidad de workers y threads depende de:

```env
FLASK_ENV
```

Configuración actual:

| `FLASK_ENV` | Workers | Threads | Uso esperado                                                                               |
| ----------- | ------: | ------: | ------------------------------------------------------------------------------------------ |
| `DEV`       |       1 |       2 | Desarrollo desplegado.                                                                     |
| `UAT`       |       3 |       2 | Validación con mayor concurrencia.                                                         |
| Otro valor  |       1 |       2 | Comportamiento genérico para `LOCAL`, `PROD` u otros valores no declarados explícitamente. |

Nota importante:

Actualmente `PROD` no tiene un bloque específico en el ejemplo de `gunicorn.config.py`. Si producción requiere una configuración distinta, debe declararse explícitamente para evitar que caiga en el bloque genérico `else`.

Ejemplo esperado si se define producción explícitamente en el futuro:

```python
elif env == 'PROD':
    workers = 3
    threads = 2
```

La configuración final debe validarse según capacidad real del App Service Plan, consumo de memoria, tiempo de respuesta y nivel esperado de concurrencia.

## App Service Plan

El App Service Plan define la capacidad disponible para la WebApp.

Aspectos que condiciona:

* CPU;
* memoria;
* región;
* escalabilidad;
* cantidad de instancias;
* capacidad de atender concurrencia;
* estabilidad frente a carga.

La configuración de Gunicorn debe ser coherente con el App Service Plan.

Aumentar workers o threads sin validar memoria y CPU puede generar degradación, reinicios o timeouts.

## App Service

Azure App Service ejecuta la WebApp contenerizada.

Responsabilidades esperadas:

* levantar el contenedor;
* exponer la aplicación;
* inyectar variables de entorno;
* resolver configuración del servicio;
* integrarse con observabilidad;
* conectarse a Key Vault si aplica;
* permitir diagnóstico y reinicio controlado.

El App Service debe recibir la configuración del ambiente desde pipeline, variables de App Service o referencias seguras.

## Archivos de mapping por ambiente

Los archivos de mapping definen configuración que será inyectada durante el despliegue.

```text
dev.mapping-env.csv
uat.mapping-env.csv
prd.mapping-env.csv
```

Uso esperado:

| Archivo               | Ambiente |
| --------------------- | -------- |
| `dev.mapping-env.csv` | DEV      |
| `uat.mapping-env.csv` | UAT      |
| `prd.mapping-env.csv` | PRD      |

Estos archivos pueden contener:

* nombres de Key Vault;
* nombres de recursos Azure;
* nombres de App Service;
* nombres de Application Insights;
* nombres de Log Analytics;
* nombres de Cosmos DB;
* variables no secretas;
* parámetros usados por el pipeline;
* referencias necesarias para inyección de configuración.

Los mapping files pueden contener datos crudos de despliegue, pero no deben reemplazar Key Vault para secretos sensibles.

## Key Vault

Azure Key Vault debe usarse para secretos y referencias protegidas.

Ejemplos de información que debe resolverse de forma segura:

* claves de Cosmos DB;
* connection strings;
* secretos internos;
* tokens;
* claves de sesión si aplica;
* valores sensibles requeridos por la WebApp.

Regla principal:

```text
Los secretos no deben vivir hardcodeados en el código ni en documentación.
```

## Variables de entorno en despliegue

En ambientes desplegados, la WebApp debe recibir variables desde:

* pipeline;
* mapping files;
* Key Vault;
* configuración del App Service;
* variables seguras del ambiente.

Variables relevantes:

| Variable                                 | Uso                                                |
| ---------------------------------------- | -------------------------------------------------- |
| `FLASK_ENV`                              | Ambiente lógico y configuración Gunicorn.          |
| `APPLICATION_INSIGHTS_CONNECTION_STRING` | Observabilidad.                                    |
| `COSMOS_CONNECTION_MODE`                 | Modo de conexión a Cosmos.                         |
| `COSMOS_DATABASE_NAME`                   | Base de datos Cosmos.                              |
| `COSMOS_ACCOUNT_URI`                     | Endpoint Cosmos.                                   |
| `COSMOS_ACCOUNT_KEY`                     | Clave Cosmos, idealmente resuelta desde Key Vault. |
| `SHAREPOINT_ROOT_PATH`                   | Ruta funcional dentro de DataEntry.                |
| `APP_NAME`                               | Nombre visible de la aplicación.                   |
| `APP_SHORT_NAME`                         | Nombre corto visible.                              |
| `SECRET_KEY`                             | Clave Flask segura.                                |

En despliegues Azure, `COSMOS_CONNECTION_MODE` normalmente debe ser:

```env
COSMOS_CONNECTION_MODE="REMOTE"
```

## Pipeline CI/CD

El archivo:

```text
azure-pipelines.yml
```

orquesta el proceso de integración y despliegue.

Responsabilidades esperadas del pipeline:

* seleccionar ambiente;
* leer mapping correspondiente;
* resolver variables;
* construir imagen Docker;
* publicar imagen o artefacto según estrategia definida;
* configurar App Service;
* inyectar variables requeridas;
* desplegar la WebApp;
* validar resultado del despliegue.

Flujo conceptual:

```text
Repositorio
    ↓
Pipeline
    ↓
Mapping por ambiente
    ↓
Resolución de variables / Key Vault
    ↓
Build Docker
    ↓
Deploy App Service
    ↓
Validación
```

## Relación entre Docker y despliegue

El mismo `Dockerfile` debe servir para local y despliegue.

La diferencia no debe estar en la imagen base, sino en la configuración externa.

| Contexto | Configuración                                |
| -------- | -------------------------------------------- |
| Local    | `.env`                                       |
| DEV      | `dev.mapping-env.csv` + Key Vault + pipeline |
| UAT      | `uat.mapping-env.csv` + Key Vault + pipeline |
| PRD      | `prd.mapping-env.csv` + Key Vault + pipeline |

Esto permite mantener una construcción consistente y despliegues predecibles.

## Observabilidad

La observabilidad debe apuntar principalmente al App Service.

Application Insights y Log Analytics deben permitir revisar:

* errores de aplicación;
* excepciones en callbacks;
* errores de rutas Flask;
* tiempos de respuesta;
* reinicios;
* fallas de conexión;
* timeouts;
* trazas relevantes de operación;
* comportamiento de sesiones si aplica.

Variable principal:

```env
APPLICATION_INSIGHTS_CONNECTION_STRING=""
```

En local puede usarse:

```env
APPLICATION_INSIGHTS_CONNECTION_STRING="LOCAL"
```

En ambientes desplegados debe usarse la connection string real del recurso Application Insights.

## SharePoint / DataEntry en despliegue

La WebApp debe recibir la ruta funcional de la aplicación mediante:

```env
SHAREPOINT_ROOT_PATH=""
```

Este valor permite ubicar los artefactos funcionales de la aplicación dentro de DataEntry.

Ejemplo conceptual:

```text
DataEntry/{SHAREPOINT_ROOT_PATH}/...
```

El valor debe ser coherente con la aplicación desplegada.

## Cosmos DB en despliegue

En ambientes desplegados, Cosmos DB corresponde al recurso remoto del ambiente.

Variables requeridas:

```env
COSMOS_CONNECTION_MODE="REMOTE"
COSMOS_DATABASE_NAME=""
COSMOS_ACCOUNT_URI=""
COSMOS_ACCOUNT_KEY=""
```

Contenedores esperados:

| Contenedor                  | Uso                                 |
| --------------------------- | ----------------------------------- |
| `active_user_sessions`      | Sesiones activas o recientes.       |
| `alarm_configuration`       | Configuración funcional de alarmas. |
| `alarm_management_actions`  | Acciones de gestión de alarmas.     |
| `alarm_management_messages` | Mensajes configurables de gestión.  |
| `alarm_runtime_snapshot`    | Snapshot runtime de alarmas.        |
| `basic_analytics`           | Analítica básica.                   |
| `kpi_configuration`         | Configuración funcional de KPIs.    |
| `kpi_runtime_snapshot`      | Snapshot runtime de KPIs.           |
| `navigation_configuration`  | Configuración de navegación.        |
| `publication_state`         | Estado de publicación.              |

## Primera carga en ambiente desplegado

La primera carga puede ejecutarse con:

```bash
python app.py --first-load
```

Esta acción puede crear o actualizar:

* configuración base en SharePoint/DataEntry;
* navegación base;
* proyección mínima en Cosmos DB;
* usuarios administradores principales.

Advertencia:

```text
No ejecutar --first-load en un ambiente desplegado sin validar variables y destino.
```

Antes de ejecutar, validar:

* `FLASK_ENV`;
* `COSMOS_CONNECTION_MODE`;
* `COSMOS_DATABASE_NAME`;
* `COSMOS_ACCOUNT_URI`;
* `SHAREPOINT_ROOT_PATH`;
* `APP_NAME`;
* `APP_SHORT_NAME`.

## Validaciones posteriores al despliegue

Después de desplegar, validar:

| Validación                | Resultado esperado                                       |
| ------------------------- | -------------------------------------------------------- |
| App Service activo        | El servicio está iniciado y sin reinicios constantes.    |
| Contenedor levantado      | La imagen se ejecuta correctamente.                      |
| Gunicorn activo           | Logs muestran inicio de Gunicorn.                        |
| `FLASK_ENV` correcto      | El ambiente lógico corresponde al despliegue.            |
| Workers/threads esperados | Gunicorn usa la configuración esperada para el ambiente. |
| Autenticación             | Microsoft Entra ID permite iniciar sesión.               |
| Navegación                | Menú y rutas cargan según perfil.                        |
| Cosmos DB                 | La WebApp consulta contenedores esperados.               |
| SharePoint/DataEntry      | La ruta configurada responde correctamente.              |
| Key Vault                 | Secretos se resuelven correctamente.                     |
| Application Insights      | Se reciben trazas y errores.                             |
| Log Analytics             | Logs disponibles para consulta.                          |
| Dash callbacks            | No existen errores críticos en callbacks principales.    |

## Validación de logs de arranque

En logs de arranque debe aparecer información equivalente a:

```text
[INFO] GUNICORN STARTUP
[INFO] ENV: <ambiente>
```

Esto permite confirmar que Gunicorn está leyendo `FLASK_ENV`.

Si el ambiente mostrado no corresponde al esperado, revisar:

* variables inyectadas por pipeline;
* mapping file utilizado;
* configuración del App Service;
* valores resueltos desde Key Vault.

## Timeouts

La configuración actual define:

```python
timeout = 90
```

Esto significa que un worker puede ser terminado si supera el tiempo de espera definido.

Si aparecen errores 504, timeouts o callbacks demasiado largos, revisar:

* callbacks lentos;
* consultas a Cosmos DB;
* llamadas a SharePoint/DataEntry;
* cantidad de workers y threads;
* capacidad del App Service Plan;
* logs en Application Insights;
* configuración del Application Gateway si aplica;
* operaciones pesadas que no deberían ejecutarse dentro de la WebApp.

Regla recomendada:

```text
La WebApp no debe ejecutar procesos pesados dentro de callbacks.
```

## Rollback

Si un despliegue falla, la estrategia de rollback depende del pipeline y del método de publicación de imagen.

Revisar:

* versión anterior de imagen;
* última ejecución exitosa del pipeline;
* configuración previa de variables;
* cambios recientes en mapping files;
* cambios en Key Vault;
* cambios en `gunicorn.config.py`;
* cambios en dependencias;
* logs de App Service.

Antes de hacer rollback, identificar si la falla proviene de:

| Origen          | Ejemplo                                                               |
| --------------- | --------------------------------------------------------------------- |
| Código          | Error de importación, callback roto, dependencia faltante.            |
| Configuración   | Variable ausente, Key Vault incorrecto, mapping errado.               |
| Infraestructura | App Service detenido, Cosmos no disponible, permisos.                 |
| Datos           | Configuración no publicada, snapshot ausente, SharePoint inaccesible. |

## Checklist previo a despliegue

Antes de desplegar, validar:

| Validación                     | Resultado esperado                              |
| ------------------------------ | ----------------------------------------------- |
| Rama correcta                  | Se despliega desde la rama esperada.            |
| `Dockerfile` válido            | Construye imagen sin errores.                   |
| `requirements.txt` actualizado | Dependencias necesarias declaradas.             |
| Mapping correcto               | Se usa el archivo del ambiente correspondiente. |
| Secretos protegidos            | No existen secretos en código ni mapping.       |
| Key Vault disponible           | Referencias resuelven correctamente.            |
| `FLASK_ENV` correcto           | Coincide con el ambiente esperado.              |
| `gunicorn.config.py` validado  | Workers y threads adecuados.                    |
| Imagen construida              | Build finaliza correctamente.                   |
| App Service disponible         | Recurso activo y listo para recibir despliegue. |

## Checklist posterior a despliegue

Después de desplegar, validar:

| Validación           | Resultado esperado                        |
| -------------------- | ----------------------------------------- |
| URL responde         | La WebApp carga correctamente.            |
| Login funciona       | El usuario puede autenticarse.            |
| Menú carga           | Navegación visible según perfil.          |
| Dashboards cargan    | Layouts principales renderizan.           |
| Alarmas cargan       | Paneles de alarmas responden si aplica.   |
| Admin funciona       | Paneles administrativos cargan si aplica. |
| Cosmos conecta       | No hay errores de conexión.               |
| SharePoint conecta   | No hay errores de DataEntry.              |
| Logs llegan          | Application Insights recibe trazas.       |
| Sin errores críticos | No hay excepciones repetitivas en logs.   |

## Problemas frecuentes

### El despliegue termina, pero la app no levanta

Revisar:

* logs del App Service;
* logs de Gunicorn;
* errores de importación;
* dependencias faltantes;
* variables ausentes;
* `FLASK_ENV`;
* `SECRET_KEY`.

### La app levanta, pero no carga navegación

Revisar:

* `navigation_configuration`;
* ejecución de `--first-load`;
* publicación de configuración;
* perfil del usuario;
* `SHAREPOINT_ROOT_PATH`.

### Error de conexión a Cosmos DB

Revisar:

* `COSMOS_CONNECTION_MODE`;
* `COSMOS_DATABASE_NAME`;
* `COSMOS_ACCOUNT_URI`;
* `COSMOS_ACCOUNT_KEY`;
* Key Vault;
* firewall/red;
* existencia de contenedores.

### Error de SharePoint/DataEntry

Revisar:

* `SHAREPOINT_ROOT_PATH`;
* permisos;
* conectividad;
* credenciales;
* disponibilidad del servicio.

### Logs no aparecen en Application Insights

Revisar:

* `APPLICATION_INSIGHTS_CONNECTION_STRING`;
* configuración del App Service;
* recurso Application Insights correcto;
* integración con Log Analytics.

### Workers no corresponden al ambiente

Revisar:

* `FLASK_ENV`;
* `gunicorn.config.py`;
* variables inyectadas por pipeline;
* mapping file usado.

## Reglas importantes

* El `Dockerfile` debe ser transversal para local y despliegue.
* Las diferencias entre ambientes deben resolverse por configuración externa.
* No hardcodear nombres de recursos Azure en código.
* No versionar secretos.
* Usar Key Vault para secretos reales.
* Validar `FLASK_ENV`, porque afecta workers y threads.
* Revisar `gunicorn.config.py` antes de cambios de concurrencia.
* No ejecutar `--first-load` en ambientes remotos sin validar destino.
* La observabilidad debe apuntar al App Service.
* La WebApp no debe ejecutar procesos pesados dentro de callbacks.
