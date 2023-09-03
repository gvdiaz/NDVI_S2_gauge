# ------------------------------
# -- DOCKER NEGRETE BALL V0.1 --
# ------------------------------

Title: Procesador de imagenes Sentinel-2
Product Code Dev: Gustavo Vladimir Diaz
Version: 0.1
Description: Seleccionador + "Bajador" + Procesador de imagenes Sentinel-2

## Container Description: 
Ubuntu 22.04LTS + SNAP 9.0 + Python 3.10 

## Use
(por ahora sigo utilizando el original de donde saqué información)
The SAOCOM image is placed in the INPUT folder for processing. 

Example:    INPUT
            │
            └── SAOCOM
                │
                └──'EOL1ASAR...'
                    │
                    ├─ SA1_OP....xemt
                    └─ SA1_OP....zip


In OUTPUT it is separated by regions:

Example:    OUTPUT
            │
            ├─LCM
            │   └─SAOCOM...zip
            └─CHM
                └─SAOCOM...zip


## 1. Install


- **CPU:**
```bash con usuario que tenga permisos para ejecutar comandos de docker
$ docker build -t gis_gvd .
```


## 2. Run 
(Comandos aún del docker original que debo cambiar en este proyecto)
docker run -d --rm --name ssm_mine_gold_veng_california --net host -it \
    -v $(pwd):/src \
    -v '/mnt/c/Users/DiazGustavoV/.snap/auxdata/dem/SRTM 1Sec HGT/':'/root/.snap/auxdata/dem/SRTM 1Sec HGT' \
    --workdir /src \
    ssm_mine_veng



## Enter to container
(Comandos aún del docker original que debo cambiar en este proyecto)
docker exec -it ssm_mine_gold_veng_california bash



## Exec matlab
docker exec -it -w /src ssm_mine_gold_veng_california ./run_A_SAOCOM_HUMEDAD_QUAD.sh /opt/mcr/v95

