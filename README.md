

Este repositorio contiene ejercicios y desafíos. Aquí encontrarás código, instrucciones y recursos que te ayudarán a desarrollar tus habilidades en programación y resolución de problemas.

---

## Contenido

1. **Ejercicios Semanales:** Desafíos organizados por semana.
2. **Archivos de Ejemplo:** Código de referencia y soluciones.
3. **Recursos Adicionales:** Enlaces útiles y documentación recomendada.

---

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalado lo siguiente:

- Python 3.8 o superior: [Descargar Python](https://www.python.org/downloads/)
- Git (opcional pero recomendado): [Descargar Git](https://git-scm.com/downloads)
- Jupyter Lab (para notebooks interactivos)
- Un editor de código como Visual Studio Code (opcional)

---

## Configuración del Proyecto

Sigue estos pasos para configurar el entorno y empezar a trabajar en el proyecto:

### 1. Clonar el repositorio

Si no tienes una copia local del proyecto, clónalo usando Git:
```bash
git clone https://github.com/usuario/PI-Get-Talent.git
cd PI-Get-Talent
```

### 2. Crear un entorno virtual

Un entorno virtual te permite instalar dependencias aisladas para este proyecto. Para crearlo:

1. Abre la consola (cmd)
2. Navega hasta la carpeta del proyecto:
```bash
cd "ruta_a_la_carpeta"
```
3. Crea el entorno virtual:
```bash
python -m venv venv
```

### 3. Activar el entorno virtual

Activa el entorno virtual según tu sistema operativo:

- **Windows (Command Prompt o PowerShell):**
  ```bash
  source venv/Scripts/activate
  ```

- **Linux/macOS:**
  ```bash
  source venv/bin/activate
  ```

Cuando el entorno virtual esté activo, deberías ver algo como `(venv)` al inicio de la línea de tu terminal.

### 4. Instalar dependencias

Hay dos formas de instalar las dependencias necesarias:

#### Opción 1: Instalación completa
```bash
pip install -r requirements.txt
```

#### Opción 2: Instalación individual (si hay problemas con requirements.txt)
```bash
pip install cohere
pip install python-dotenv
pip install ipywidgets
```

### 5. Configuración de Cohere API

1. Crear una cuenta en [Cohere](https://cohere.ai/)
2. Ir a Dashboard -> API Keys para obtener tu API Key
3. Crear un archivo `.env` en la carpeta raíz del proyecto
4. Agregar tu API Key al archivo `.env`:
```
COHERE_API_KEY="tu_api_key_aquí"
```

### 6. Iniciar Jupyter Lab

Para trabajar con notebooks:
```bash
jupyter lab
```
Esto abrirá automáticamente una ventana del navegador. Si no se abre, copia y pega en tu navegador la URL que aparece en la consola.

---

## Estructura del Proyecto

```
PI-Get-Talent/
├── Semana1/
│   ├── ejercicio1.py
│   ├── ejercicio2.py
│   └── ...
├── Semana2/
│   ├── ejercicio1.py
│   ├── desafio.py
│   └── ...
├── README.md
├── requirements.txt
├── .env
└── venv/ (entorno virtual)
```

- **SemanaX/**: Contiene los ejercicios de cada semana.
- **requirements.txt**: Lista de dependencias necesarias.
- **README.md**: Documentación del proyecto.
- **.env**: Archivo de configuración para las API keys.

---

## Uso

### Ejecutar un ejercicio

Para ejecutar un archivo de ejercicio, usa el comando:
```bash
python SemanaX/archivo.py
```

### Añadir Dependencias

Si necesitas instalar nuevas bibliotecas, usa:
```bash
pip install <nombre_de_paquete>
```
Luego actualiza el archivo `requirements.txt`:
```bash
pip freeze > requirements.txt
```

---
### Ejecutar Main

Instalar FastAPI junto con su servidor:
```bash
pip install fastapi uvicorn
```
Ejecutar el servidor:
```bash
uvicorn main:app --reload
```
---

## Solución de Problemas

Si encuentras problemas durante la configuración:

1. **Error en la instalación de requirements.txt:**
   - Intenta la instalación individual de paquetes
   - Verifica que tu versión de Python sea compatible

2. **Problemas con Jupyter Lab:**
   - Puedes usar Visual Studio Code como alternativa
   - Asegúrate de tener el entorno virtual activado

3. **Error con la API Key:**
   - Verifica que el archivo `.env` esté en la ubicación correcta
   - Asegúrate de que el formato de la API Key sea exactamente como se muestra en el ejemplo

---

## Contribuir

Si deseas contribuir a este repositorio, sigue estos pasos:

1. Crea un _fork_ del repositorio.
2. Crea una nueva rama para tu función o corrección:
   ```bash
   git checkout -b nueva-rama
   ```
3. Realiza tus cambios y súbelos a tu rama.
4. Crea un _pull request_ en GitHub.

---

## Soporte

Si tienes alguna duda o encuentras un problema, abre un _issue_ en el repositorio o contacta a los administradores del proyecto.

---

