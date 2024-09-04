# Proyecto de Albergue de Animales

Este proyecto consiste en una API REST para un albergue de animales desarrollada con Django Rest Framework y un cliente web construido con Next.js. El sistema permite gestionar animales, voluntarios, adoptantes y procesos de adopción.

## Tecnologías Utilizadas

- Backend:
  - Python 3.12
  - Django Rest Framework
  - Simple JWT para autenticación
- Frontend:
  - Next.js 14
  - React con TypeScript
  - Mantine UI
  - App Router de Next.js
- Base de Datos:
  - PostgreSQL (configurado con Docker Compose para desarrollo local)

## Configuración del Proyecto

### Backend (Django Rest Framework)

1. Navega al directorio del backend:
   ```
   cd backend
   ```

2. Crea un entorno virtual:
   ```
   python -m venv env
   ```

3. Activa el entorno virtual:
   - En Windows:
     ```
     .\env\Scripts\activate
     ```
   - En macOS y Linux:
     ```
     source env/bin/activate
     ```

4. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

5. Configura las variables de entorno:
   - Copia el archivo `.env.example` a `.env`
   - Ajusta las variables en `.env` según tu configuración local

6. Ejecuta las migraciones:
   ```
   python manage.py migrate
   ```

7. Inicia el servidor de desarrollo:
   ```
   python manage.py runserver
   ```

8. Para ejecutar las pruebas:
   ```
   python manage.py test
   ```

### Frontend (Next.js)

1. Navega al directorio del frontend:
   ```
   cd frontend
   ```

2. Instala las dependencias:
   ```
   npm install
   ```

3. Configura la URL de la API:
   - Copia el archivo `.env.example` a `.env.local`
   - Ajusta la variable `NEXT_PUBLIC_API_URL` en `.env.local`

4. Inicia el servidor de desarrollo:
   ```
   npm run dev
   ```

## Base de Datos (PostgreSQL con Docker)

Para configurar la base de datos PostgreSQL usando Docker Compose:

1. Asegúrate de tener Docker y Docker Compose instalados.
2. Desde la raíz del proyecto, ejecuta:
   ```
   docker-compose up -d
   ```

## Despliegue

- Frontend: Desplegado en Vercel
- Backend y Base de Datos: Desplegados en Render.com

## Funcionalidades Logradas

1. Gestión de Animales:
   - Listar, crear, actualizar y eliminar animales en el albergue
   - Filtrar animales por tipo (perro o gato) y estado de adopción

2. Gestión de Voluntarios:
   - Registro y autenticación de voluntarios
   - Listar, actualizar y eliminar perfiles de voluntarios
   - Asignar tareas y gestionar horarios de voluntarios

3. Gestión de Adoptantes:
   - Registro y autenticación de adoptantes
   - Listar, actualizar y eliminar perfiles de adoptantes
   - Proceso de solicitud de adopción

4. Proceso de Adopción:
   - Crear y gestionar solicitudes de adopción
   - Seguimiento del estado de las adopciones
   - Aprobación o rechazo de solicitudes por parte de voluntarios
   - Sincronaziación de la información de adopciones con adoptantes y animales

5. Autenticación y Autorización:
   - Implementación de JWT para autenticación segura
   - Diferentes niveles de acceso para administradores, voluntarios y adoptantes

6. Interfaz de Usuario:
   - Diseño responsivo utilizando Mantine UI
   - Navegación intuitiva con App Router de Next.js
   - Formularios con validación para entrada de datos

## Notas Adicionales

- El proyecto utiliza Django Rest Framework para la API REST.
- La autenticación se maneja con Simple JWT.
- El frontend está construido con Next.js 14, utilizando el App Router y Mantine UI para la interfaz de usuario.
- Se han implementado pruebas en Django para asegurar la calidad del código backend.