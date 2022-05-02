# poke-berries-statistics
Simple Poke-berries statistics API


## How to Run
Rename the file `.env.EXAPLE` to `.env` and replace inside the config values:  
- `BERRIES_URL`: The url to get berries information. Default: [https://pokeapi.co/api/v2/berry](https://pokeapi.co/api/v2/berry)  
- `CACHE`: To enable or disable simple caching of requested external resources. *Pokeapi* asks to [Locally cache resources whenever you request them](https://pokeapi.co/docs/v2#fairuse). Default: `TRUE`  
### Start the app for development  
Inside root directory, run:  
```bash 
pip install -r requirements.txt
python -m hypercorn app.main:app --bind 0.0.0.0:80 --reload --debug
```  
Run tests with:
```bash 
pytest
```  

### Or with Docker
```bash 
docker build -t poke-berries .
docker run -d --name poke-berries -p 80:80 --rm poke-berries
```  


Fastapi automatic api docs at [/docs](http://localhost/docs)  
  
Berries statistics at [/allBerryStats](http://localhost/allBerryStats)  
  
Growth time frequency graph at [/graph](http://localhost/graph)