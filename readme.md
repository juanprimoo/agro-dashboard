# Agro Dashboard - Lavouras Permanentes

Dashboard interativo de produção agrícola no Brasil, com mapa e gráficos por estado, focado em **lavouras permanentes**.

## Tecnologias

- Frontend: Vue.js, Leaflet, Chart.js  
- Backend: FastAPI  
- Containerização: Docker, Docker Compose

## Como rodar

1. Clone o repositório:

```bash
git clone https://github.com/juanprimoo/agro-dashboard.git
cd agro-dashboard
```

2. Rode com Docker Compose:

```bash
docker-compose up --build
```

3. Acesse:

- Frontend: [http://localhost:5173](http://localhost:5173)  
- Backend: [http://localhost:8000](http://localhost:8000)  

## Funcionalidades

- Mapa interativo do Brasil com cores por valor de produção.  
- Gráficos de valores produção nacional e por estado.  
- Cards de resumo (valor de produção, área destinada e colhida).   
- Filtro rápido por estado no gráfico e tabela.

## Observações

- O mapa utiliza Leaflet com cores verdes para indicar intensidade de produção.  
- O gráfico mostra apenas dados de **valor de produção**.  
- Ao clicar em um estado, os cards e gráficos são atualizados para os dados daquele estado.

## Vídeo Demonstrativo

[Assista aqui](https://drive.google.com/file/d/1ZGnQAL7vU0KJ9axVVJpy_gVrJMn1_-zY/view?usp=drive_link)

