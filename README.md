# poke-berries-statistics
Simple Poke-berries statistics API


### Start the app for development
```bash 
python -m hypercorn app.main:app --bind 0.0.0.0:80 --reload --debug
```  
### Or with Docker
```bash 
docker build -t poke-berries .
docker run -d --name poke-berries -p 80:80 poke-berries
```  


Fastapi automatic api docs at [localhost/docs](localhost/docs)