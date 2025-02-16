version: "3.9"
services:
  web:
    image: nginx:latest
    volumes:
      # - ./html:/usr/share/nginx/html:ro
      - ./html/index.html:/usr/share/nginx/html/index.html:ro
    networks:
      - global
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: "1"
          memory: 1G
          # pids: 100
        reservations:
          cpus: "0.1"
          memory: 20M
      restart_policy:
        condition: on-failure
    ports:
      - "80:80"

  web-alt:
    image: nginx:latest
    volumes:
      # - ./html:/usr/share/nginx/html:ro
      - ./html/index-alt.html:/usr/share/nginx/html/index.html:ro
    networks:
      - global
    deploy:
      replicas: 4
      resources:
        limits:
          cpus: "1"
          memory: 1G
          # pids: 100
        reservations:
          cpus: "0.1"
          memory: 20M
      restart_policy:
        condition: on-failure
    ports:
      - "8080:80"
networks:
  global:
    driver: overlay