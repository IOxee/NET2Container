import os
import xml.etree.ElementTree as ET
import shutil

# Ruta del archivo .csproj del proyecto partiendo de la ruta de ejecución del script
csproj_route = os.getcwd() + "\\" + os.getcwd().split(os.path.sep)[-1] + ".csproj"
archivo_csproj = csproj_route

file_name = os.path.basename(archivo_csproj)

 # Nombre del host de Docker Hub donde se va a subir la imagen ej. django/django
host_name = 'ioxee'

# Obtiene las rutas absolutas de las dependencias del archivo .csproj
# Devuelve una lista con las rutas absolutas de las dependencias
# Si no se puede analizar el archivo .csproj devuelve una lista vacía
# Si no se encuentran dependencias devuelve una lista vacía
# Si no se encuentra el archivo .csproj devuelve una lista vacía

def obtener_rutas_dependencias(archivo_csproj):
    rutas_absolutas = []

    try:
        # Analizar el archivo .csproj con ElementTree para obtener las rutas de las dependencias del proyecto
        tree = ET.parse(archivo_csproj)
        root = tree.getroot()

        # Obtener las rutas de las dependencias del archivo .csproj
        for reference in root.iter('Reference'):
            # Obtener el atributo Include del elemento Reference para obtener el nombre de la dependencia
            include = reference.attrib.get('Include')

            # Obtener el elemento HintPath para obtener la ruta relativa de la dependencia
            hint_path_element = reference.find('HintPath')

            # Comprobar si el elemento HintPath existe
            if hint_path_element is not None:

                # Obtener la ruta relativa de la dependencia del elemento HintPath
                hint_path = hint_path_element.text

                # Obtener la ruta absoluta de la dependencia a partir de la ruta relativa
                ruta_absoluta = obtener_ruta_absoluta(archivo_csproj, hint_path)

                # Comprobar si la ruta absoluta existe
                if ruta_absoluta:

                    # Añadir la ruta absoluta a la lista de rutas absolutas
                    rutas_absolutas.append(ruta_absoluta)

        # Devolver la lista de rutas absolutas
        return rutas_absolutas
    
    # Si no se puede analizar el archivo .csproj devuelve una lista vacía
    except ET.ParseError:

        # Devolver una lista vacía si no se puede analizar el archivo .csproj
        print(f"Error al analizar el archivo: {archivo_csproj}")
        return []


# Obtiene la ruta absoluta de una dependencia a partir de la ruta relativa
# Devuelve la ruta absoluta de la dependencia

def obtener_ruta_absoluta(archivo_csproj, hint_path):
    # Obtener la ruta absoluta de la dependencia a partir de la ruta relativa
    directorio_actual = os.path.dirname(archivo_csproj)
    # Une la ruta actual con la ruta relativa de la dependencia
    directorio_dependencia = os.path.normpath(os.path.join(directorio_actual, hint_path))
    return directorio_dependencia

# Modifica las rutas de las dependencias en el archivo .csproj
# Devuelve True si se han modificado las rutas de las dependencias correctamente
# Devuelve False si no se han modificado las rutas de las dependencias correctamente

def modificar_ruta_dependencias(archivo_csproj, ruta_dependencias):
    try:
        # Analizar el archivo .csproj con ElementTree para modificar las rutas de las dependencias del proyecto
        tree = ET.parse(archivo_csproj)
        root = tree.getroot()

        # Modificar las rutas de las dependencias del archivo .csproj
        for reference in root.iter('Reference'):
            # Obtener el elemento HintPath para obtener la ruta relativa de la dependencia
            hint_path_element = reference.find('HintPath')
            # Comprobar si el elemento HintPath existe
            if hint_path_element is not None:
                # Obtener la ruta relativa de la dependencia del elemento HintPath
                hint_path = hint_path_element.text

                # Obtener el nombre del archivo de la dependencia
                nombre_archivo = os.path.basename(hint_path)

                # Crear la nueva ruta de la dependencia
                nueva_ruta = os.path.join(ruta_dependencias, nombre_archivo)

                # Modificar la ruta en el elemento HintPath
                hint_path_element.text = nueva_ruta

        # Guardar los cambios en el archivo .csproj
        tree.write(archivo_csproj)

        print("Rutas de dependencias modificadas correctamente.")

    # Si no se puede analizar el archivo .csproj devuelve una lista vacía
    except ET.ParseError:
        # Devolver una lista vacía si no se puede analizar el archivo .csproj
        print(f"Error al analizar el archivo: {archivo_csproj}")

