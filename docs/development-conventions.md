# Convenciones de desarrollo

## Propósito

Este documento define las convenciones de desarrollo para ADA WebApp.

El objetivo es mantener una base de código ordenada, modular, escalable y fácil de mantener, evitando acoplamiento innecesario entre Flask, Dash, features, servicios internos, infraestructura compartida y componentes visuales.

Este documento no describe arquitectura general, ejecución local, variables de entorno ni despliegue. Esos temas se documentan en archivos separados dentro de `/docs`.

## Principios generales

La WebApp debe seguir estos principios:

* separar presentación, configuración, runtime e infraestructura;
* mantener callbacks Dash delgados;
* delegar lógica en servicios, builders, mappers o repositories;
* registrar callbacks explícitamente;
* evitar imports por side effect;
* no hardcodear ambientes, recursos Azure ni secretos;
* reutilizar componentes visuales desde `src/shared/ui`;
* reutilizar infraestructura desde `src/shared/infrastructure`;
* mantener la lógica funcional dentro de `src/features`;
* mantener páginas Dash en `src/pages`;
* mantener inicialización, extensiones y dependencias en `src/app`.

## Separación de capas

| Capa           | Responsabilidad                                                                                      |
| -------------- | ---------------------------------------------------------------------------------------------------- |
| `src/app`      | Inicialización Flask/Dash, extensiones, dependencias, rutas, middlewares, autenticación y bootstrap. |
| `src/pages`    | Páginas Dash navegables y conexión con layouts principales.                                          |
| `src/features` | Funcionalidades agrupadas por dominio.                                                               |
| `src/shared`   | Infraestructura, UI, utilidades y componentes transversales.                                         |
| `assets`       | CSS, JavaScript, imágenes, iconos, manifest y recursos servidos por Dash.                            |

## `src/app`

La capa `src/app` contiene el arranque y configuración global de la WebApp.

Responsabilidades:

* crear la aplicación Flask;
* inicializar Dash;
* registrar rutas;
* configurar middlewares;
* inicializar servicios globales;
* exponer dependencias;
* registrar callbacks;
* registrar layouts;
* resolver configuración de entorno;
* configurar logging.

Archivos relevantes:

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

## Servicios globales

Los servicios globales deben inicializarse en:

```text
src/app/extensions.py
```

Ejemplos:

* cliente o servicio Cosmos;
* servicio SharePoint/DataEntry;
* servicios de navegación;
* servicios de identidad;
* servicios de analítica o runtime requeridos por la WebApp.

El acceso a esos servicios debe hacerse mediante:

```text
src/app/dependencies.py
```

Esto evita acoplar las features directamente a detalles de inicialización de Flask o `app.extensions`.

Regla recomendada:

```text
features -> dependencies.py -> app.extensions
```

Evitar:

```text
features -> current_app.extensions[...] directamente en múltiples lugares
```

salvo casos justificados y centralizados.

## Bootstrap y registro de callbacks

Los callbacks deben registrarse explícitamente desde la capa de bootstrap.

Referencia:

```text
src/app/bootstrap/callback_registry.py
```

No se deben activar callbacks únicamente por importar módulos con side effects.

Correcto:

```text
callback_registry.py
    -> register_dashboard_callbacks(app)
    -> register_alarm_callbacks(app)
    -> register_admin_callbacks(app)
```

Evitar:

```text
import src.features.some_feature.callbacks
```

si el único propósito del import es ejecutar código al cargar el módulo.

El registro explícito permite:

* saber qué callbacks están activos;
* controlar qué módulos se montan por aplicación;
* evitar duplicidad de outputs;
* mejorar trazabilidad;
* facilitar pruebas;
* desacoplar features.

## Callbacks Dash

Los callbacks Dash deben ser lo más delgados posible.

Responsabilidades esperadas de un callback:

* leer inputs y states;
* validar condiciones mínimas;
* llamar servicios internos;
* mapear respuesta a componentes visuales;
* manejar errores esperados;
* retornar outputs.

Evitar en callbacks:

* consultas complejas directas a infraestructura;
* lógica de negocio extensa;
* normalización pesada de datos;
* cálculos intensivos;
* manipulación de configuración cruda;
* imports dinámicos innecesarios;
* dependencias circulares.

Patrón recomendado:

```text
callback
  -> service
  -> repository / infrastructure
  -> mapper / builder
  -> UI output
```

## Manejo de errores en callbacks

Los callbacks deben distinguir entre:

| Caso                           | Manejo recomendado                                        |
| ------------------------------ | --------------------------------------------------------- |
| No hay actualización requerida | `PreventUpdate` si corresponde.                           |
| Input incompleto               | Retornar fallback visual o estado vacío.                  |
| Error esperado de datos        | Mostrar mensaje controlado y registrar log.               |
| Error técnico inesperado       | Registrar excepción y retornar fallback seguro si aplica. |

