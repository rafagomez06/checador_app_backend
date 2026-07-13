## Crear Entorno Virtual (venv)

    python3 -m venv venv

## Ejecutar Entorno Virtual

    --Linux:    source venv/bin/activate
    --Win:      ./venv/Scripts/activate
    --Salir del venv:     deactivate

## Actualizar Pip

    python -m pip install --upgrade pip

## Instalacion de Dependencias

    pip3 install -r requirements.txt

## Run

    flask --app main run
    python main.py

## Ejecucion GUNICORN

    gunicorn -w 4 -b 0.0.0.0:5100 main:app --log-level debug