# Genera el Dockerfile partiendo del ejemplo proporcionado por Visual Studio
# Devuelve True si se ha generado el Dockerfile correctamente
# Devuelve False si no se ha generado el Dockerfile correctamente

def generar_dockerfile(archivo_csproj):
    try:
        # Analizar el archivo .csproj con ElementTree para obtener las rutas de las dependencias del proyecto
        tree = ET.parse(archivo_csproj)
        root = tree.getroot()

        # Crear el contenido del Dockerfile
        contenido_dockerfile = """\
#See https://aka.ms/customizecontainer to learn how to customize your debug container and how Visual Studio uses this Dockerfile to build your images for faster debugging.

FROM mcr.microsoft.com/dotnet/aspnet:6.0 AS base
WORKDIR /app
EXPOSE 80
EXPOSE 443

FROM mcr.microsoft.com/dotnet/sdk:6.0 AS build
WORKDIR /src
"""
        # Copiar el archivo csproj y restaurar las dependencias
        contenido_dockerfile += "\n"
        # Obtener la ruta relativa del proyecto
        relative_path_project = csproj_route.split(os.path.sep)[-2:]
        # Unir la ruta relativa del proyecto en una cadena separada por /
        relative_path_project = "/".join(relative_path_project)
        # Copiar el archivo csproj y restaurar las dependencias del proyecto principal en el Dockerfile
        contenido_dockerfile += f"COPY [\"{relative_path_project}\", \"{os.path.basename(os.path.dirname(archivo_csproj))}/\"]\n"


        # Obtener los proyectos referenciados en el archivo csproj
        proyectos_referenciados = []
        for project_reference in root.iter('ProjectReference'):

            # Obtener el atributo Include del elemento ProjectReference para obtener el nombre del proyecto
            include = project_reference.attrib.get('Include')

            # Cambiar las barras invertidas por barras normales para que Docker las reconozca
            include = include.split('\\')[-2] + '/' + include.split('\\')[-1].split('.')[0]

            # Añadir el proyecto a la lista de proyectos referenciados
            proyectos_referenciados.append(include)

        # Copiar los archivos csproj y restaurar las dependencias
        for proyecto in proyectos_referenciados:
            # Obtener la ruta relativa del proyecto referenciado en el archivo csproj principal 
            contenido_dockerfile += f"COPY [\"{proyecto}.csproj\", \"{os.path.dirname(proyecto)}/\"]\n"
        
        # Restaurar las dependencias de los proyectos referenciados
        contenido_dockerfile += f"RUN dotnet restore \"{relative_path_project}\"\n"

        # Copiar el resto de los archivos y construir el proyecto principal
        contenido_dockerfile += "\n"
        contenido_dockerfile += "COPY . .\n"

        # Cambiar el directorio de trabajo a la carpeta del proyecto principal
        contenido_dockerfile += f"WORKDIR \"/src/{os.path.basename(os.path.dirname(archivo_csproj))}\"\n"

        # Construir el proyecto principal en modo Release y publicarlo en la carpeta /app/build del contenedor
        contenido_dockerfile += f"RUN dotnet build \"{file_name}\" -c Release -o /app/build\n"

        # Publicar el proyecto principal
        contenido_dockerfile += "\n"

        # Cambiar el directorio de trabajo a la carpeta del proyecto principal
        contenido_dockerfile += "FROM build AS publish\n"

        # Publicar el proyecto principal en la carpeta /app/publish del contenedor
        contenido_dockerfile += f"RUN dotnet publish \"{file_name}\" -c Release -o /app/publish /p:UseAppHost=false\n"

        # Configurar la imagen final
        contenido_dockerfile += "\n"
        
        # Cambiar el directorio de trabajo a la carpeta /app del contenedor
        contenido_dockerfile += "FROM base AS final\n"

        # Copiar el contenido de la carpeta /app/publish del contenedor a la carpeta /app del contenedor
        contenido_dockerfile += "WORKDIR /app\n"

        # Copiar el contenido de la carpeta /app/publish del contenedor a la carpeta /app del contenedor
        contenido_dockerfile += "COPY --from=publish /app/publish .\n"

        # Ejecutar el proyecto principal
        contenido_dockerfile += f"ENTRYPOINT [\"dotnet\", \"{file_name.split('.')[0]}.dll\"]\n"

        # Escribir el contenido en el archivo Dockerfile
        with open("Dockerfile", "w") as f:
            f.write(contenido_dockerfile)

        print("Dockerfile generado correctamente.")

    # Si no se puede analizar el archivo .csproj devuelve una lista vacía
    except ET.ParseError:
        print(f"Error al analizar el archivo: {archivo_csproj}")