Evitar que un error no crítico rompa toda la experiencia visual.

## `src/pages`

La carpeta `src/pages` debe contener páginas navegables.

Responsabilidades:

* declarar páginas Dash;
* conectar rutas con layouts principales;
* importar layouts desde features;
* mantener páginas delgadas;
* evitar lógica funcional compleja.

Ejemplo:

```text
src/pages/
├── admin_panels/
├── analytics/
└── dashboards/
```

Una página no debería construir todo el contenido por sí misma si existe una feature responsable.

## `src/features`

La carpeta `src/features` contiene funcionalidades agrupadas por dominio.

Ejemplo:

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

Cada feature debe agrupar su lógica interna:

```text
feature/
├── callbacks/
├── components/
├── services/
├── repositories/
├── models/
├── mappers/
├── builders/
├── definitions/
└── ids.py
```

No todas las carpetas son obligatorias. Se deben crear solo cuando aporten responsabilidad real.

## Dashboards

Los dashboards deben respetar la separación entre contrato base y proyecto específico.

Contrato base:

```text
src/features/dashboards/home/
```

Proyecto específico:

```text
src/features/dashboards/{project_name}/
```

Regla principal:

* `home` mantiene la estructura visual base.
* `{project_name}` expone áreas, builders, componentes, definiciones, KPIs y series.
* `home/sections` importa builders generales del proyecto.
* No se debe crear un `home` por cada proyecto si se reutiliza el contrato base.
* No se debe mover lógica específica del proyecto dentro de `home`.

Flujo recomendado:

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

## Builders

Los builders construyen componentes, regiones o layouts a partir de modelos o contratos preparados.

Deben:

* recibir datos ya normalizados cuando sea posible;
* construir componentes visuales;
* evitar consultas directas a infraestructura;
* mantener nombres claros;
* ser reutilizables dentro del dominio correspondiente.

Ejemplo:

```text
build_aguas_abajo_rows()
build_aguas_abajo_ready_flag()
```

## Mappers

Los mappers transforman datos entre capas.

Usos típicos:

* convertir contratos runtime en modelos visuales;
* adaptar respuestas de servicios a props de componentes;
* normalizar nombres o estructuras para UI;
* reducir lógica de transformación dentro de callbacks.

Los mappers no deberían consultar infraestructura ni modificar estado externo.

## Services

Los services concentran lógica funcional o coordinación.

Responsabilidades:

* consultar repositories;
* aplicar reglas de negocio livianas del lado web;
* coordinar datos para UI;
* validar contratos;
* preparar respuestas para mappers/builders.

Un service no debería depender de componentes Dash si su lógica puede mantenerse independiente.

## Repositories

Los repositories encapsulan acceso a fuentes externas o persistencia.

Ejemplos:

* Cosmos DB;
* SharePoint/DataEntry;
* APIs internas;
* archivos o recursos de infraestructura.

Regla:

```text
services -> repositories -> infrastructure
```

Evitar que callbacks o builders consulten directamente Cosmos DB o SharePoint/DataEntry.

## `src/shared`

La carpeta `src/shared` contiene código transversal.

```text
src/shared/
├── formatters/
├── infrastructure/
├── runtime/
├── time/
└── ui/
```

## `src/shared/ui`

Debe contener componentes visuales reutilizables por múltiples features.

Ejemplos:

* cards genéricas;
* shells;
* grids;
* botones reutilizables;
* wrappers visuales;
* componentes base de layout.

Regla:

```text
Si un componente puede ser usado por más de una feature, evaluar moverlo a src/shared/ui.
```

## `src/shared/infrastructure`

Debe contener infraestructura transversal.

Ejemplos:

* clientes Cosmos;
* clientes SharePoint/DataEntry;
* servicios HTTP;
* wrappers de autenticación técnica;
* utilidades de acceso a recursos externos.

Regla:

```text
La infraestructura compartida no debe depender de componentes visuales.
```

## Assets

La carpeta `assets` contiene recursos servidos automáticamente por Dash.

Puede incluir:

* CSS;
* JavaScript;
* imágenes;
* iconos;
* manifest;
* service worker;
* recursos visuales estáticos.

Convenciones JavaScript:

* usar sintaxis ECMAScript moderna;
* preferir `const` y `let`;
* preferir arrow functions;
* evitar `function` salvo que sea necesario por scope;
* mantener scripts separados por responsabilidad;
* evitar lógica de negocio en JavaScript de assets.

## CSS

El CSS debe mantenerse organizado y con nombres claros.

Recomendaciones:

* evitar selectores excesivamente globales;
* usar clases con prefijos cuando correspondan;
* centralizar variables visuales;
* no modificar clases compartidas si son usadas por varias features sin revisar impacto;
* separar CSS de loader, navegación, dashboards, alarmas y componentes cuando sea necesario.

## IDs Dash

Los IDs deben ser explícitos, consistentes y preferentemente centralizados.

Recomendación:

