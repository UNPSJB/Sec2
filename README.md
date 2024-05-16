# Sindicato Empleados de Comercio (SEC) <img align="left" style ="text-align: left- margin-right= 10px;" alt="GIF" src="README/icon/SEC.jpg"  width="40" height="40"/><img style ="text-align: left- margin-right= 10px;" alt="GIF" src="README/icon/SEC.jpg"  width="40" height="40"/>

<img height="120" alt="SEC" width="100%" src="README/marquee.svg" />

<img align="left" src="README/icon/python.png" />
<img align="left" src="README/icon/django.png" width="32" height="32"/>
<img align="left" src="README/icon/SQLite.png" width="32" height="32"/>
<img align="left" src="README/icon/javascript.png"/>
<img align="left" src="README/icon/html5.png" width="32" height="32"/>
<img align="left" src="README/icon/CSS3.png" width="32" height="32"/>

<br>

## Autores

- [Arcos Vargas Martín](https://github.com/cozakoo)
- Fabro Diego Ezequiel
- Lucero Carlos
- Murillo Alexis

## Proyecto

- [Tablero](https://github.com/orgs/UNPSJB/projects/9)

## Elementos
- Python 3.10.7
- Django versión 4.1.1

##### Páginas de ayuda:

<a> https://www.python.org/downloads/ </a>

## Instalar
```bash
git clone --branch develop https://github.com/UNPSJB/Sec2.git

python3 -m venv <venv>
source <venv>/Scripts/activate
  
cd sec2/
  
pip install -r requirements.txt

python manage.py makemigrations

python manage.py migrate

python manage.py createsuperuser

python manage.py runserver
```
### Activar venv
  
| Platform | Shell           | Command to activate virtual environment |
| -------- | --------------- | --------------------------------------- |
| POSIX    | bash/zsh        | $ source <venv>/bin/activate            |
|          | fish            | $ source <venv>/bin/activate.fish       |
|          | csh/tcsh        | $ source <venv>/bin/activate.csh        |
|          | PowerShell Core | $ <venv>/bin/Activate.ps1               |
| Windows  | cmd.exe         | C:\> <venv>\Scripts\activate.bat        |
|          | PowerShell      | PS C:\> <venv>\Scripts\Activate.ps1     |

### Configurar variables de entorno
