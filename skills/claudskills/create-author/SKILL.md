---
name: create-author
description: Crear página de Autor con ayuda de la IA Generativa. Usar cuando el usuario quiere crear un nuevo autor para el blog.
---

# Workflow para crear página de Autor

## Fase 1: Recopilación de información

1. **Obtener datos del autor**
   - Preguntar al usuario si desea proporcionar una URL pública con información del autor (GitHub, blog personal, portfolio).
   - Recopilar los siguientes datos esenciales:
     - Nombre completo
     - Cargo (`position`) en Buk
     - Nombre de usuario de LinkedIn (`linkedin_username`)
     - Nombre de usuario de GitHub (`github_username`)
     - Breve descripción profesional para la sección "Sobre mí"
   - Si el usuario proporciona una URL, extraer automáticamente los datos disponibles.
   - Solicitar al usuario cualquier dato faltante.

2. **Definir identificador único**
   - Proponer un identificador único (`short_name`) para el autor basado en su nombre (ejemplo: `aboneto` para Antonio Barbosa).
   - Este identificador se utilizará para el nombre del archivo y la URL del perfil.
   - Confirmar con el usuario si está de acuerdo con el identificador propuesto.

## Fase 2: Verificación y creación

1. **Verificar existencia del autor**
   - Comprobar si ya existe un archivo para este autor en la carpeta `_authors/`.
   - Si existe, informar al usuario y preguntar si desea editar el autor existente o crear uno con otro identificador.

2. **Crear archivo de autor**
   - Crear un archivo en `_authors/[identificador].md` con la siguiente estructura:

   ```yaml
   ---
   layout: author
   short_name: [identificador]
   title: '[Nombre completo]'
   name: [Nombre completo]
   position: [Cargo en Buk]
   linkedin_username: [usuario_linkedin]
   github_username: [usuario_github]
   background: "/assets/images/authors/[identificador]/background.jpeg"
   ---
   [Descripción profesional en formato Markdown]
   ```

3. **Gestionar imágenes (opcional)**
   - Informar al usuario que las imágenes son opcionales, pero si desea agregarlas, debe hacerlo en:
     `assets/images/authors/[identificador]/`
   - Tipos de imágenes que puede agregar (todas opcionales):
     - Una imagen de perfil
     - Una imagen de fondo (`background.jpeg`)

## Fase 3: Finalización

1. **Revisión**
   - Mostrar al usuario una vista previa del perfil creado.
   - Verificar que todos los datos estén correctos.
   - Corregir cualquier error ortográfico o de formato.

2. **Prueba local**
   - Sugerir al usuario probar el perfil localmente ejecutando el blog según las instrucciones en `docs/como-ejecutar-el-blog-localmente.md`.
   - La página del autor estará disponible en: `http://localhost:4000/authors/[identificador]`

3. **Publicación**
   - Recordar al usuario que debe crear un Pull Request siguiendo las convenciones de git establecidas.
   - Solicitar aprobación final en el espacio de Google Chat [#comité-techblog](https://chat.google.com/room/AAAAm1mqm2E?cls=7).

## Notas importantes

- Los perfiles de autor no son obligatorios, pero son altamente recomendables para dar reconocimiento a quien escribe.
- Al crear un perfil, se genera automáticamente una página dedicada en el blog bajo la URL `https://buk.engineering/authors/[identificador]`.
- En cada post escrito por este autor, su nombre aparecerá como un enlace que dirige a esta página de perfil.