```text
ids.py
```

por feature o módulo cuando existan IDs reutilizados en callbacks/componentes.

Para IDs dinámicos, preferir builders o helpers claros.

Ejemplo conceptual:

```python
def build_alarm_card_id(alarm_id: str) -> dict:
    return {
        'type': 'alarm-card',
        'alarm_id': alarm_id,
    }
```

## Configuración vs runtime vs presentación

Mantener separación clara:

| Concepto                    | Capa esperada                                    |
| --------------------------- | ------------------------------------------------ |
| Configuración administrable | SharePoint/DataEntry, features de configuración. |
| Publicación/runtime         | Cosmos DB, services runtime.                     |
| Presentación                | Dash layouts, components, builders.              |
| Infraestructura             | `src/shared/infrastructure`.                     |

La presentación no debe manipular directamente configuración cruda si existe una capa de servicio o publicación.

## Variables y ambientes

No hardcodear:

* nombres de recursos Azure;
* nombres de Key Vault;
* endpoints;
* claves;
* rutas de ambiente;
* connection strings.

Usar:

* `.env` en local;
* mapping files en despliegue;
* Key Vault para secretos;
* variables de App Service o pipeline.

## Gunicorn y concurrencia

`gunicorn.config.py` define la configuración runtime cuando la WebApp se ejecuta con Gunicorn.

La variable:

```text
FLASK_ENV
```

afecta workers y threads.

Configuración actual:

| `FLASK_ENV` | Workers | Threads |
| ----------- | ------: | ------: |
| `DEV`       |       1 |       2 |
| `UAT`       |       3 |       2 |
| Otro valor  |       1 |       2 |

Si se requiere comportamiento específico para `PROD`, debe declararse explícitamente.

Los cambios en workers y threads deben validarse con:

* capacidad del App Service Plan;
* uso de memoria;
* tiempos de respuesta;
* errores 504;
* logs de Application Insights;
* comportamiento de callbacks.

## Calidad de código

Usar Ruff para linting y formato:

```bash
ruff check . --fix
ruff format .
```

Criterios esperados:

* imports ordenados;
* comillas simples según configuración del proyecto;
* formato consistente;
* eliminación de imports no usados;
* evitar archivos legacy;
* evitar aliases temporales innecesarios;
* mantener nombres expresivos.

## Tipado

Se recomienda usar type hints en servicios, mappers, builders, repositories y modelos.

Priorizar tipado en:

* modelos;
* contratos de servicios;
* repositorios;
* mappers;
* funciones públicas;
* helpers compartidos.

## Logging

Los logs deben ayudar a diagnosticar sin exponer secretos.

Recomendaciones:

* usar mensajes claros;
* incluir contexto útil;
* no loguear claves ni connection strings;
* distinguir `[INFO]`, `[WARNING]`, `[ERROR]` cuando aplique;
* registrar excepciones técnicas relevantes;
* evitar ruido excesivo en callbacks muy frecuentes.

## Secretos

Nunca dejar en código o documentación:

* `COSMOS_ACCOUNT_KEY`;
* `SECRET_KEY` productiva;
* connection strings productivas;
* tokens;
* passwords;
* claves de servicios.

Si un secreto se publica accidentalmente, debe rotarse.

## Archivos que no deben versionarse

No versionar:

```text
.env
.venv/
venv/
__pycache__/
.ruff_cache/
.mypy_cache/
archivos temporales locales
cachés locales
```

`.env.local` puede versionarse solo si funciona como plantilla y no contiene secretos reales.

## Criterio para agregar nueva funcionalidad

Antes de crear archivos nuevos, responder:

| Pregunta                                   | Ubicación probable                                       |
| ------------------------------------------ | -------------------------------------------------------- |
| ¿Es una nueva página?                      | `src/pages`                                              |
| ¿Es una nueva feature funcional?           | `src/features/{feature_name}`                            |
| ¿Es parte de un dashboard específico?      | `src/features/dashboards/{project_name}`                 |
| ¿Es parte del contrato base de dashboards? | `src/features/dashboards/home`                           |
| ¿Es un componente reusable?                | `src/shared/ui`                                          |
| ¿Es infraestructura transversal?           | `src/shared/infrastructure`                              |
| ¿Es inicialización global?                 | `src/app/extensions.py`                                  |
| ¿Es acceso a dependencia global?           | `src/app/dependencies.py`                                |
| ¿Es callback nuevo?                        | Registrar desde `src/app/bootstrap/callback_registry.py` |

## Reglas finales

* No mezclar lógica específica de proyecto en contratos base.
* No poner lógica pesada en callbacks.
* No consultar infraestructura directamente desde componentes visuales.
* No registrar callbacks por side effects.
* No hardcodear ambientes.
* No versionar secretos.
* No duplicar componentes si pueden vivir en `shared`.
* No crear capas si no tienen responsabilidad real.
* Mantener nombres explícitos y estructura simple.
