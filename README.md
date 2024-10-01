# Papelectro

## Descripción del Proyecto

**Papelectro** es una aplicación web de Gestión Electrónica de Documentos (GED) diseñada para empresas, con el objetivo de optimizar la administración de sus documentos mediante un sistema de almacenamiento digital centralizado. La aplicación busca sustituir el uso tradicional de archivos en papel, facilitando la organización y acceso a la información desde cualquier lugar. Además, se integra con funcionalidades avanzadas como la búsqueda inteligente, la gestión de usuarios con roles y la implementación de pagos por suscripción.

## Funcionalidades Principales

### Almacenamiento y Gestión de Documentos
Papelectro permite a las empresas almacenar diferentes tipos de documentos (`*.txt`, `*.xls`, `.pdf`) de manera segura y accesible en cualquier momento. Los archivos podrán organizarse en carpetas dentro de la plataforma, según el plan de almacenamiento contratado.

### Búsqueda Inteligente
Los usuarios podrán realizar búsquedas avanzadas utilizando palabras clave, categorías o fechas, mejorando la eficiencia en la recuperación de información.

### Gestión de Usuarios y Roles
Se implementarán diferentes niveles de acceso basados en roles, lo que permitirá a los usuarios pertenecer a grupos según su empresa o cargo, con acceso limitado o completo a funciones y documentos.

### Planes de Suscripción
Papelectro implementa un modelo de negocio basado en suscripciones, donde las empresas pagarán una cuota mensual o anual para acceder al servicio, con diferentes niveles de almacenamiento y funcionalidades según el plan contratado.

### Seguridad
La seguridad es fundamental en este proyecto. Se implementarán prácticas como el cifrado de datos, autenticación segura y protección de acceso a los documentos.

### Simulación de Pago
Se integrará un simulador de pago mediante **PayPal** para gestionar las cuotas de suscripción, permitiendo a las empresas abonar los planes de almacenamiento de manera sencilla y segura.

### Páginas Adicionales
La aplicación contará con una página de inicio, una sección de información sobre el servicio, una página de contacto y una sección para seleccionar los planes de almacenamiento disponibles.

## Justificación del Proyecto

El papel es ineficiente y genera altos costos de almacenamiento físico y riesgo de pérdida de información. Papelectro busca resolver estos problemas, optimizando la gestión de documentos mediante una plataforma segura y eficiente, dirigida a empresas que deseen mejorar su proceso de digitalización.

## Alcance del Proyecto

El proyecto incluye:
- Desarrollo del backend y frontend para la gestión de archivos, usuarios y roles.
- Integración de funcionalidades de seguridad.
- Implementación del sistema de pagos por suscripción con **PayPal**.
- Funcionalidad de búsqueda avanzada de documentos.
- Escalabilidad para crecer a medida que más empresas se unan al servicio.

El proyecto se centrará en crear un **MVP (Producto Mínimo Viable)** con funcionalidades básicas, seguido de mejoras progresivas en seguridad y optimización de la interfaz.

## Valoración de Alternativas Existentes

### Google Drive y Dropbox
Son plataformas populares para el almacenamiento en la nube, pero **Papelectro** se enfoca en entornos empresariales con roles personalizados y un sistema de búsqueda optimizado para documentos empresariales.

### M-Files y Alfresco
Son sistemas más completos pero costosos. Papelectro ofrece una alternativa accesible y fácil de implementar, dirigida a pequeñas y medianas empresas.

### Evernote y OneNote
Son plataformas de notas que carecen de la gestión de roles y la seguridad avanzada que **Papelectro** implementará.

## Stack Tecnológico Elegido

### Backend:
- **Django**: Framework robusto y seguro para el desarrollo del backend, gestión de usuarios y autenticación.

### Frontend:
- **Angular** o **Django Templates**: Dependiendo del nivel de interactividad necesario.
- **Bootstrap**, **CSS**, **HTML**: Para una interfaz responsiva y amigable.

### Base de Datos:
- **PostgreSQL** o **SQLite3**: PostgreSQL para producción, SQLite3 para desarrollo.

### Servidor:
- **Apache** o **AWS**: Apache para servidor local, y AWS para almacenamiento y hosting escalable.

### Almacenamiento de Archivos:
- Sistema de archivos local o **Amazon S3** para almacenamiento escalable.

### JSON:
- Se utilizará para la transferencia de datos entre frontend y backend.

## Objetivos del Proyecto

1. Desarrollar un sistema de almacenamiento de documentos que permita subir, organizar y descargar archivos de diferentes tipos (`*.txt`, `*.pdf`, `*.xls`).
2. Implementar una búsqueda avanzada para localizar documentos por palabras clave, categorías, fecha, etc.
3. Crear un sistema de gestión de usuarios con roles y niveles de acceso diferenciados.
4. Implementar un sistema de suscripción con planes de almacenamiento y pasarela de pago.
5. Garantizar la seguridad mediante cifrado y control de acceso.
6. Desarrollar una interfaz intuitiva y accesible desde cualquier dispositivo.

## Requisitos del Sistema

### Requisitos Funcionales:
- Autenticación de usuarios y gestión de contraseñas.
- Gestión de documentos: subir, descargar, renombrar y eliminar archivos.
- Roles y permisos de usuario diferenciados (administrador y usuario estándar).
- Suscripciones y pagos mediante **PayPal**.
- Búsqueda avanzada de documentos por filtros y palabras clave.
- Límites de almacenamiento según el plan.

### Requisitos No Funcionales:
- Escalabilidad para manejar un número creciente de usuarios y documentos.
- Seguridad mediante SSL, cifrado de datos y autenticación segura.
- Disponibilidad del 99.9% del tiempo.
- Rendimiento optimizado (operaciones en menos de 3 segundos).
- Compatibilidad con diferentes navegadores y dispositivos.
- Mantenimiento y actualización sin interrupciones.

### Requisitos de Interfaz:
- Diseño responsivo.
- Interfaz minimalista e intuitiva.
- Dashboard para gestionar almacenamiento y documentos.
- Notificaciones y alertas claras.
- Sistema de ayuda y FAQ.

## Casos de Uso Importantes

### Caso de Uso 1: Subir un Documento
**Descripción**: El usuario sube un archivo para almacenarlo.
- **Actor**: Usuario (administrador o estándar).
- **Flujo**: Acceder a la sección de documentos > Seleccionar archivo > Subir.

### Caso de Uso 2: Buscar un Documento
**Descripción**: El usuario realiza una búsqueda avanzada.
- **Actor**: Usuario.
- **Flujo**: Acceder a búsqueda avanzada > Introducir criterios > Ver resultados.

### Caso de Uso 3: Pago de Suscripción
**Descripción**: El administrador renueva la suscripción.
- **Actor**: Administrador.
- **Flujo**: Seleccionar plan > Realizar pago vía PayPal > Confirmación.

### Caso de Uso 4: Gestión de Roles y Permisos
**Descripción**: El administrador gestiona los permisos de usuarios.
- **Actor**: Administrador.
- **Flujo**: Acceder a gestión de usuarios > Asignar permisos/roles > Guardar cambios.

  
## Diagrama inicial entidad relación

![Diagrana_ER_GED](./readme_imgs/Diagrama_GED)

