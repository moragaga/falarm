# Configuración y publicación

## Propósito

Este documento describe cómo ADA WebApp gestiona configuración funcional, artefactos administrables y publicación hacia Cosmos DB.

El objetivo es separar claramente:

* configuración administrable;
* publicación por ambiente;
* datos runtime consultables por la WebApp;
* responsabilidades entre SharePoint/DataEntry, Cosmos DB y la aplicación.

Este documento no cubre instalación local, variables de entorno ni despliegue técnico. Esos temas se documentan en archivos separados dentro de `/docs`.

## Principio general

SharePoint/DataEntry es la fuente administrable de configuración y artefactos funcionales.

Cosmos DB representa la configuración publicada, snapshots runtime y datos consultables por la WebApp en el ambiente actual.

La WebApp no debe tratar Cosmos DB como una fuente manual paralela de configuración cuando SharePoint/DataEntry sea la fuente oficial.

| Capa                   | Responsabilidad                                                             |
| ---------------------- | --------------------------------------------------------------------------- |
| SharePoint / DataEntry | Fuente administrable de configuración y artefactos funcionales.             |
| Cosmos DB              | Proyección publicada, snapshots runtime y datos consultables por la WebApp. |
| WebApp                 | Administración visual, consulta, renderizado e interacción del usuario.     |
| Pipeline / despliegue  | Inyección de configuración técnica por ambiente.                            |

## SharePoint / DataEntry

SharePoint/DataEntry contiene artefactos funcionales que pueden ser administrados por usuarios autorizados o procesos controlados.

Puede incluir:

* configuración de navegación;
* configuración de perfiles;
* configuración de KPIs;
* configuración de alarmas;
* mensajes de gestión;
* catálogos funcionales;
* parámetros editables;
* artefactos administrativos;
* archivos o estructuras base requeridas por la WebApp.

La ruta funcional de la aplicación dentro de SharePoint/DataEntry se define mediante:

```env
SHAREPOINT_ROOT_PATH=""
```

Ejemplo conceptual:

```text
DataEntry/{SHAREPOINT_ROOT_PATH}/...
```

El valor exacto de `SHAREPOINT_ROOT_PATH` depende de la aplicación o dominio funcional.

## Cosmos DB como proyección/runtime

Cosmos DB se utiliza para que la WebApp consulte información lista para consumo visual o administrativo.

Contenedores principales:

| Contenedor                  | Uso esperado                                                  |
| --------------------------- | ------------------------------------------------------------- |
| `active_user_sessions`      | Sesiones activas o recientes de usuarios.                     |
| `alarm_configuration`       | Configuración funcional relacionada con alarmas.              |
| `alarm_management_actions`  | Acciones de gestión de alarmas realizadas desde la WebApp.    |
| `alarm_management_messages` | Mensajes configurables asociados a gestión de alarmas.        |
| `alarm_runtime_snapshot`    | Snapshot runtime de alarmas listo para consumo visual.        |
| `basic_analytics`           | Datos agregados para analítica básica.                        |
| `kpi_configuration`         | Configuración funcional relacionada con KPIs.                 |
| `kpi_runtime_snapshot`      | Snapshot runtime de KPIs listo para consumo visual.           |
| `navigation_configuration`  | Configuración publicada de navegación, menú y rutas visibles. |
| `publication_state`         | Estado de publicación de artefactos de configuración.         |

Cosmos DB debe contener información publicada, runtime o consultable por la WebApp. No debería ser editado manualmente como fuente primaria si el artefacto correspondiente se administra desde SharePoint/DataEntry.

## Flujo conceptual de configuración

El flujo esperado es:

```text
SharePoint / DataEntry
        ↓
Validación / normalización
        ↓
Publicación controlada
        ↓
Cosmos DB
        ↓
Servicios internos WebApp
        ↓
Dash / UI
```

La WebApp puede tener paneles administrativos para modificar artefactos funcionales, pero esos cambios deben respetar el flujo de configuración definido.

## Primera carga: `--first-load`

La primera carga se ejecuta con:

```bash
python app.py --first-load
```

Esta acción inicializa la estructura mínima necesaria para que la WebApp pueda operar correctamente.

Responsabilidades principales:

| Inicialización                             | Descripción                                                                              |
| ------------------------------------------ | ---------------------------------------------------------------------------------------- |
| Configuración base en SharePoint/DataEntry | Crea o actualiza artefactos funcionales iniciales.                                       |
| Menú y navegación                          | Inicializa estructura base de navegación, rutas y menú.                                  |
| Proyección en Cosmos DB                    | Publica configuración mínima para que la WebApp pueda consultar navegación y datos base. |
| Usuarios administradores principales       | Crea o asegura usuarios/perfiles administradores iniciales de la aplicación.             |

## Riesgo operacional de `--first-load`

Antes de ejecutar:

```bash
python app.py --first-load
```

se debe revisar cuidadosamente el archivo `.env`.

Si `.env` apunta a recursos remotos, la ejecución puede modificar SharePoint/DataEntry y Cosmos DB del ambiente configurado.

