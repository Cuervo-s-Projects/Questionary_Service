![Portada](portada_cuervos.jpg)
# 📄 Servicio de Gestión de Documentos y Cuestionarios

Este microservicio Flask proporciona endpoints para la **gestión de documentos PDF** (carga, descarga, búsqueda) y la **creación y evaluación de cuestionarios**. Forma parte de un ecosistema distribuido y modular basado en autenticación JWT y documentación Swagger.

---

## ✨ Funcionalidades Principales
- **Creación dinámica de cuestionarios**

---

## 📆 Tecnologías utilizadas

* [Python 3.10+](https://www.python.org/)
* [Flask](https://flask.palletsprojects.com/)
* [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/) – Autenticación
* [MongoEngine](https://mongoengine.org/) – ORM para MongoDB
* \[GridFS / PyMongo] – Almacenamiento de archivos
* [Flasgger](https://github.com/flasgger/flasgger) – Swagger/OpenAPI
* [PyPDF2](https://pypi.org/project/PyPDF2/) – Procesamiento de PDFs
* [Decouple](https://pypi.org/project/python-decouple/) – Gestión de variables de entorno
* \[pytest] – Pruebas (estructura básica)

---

## 🛠️ Requisitos

* Python 3.10 o superior
* `pip`
* MongoDB en ejecución (local o remoto)
* Configuración `.env` con:

  ```
  MONGO_DBNAME=nombre_bd
  MONGO_URI=mongodb://localhost:27017
  ```

---

## 🚀 Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/Cuervo-s-Projects/Questionary_Service.git
   cd nombre-del-servicio
   ```

2. (Opcional) Crea un entorno virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate     # Windows: venv\Scripts\activate
   ```

3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Ejecución local

Levanta el servidor Flask en modo desarrollo:

```bash
python main.py
```

Esto iniciará la app en:

```
http://localhost:5002
```

---

## 📬 Endpoints principales

### 📚 Documentos

| Método | Ruta                           | Descripción                          |
| ------ | ------------------------------ | ------------------------------------ |
| POST   | `/api/documents/upload`        | Subir un archivo PDF                 |
| GET    | `/api/documents/<id>`          | Consultar metadatos del documento    |
| DELETE | `/api/documents/<id>`          | Eliminar documento                   |
| GET    | `/api/documents`               | Listar documentos (filtros)          |
| GET    | `/api/documents/search`        | Buscar por título, descripción, etc. |
| GET    | `/api/documents/<id>/download` | Descargar documento por ID           |
| GET    | `/api/download/<file_id>`      | Descargar documento por `file_id`    |

### ❓ Cuestionarios

| Método | Ruta                       | Descripción                          |
| ------ | -------------------------- | ------------------------------------ |
| POST   | `/api/test/create`         | Crear un nuevo cuestionario          |
| POST   | `/api/test/assess`         | Evaluar respuestas a un cuestionario |
| GET    | `/api/test/quiz/<quiz_id>` | Obtener cuestionario por ID          |

> Todos los endpoints requieren token JWT válido en el header `Authorization`.

---

## 📃 Documentación Swagger

Este proyecto incluye documentación de los endpoints en formato **YAML**, ubicada en la carpeta `docs/`.

### Ver documentación:

1. Instala [Swagger Editor](https://editor.swagger.io/) o usa el visualizador en línea.
2. Carga los archivos YAML:

   * `docs/create.yaml`
   * `docs/assess.yaml`
   * `docs/get_quiz.yaml`

> Los endpoints están documentados usando `@swag_from(...)` de [Flasgger](https://github.com/flasgger/flasgger), permitiendo acoplar los YAML con sus funciones correspondientes.

---

## 📁 Estructura del proyecto

```
.
├── app/
│   ├── routes.py               # Cuestionarios
│   ├── document_routes.py      # Gestión de documentos
│   ├── service.py              # Lógica de negocio
│   ├── models.py               # Modelos de MongoEngine
│   ├── gridfs_utils.py         # Carga/descarga en GridFS
│   └── ...
├── config/                     # Configuración por clase
├── docs/                       # Archivos OpenAPI YAML
├── test/                       # Carpeta para pruebas
├── main.py                     # Punto de entrada Flask
├── requirements.txt
├── README.md
├── CHANGELOG.md
```

---

## 📬 Contacto
- Jacel Thomás Enciso Pinzón - [@slendrac123](https://github.com/slendrac123) - Correo: jencisop@unal.edu.co
- Daniel Santiago Delgado Pinilla - [@ddelgadopi](https://github.com/ddelgadopi) - Correo: ddelgadopi@unal.edu.co
- Juan David Ramírez López - [@Juramirezlop](https://github.com/Juramirezlop) - Correo: juramirezlop@unal.edu.co
- Jesus David Giraldo Gomez - [@gdavidg-27](https://github.com/gdavidg-27) - Correo: jedgiraldogo@unal.edu.co
- Cristian Liu Chois Amaya - [@cchois](https://github.com/cchois) - Correo: cchois@unal.edu.co
- Iván David Molina Leguízamo - [@ivdmolinale](https://gitlab.com/ivdmolinale) - Correo: ivdmolinale@unal.edu.co

Proyecto: [https://github.com/Cuervo-s-Projects/Frontend_cuervos](https://github.com/Cuervo-s-Projects/Frontend_cuervos)

---