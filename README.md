# RepoTareWEB-API

Repositorio que engloba una pequeña plataforma de ejemplo compuesta por:

- **API REST en Flask** para crear y listar elementos en memoria.
- **Frontend mínimo en Flask** que expone una página HTML.
- **Manifiestos de Kubernetes** para desplegar ambos servicios en un clúster.
- **Guía operativa** (`ComandosDeCreacion.txt`) con los pasos para preparar secretos y ConfigMaps.

---

## Estructura de carpetas

| Carpeta / Archivo | Descripción |
| --- | --- |
| `tareaAPI/app.py` | API REST con endpoints `GET/POST /api/items`, `/` y `/healthz`. |
| `tareaAPI/Dockerfile` | Imagen basada en `python:3.9-slim` que instala Flask y expone el puerto 5000. |
| `tareaWEB/app.py` | Servicio web minimalista que responde con `Web Funcionando!`. |
| `tareaWEB/Dockerfile` | Imagen Flask idéntica a la de la API, enfocada al frontend. |
| `tareaK8s/*.yaml` | Despliegues y Services tipo `LoadBalancer` para los pods `api` y `web`. |
| `ComandosDeCreacion.txt` | Secuencia sugerida de `kubectl` para namespace, secretos y ConfigMaps. |

---

## Servicios incluidos

### API Flask (`tareaAPI`)

- Endpoint raíz (`/`) para verificación rápida: responde **API Funcionando!**
- `/healthz` entrega `200 OK` para chequeos de vida.
- `/api/items`
  - `GET`: devuelve un JSON `{ items: [], count: n }`.
  - `POST`: recibe JSON arbitrario, le agrega un `id` incremental y lo almacena en memoria.
- El almacenamiento es temporal (se pierde al reiniciar el contenedor), por lo que no requiere base de datos.

### Web Flask (`tareaWEB`)

- Endpoint único `/` que retorna un `h1` HTML con **Web Funcionando!**
- Usa el mismo puerto 5000 para mantener coherencia con el despliegue de la API.

---

## Construcción y ejecución con Docker

```bash
# API
docker build -t tarea-api ./tareaAPI
docker run --rm -p 5000:5000 tarea-api

# Web
docker build -t tarea-web ./tareaWEB
docker run --rm -p 5001:5000 tarea-web
```

> Ajusta los puertos de publicación (`-p`) si necesitas correr ambos contenedores en la misma máquina.

---

## Despliegue en Kubernetes (`tareaK8s`)

1. **Namespace y configuraciones previas** (ver `ComandosDeCreacion.txt`):
   - `kubectl create namespace tarea-namespace`
   - Crear los secretos `db-conn` y `app-secrets`.
   - Crear el ConfigMap `app-config`.
2. **Aplicar manifiestos**:
   ```bash
   kubectl apply -f tareaK8s/api-deploy.yaml -n tarea-namespace
   kubectl apply -f tareaK8s/api-svc.yaml -n tarea-namespace
   kubectl apply -f tareaK8s/web-deploy.yaml -n tarea-namespace
   kubectl apply -f tareaK8s/web-svc.yaml -n tarea-namespace
   ```
3. **Imágenes**: Los despliegues apuntan a `acruno.azurecr.io/tareaapi:v2` y `acruno.azurecr.io/tareaweb:v2`. Publica versiones compatibles en ese registro o actualiza los valores del campo `image`.
4. **Configuración dinámica**:
   - La API consume `APP_ENV` mediante `env.valueFrom.configMapKeyRef`.
   - `ComandosDeCreacion.txt` también documenta cómo extender el Deployment para leer secretos (ej. `APP_SECRET`).
5. **Servicios**: Ambos Services son `LoadBalancer` con `port: 80` → `targetPort: 5000`. Cambia a `ClusterIP` si solo necesitas exposición interna.

---