Validar antes de ejecutar:

| Variable                 | Validación                                           |
| ------------------------ | ---------------------------------------------------- |
| `FLASK_ENV`              | Debe representar el ambiente esperado.               |
| `COSMOS_CONNECTION_MODE` | Debe ser `LOCAL` o `REMOTE` según corresponda.       |
| `COSMOS_DATABASE_NAME`   | Debe apuntar a la base correcta.                     |
| `COSMOS_ACCOUNT_URI`     | Debe apuntar al Cosmos correcto.                     |
| `SHAREPOINT_ROOT_PATH`   | Debe apuntar a la ruta funcional correcta.           |
| `APP_NAME`               | Debe corresponder a la aplicación esperada.          |
| `APP_SHORT_NAME`         | Debe corresponder a la abreviatura visible esperada. |

No se debe ejecutar `--first-load` contra un ambiente sin confirmar previamente las variables activas.

## Publicación de configuración

La publicación corresponde al proceso mediante el cual los artefactos administrables quedan disponibles para consulta runtime desde Cosmos DB.

La idea es que la WebApp no consuma configuración cruda de forma descontrolada, sino una versión publicada, consistente y consultable.

Ejemplo de artefactos publicables:

| Artefacto             | Fuente                 | Destino esperado            |
| --------------------- | ---------------------- | --------------------------- |
| Navegación            | SharePoint/DataEntry   | `navigation_configuration`  |
| Configuración KPI     | SharePoint/DataEntry   | `kpi_configuration`         |
| Configuración alarmas | SharePoint/DataEntry   | `alarm_configuration`       |
| Mensajes de gestión   | SharePoint/DataEntry   | `alarm_management_messages` |
| Estado de publicación | Proceso de publicación | `publication_state`         |


El contenedor `publication_state` representa el estado de publicación de artefactos.

Su objetivo es permitir identificar qué configuración está publicada y disponible para la WebApp en el ambiente actual.

Puede utilizarse para registrar información como:

* artefacto publicado;
* versión o revisión;
* hash o identificador de contenido;
* fecha de publicación;
* usuario o proceso responsable;
* estado de publicación;
* diferencias pendientes.

El objetivo no es duplicar toda la configuración, sino mantener trazabilidad sobre qué fue publicado hacia Cosmos DB.

## Navegación

La configuración de navegación es un caso crítico porque determina qué páginas o rutas puede ver el usuario.

Fuente administrable:

```text
SharePoint / DataEntry
```

Destino publicado:

```text
navigation_configuration
```

La WebApp utiliza esta configuración para:

* construir menú;
* resolver rutas visibles;
* filtrar opciones por perfil;
* habilitar o deshabilitar accesos;
* mantener navegación centralizada.

La navegación no debería quedar hardcodeada directamente en componentes visuales si existe un flujo administrable de configuración.

## Configuración de KPIs

La configuración de KPIs puede incluir artefactos funcionales necesarios para representar indicadores, nombres visibles, agrupaciones, ordenamiento o parámetros de visualización.

Fuente administrable:

```text
SharePoint / DataEntry
```

Destino publicado:

```text
kpi_configuration
```

La WebApp puede consultar esta configuración para renderizar vistas, paneles o elementos visuales relacionados con KPIs.

Los cálculos pesados de KPIs no pertenecen a la WebApp. La aplicación debe consumir snapshots o contratos preparados.

## Configuración de alarmas

La configuración de alarmas puede incluir reglas visuales, mensajes, definiciones administrables, textos de gestión o parámetros requeridos por la experiencia web.

Fuente administrable:

```text
SharePoint / DataEntry
```

Destinos publicados o runtime:

```text
alarm_configuration
alarm_management_messages
alarm_runtime_snapshot
alarm_management_actions
```

La WebApp puede permitir acciones de gestión sobre alarmas. Esas acciones deben persistirse en el contenedor correspondiente, manteniendo trazabilidad.

## Acciones de gestión de alarmas

Las acciones realizadas desde la WebApp deben quedar registradas en:

```text
alarm_management_actions
```

Este contenedor representa acciones generadas desde la experiencia visual.

Ejemplos conceptuales:

* gestión individual de alarma;
* solicitud de silencio;
* mensaje asociado a gestión;
* acción administrativa;
* trazabilidad de usuario;
* fecha/hora de ejecución.

La WebApp debe registrar estas acciones de forma controlada y consistente, evitando manipulación manual directa sobre Cosmos DB.

## Snapshots runtime

Los snapshots runtime representan información ya preparada para renderizar.

Ejemplos:

```text
kpi_runtime_snapshot
alarm_runtime_snapshot
```

La WebApp consume estos snapshots para evitar cálculos pesados dentro de callbacks o layouts.

Regla principal:

```text
La WebApp renderiza; no recalcula procesos pesados.
```

## Relación con ambientes

El README y la arquitectura son transversales para:

```text
DEV
UAT
PRD
```

Cada ambiente debe tener sus propios recursos y configuración publicada.

