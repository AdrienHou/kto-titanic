# TODO : Importer uvicorn et l'application FastAPI à démarrer
import uvicorn
from titanic.api import infer

def main():
    # TODO : Démarrer le server WEB et exposer l'application FastAPI
    uvicorn.run(infer.app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
    