# Genera la imagen de Docker

def generar_docker_image():
    os.system(f"docker build -t {host_name}/{file_name.split('.')[0].lower()}  -f Dockerfile ..")

# Restaura la ruta de las dependencias en el archivo .csproj
# Devuelve True si se ha restaurado la ruta de las dependencias correctamente
# Devuelve False si no se ha restaurado la ruta de las dependencias correctamente

def restaurar_ruta_dependencias(initial_route, archivo_csproj, ruta_backup):
    os.remove(archivo_csproj)

    print(ruta_backup + "\\" + file_name)
    if os.path.isfile(ruta_backup + "\\" + file_name):
        shutil.move(ruta_backup + "\\" + file_name, initial_route)
        print("Archivo .csproj restaurado correctamente.")

        # destruye la carpeta Backup
        shutil.rmtree(initial_route + "Backup")
        return True
    else:
        print("El archivo .csproj no existe.")
        return False
    

    



if not os.path.isfile(archivo_csproj):
    print("El archivo no existe.")
else:
    rutas_dependencias = obtener_rutas_dependencias(archivo_csproj)

    if rutas_dependencias:
        print("Rutas absolutas de las dependencias encontradas:")
        for ruta in rutas_dependencias:
            initial_route = archivo_csproj.replace(file_name, "")

            # Crea una carpeta llamada "Backup" en la ruta inicial solo si no existe
            if not os.path.exists(initial_route + "Backup"):
                os.mkdir(initial_route + "Backup")

            # Copia el archivo .csproj en la carpeta Backup
            os.system(f"copy {archivo_csproj} {initial_route}Backup")


            # Comprueba si la ruta es un archivo
            if os.path.isfile(ruta):
                print(ruta)

                # Crea una carpeta llamada "Dependencias" en la ruta inicial solo si no existe
                if not os.path.exists(initial_route + "Dependencias"):
                    os.mkdir(initial_route + "Dependencias")
                
                # Copia el archivo en la carpeta Dependencias
                os.system(f"copy {ruta} {initial_route}Dependencias")

            else:
                print(f"El archivo no existe: {ruta}")
                # Obtiene la ruta del archivo .csproj para compilar el proyecto con dotnet build
                ruta_to_compile = ruta.split("bin")[0].rstrip(os.path.sep)

                # Cambia el directorio de trabajo a la ruta del archivo .csproj
                os.chdir(ruta_to_compile)

                # Comprueba si existe la carpeta bin\Debug por si el proyecto ya se ha compilado anteriormente
                if os.path.isdir(ruta_to_compile + "\\bin\\Debug"):
                    # Cambia el directorio de trabajo a la ruta inicial
                    os.chdir(initial_route)

                    # Crea una carpeta llamada "Dependencias" en la ruta inicial solo si no existe
                    if not os.path.exists(initial_route + "Dependencias"):
                        os.mkdir(initial_route + "Dependencias")

                    # Copia el archivo en la carpeta Dependencias
                    os.system(f"copy {ruta} {initial_route}Dependencias")

                else:
                    # Compila el proyecto
                    os.system(f"dotnet build -c Debug")

                    # Comprueba si existe la carpeta bin\Debug
                    if os.path.isdir(ruta_to_compile + "\\bin\\Debug"):
                        # Cambia el directorio de trabajo a la ruta inicial
                        os.chdir(initial_route)

                        # Crea una carpeta llamada "Dependencias" en la ruta inicial solo si no existe
                        if not os.path.exists(initial_route + "Dependencias"):
                            os.mkdir(initial_route + "Dependencias")

                        # Copia el archivo en la carpeta Dependencias
                        os.system(f"copy {ruta} {initial_route}Dependencias")

        # Modifica las rutas de las dependencias en el archivo .csproj
        modificar_ruta_dependencias(archivo_csproj, initial_route + "Dependencias")

        # Genera el Dockerfile partiendo del ejemplo proporcionado por Visual Studio
        generar_dockerfile(archivo_csproj)

        # Genera la imagen de Docker
        generar_docker_image()

        # Restaura la ruta de las dependencias en el archivo .csproj
        restaurar_ruta_dependencias(initial_route, archivo_csproj, initial_route + "Backup")

    else:
        print("No se encontraron dependencias o no se pudo analizar el archivo.")