La WebApp se conecta al ambiente correspondiente mediante variables de entorno y configuración inyectada.

No se deben hardcodear nombres reales de recursos en el código.

Patrón conceptual:

```text
MLP-{Ambiente}-{Recurso}-{AbrevAPP}
```

Ejemplos:

```text
MLP-DEV-RG-ADAN1FS
MLP-UAT-APP-ADAN1FS
MLP-PRD-COSMOS-ADAN1FS
```

## Configuración local vs configuración desplegada

| Contexto        | Configuración activa                         |
| --------------- | -------------------------------------------- |
| Local           | `.env`                                       |
| Plantilla local | `.env.local`                                 |
| DEV desplegado  | `dev.mapping-env.csv` + Key Vault + pipeline |
| UAT desplegado  | `uat.mapping-env.csv` + Key Vault + pipeline |
| PRD desplegado  | `prd.mapping-env.csv` + Key Vault + pipeline |

La configuración funcional vive en SharePoint/DataEntry y se publica hacia Cosmos DB.
La configuración técnica de despliegue se resuelve mediante variables, mapping files, Key Vault y pipeline.

## Mapping de despliegue

Los archivos de mapping participan en el despliegue:

```text
dev.mapping-env.csv
uat.mapping-env.csv
prd.mapping-env.csv
```

Pueden contener:

* nombres de Key Vault;
* nombres de recursos Azure;
* variables del ambiente;
* parámetros del pipeline;
* valores no secretos;
* referencias técnicas de despliegue.

No deben reemplazar Key Vault para secretos sensibles.

## Reglas de seguridad

* No versionar `.env` si contiene secretos.
* No documentar claves reales.
* No dejar `SECRET_KEY` productiva en archivos de ejemplo.
* No dejar `COSMOS_ACCOUNT_KEY` productiva en documentación.
* Usar Key Vault para secretos de ambientes desplegados.
* No editar manualmente Cosmos DB como fuente primaria de configuración.
* Revisar `.env` antes de ejecutar `--first-load`.

## Checklist antes de publicar configuración

Antes de publicar configuración hacia Cosmos DB, validar:

| Validación                               | Resultado esperado                               |
| ---------------------------------------- | ------------------------------------------------ |
| Artefacto existe en SharePoint/DataEntry | La fuente administrable está disponible.         |
| Estructura válida                        | El artefacto cumple el contrato esperado.        |
| Ambiente correcto                        | La publicación apunta al Cosmos correspondiente. |
| Contenedor existe                        | El destino en Cosmos DB está disponible.         |
| Estado de publicación actualizado        | `publication_state` refleja la publicación.      |
| WebApp consulta correctamente            | La UI refleja la configuración publicada.        |
| No hay secretos expuestos                | Ningún artefacto contiene claves sensibles.      |

## Checklist después de `--first-load`

Después de ejecutar:

```bash
python app.py --first-load
```

validar:

| Validación               | Resultado esperado                                     |
| ------------------------ | ------------------------------------------------------ |
| SharePoint/DataEntry     | Artefactos base creados o actualizados.                |
| Navegación               | Configuración base disponible.                         |
| Cosmos DB                | Proyección mínima creada.                              |
| Usuarios administradores | Usuarios/perfiles iniciales disponibles.               |
| WebApp                   | Puede cargar menú y rutas base.                        |
| Logs                     | No existen errores críticos durante la inicialización. |

## Problemas frecuentes

### Se ejecutó `--first-load` contra el ambiente incorrecto

Revisar inmediatamente:

* `.env`;
* `FLASK_ENV`;
* `COSMOS_CONNECTION_MODE`;
* `COSMOS_ACCOUNT_URI`;
* `COSMOS_DATABASE_NAME`;
* `SHAREPOINT_ROOT_PATH`.

Luego validar qué artefactos fueron creados o modificados en SharePoint/DataEntry y Cosmos DB.

### La navegación no carga

Revisar:

* configuración base creada en SharePoint/DataEntry;
* contenedor `navigation_configuration`;
* publicación hacia Cosmos DB;
* perfil del usuario;
* logs de la WebApp.

### Cambios de configuración no se reflejan

Revisar:

* si el artefacto fue guardado en SharePoint/DataEntry;
* si fue publicado a Cosmos DB;
* si `publication_state` fue actualizado;
* si la WebApp está apuntando al ambiente correcto;
* si existe caché o refresh pendiente.

### Cosmos tiene datos distintos a SharePoint/DataEntry

Validar si existe una publicación pendiente o si Cosmos fue modificado manualmente.

La fuente administrable debe ser SharePoint/DataEntry. Cosmos DB representa una proyección publicada o runtime.

## Principios finales

* SharePoint/DataEntry es la fuente administrable.
* Cosmos DB es proyección publicada o runtime.
* La WebApp consume contratos listos para UI.
* La configuración técnica depende del ambiente.
* `--first-load` debe ejecutarse con extremo cuidado.
* Los secretos deben gestionarse fuera del código y documentación.
* La publicación debe ser trazable mediante `publication_state`.
