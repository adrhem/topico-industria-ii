## Tarea 1: Creación de ambiente de trabajo

### Configuración de la máquina virtual
En el directorio existe un archivo `Makefile`con el cual se puede montar la máquina virtual con distintos comandos. Para esta tarea se está usando [qemu](https://www.qemu.org/) como emulador de hardware, y se ha creado una imagen de disco con el sistema operativo Ubuntu 22.04 Desktop para AMD64. Para montar la máquina virtual, se deben ejecutar los comandos a continuación:


1. `make create_disk`
    Este comando crea una imagen de disco llamada `ubuntu-amd64.qcow2` con un tamaño de 60GB. Esta imagen se utilizará como disco duro para la máquina virtual.

2. `make get_ubuntu_iso`
    Este comando descarga la imagen ISO de Ubuntu 22.04 Desktop para AMD64, que se utilizará para instalar el sistema operativo en la máquina virtual. Se eligió la arquitectura AMD64 por la compatibilidad con la mayoría de los sistemas, lo que permite ejecutar la máquina virtual de manera más eficiente en hardware estándar.

3. `make install`
    Este comando inicia la máquina virtual utilizando qemu, con la imagen de disco creada y la imagen ISO de Ubuntu como fuente de instalación. Al ejecutar este comando, se abrirá una ventana de la máquina virtual, donde se podrá seguir el proceso de instalación de Ubuntu 22.04 Desktop para AMD64. Durante la instalación, se deben seguir las instrucciones en pantalla para configurar el sistema operativo según las preferencias del usuario.

4. `make boot`
    Este comando inicia la máquina virtual utilizando qemu, pero en lugar de usar la imagen ISO para la instalación, utiliza la imagen de disco `ubuntu-amd64.qcow2` que se creó previamente. Esto permite arrancar directamente en el sistema operativo instalado en la máquina virtual, sin necesidad de pasar por el proceso de instalación nuevamente. 