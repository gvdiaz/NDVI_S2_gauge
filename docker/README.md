# ----------------------------
# -- DOCKER CONAE BALL V1.0 --
# ----------------------------

Title: SSM GoldMine California for VENG
Product Code Dev: Danilo Dadamia
Version: 1.0
Description: Product for California gold mine ordered by VENG, November 2022. SAOCOM image processing.

## Container Description: 
Ubuntu 20.04 + MatLab Runtime 2018b + SNAP 9.0 + Python 3.9 

## Use
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
```bash
$ docker build -t ssm_mine_veng -f docker/Dockerfile .
```


## 2. Run 

docker run -d --rm --name ssm_mine_gold_veng_california --net host -it \
    -v $(pwd):/src \
    -v '/mnt/c/Users/DiazGustavoV/.snap/auxdata/dem/SRTM 1Sec HGT/':'/root/.snap/auxdata/dem/SRTM 1Sec HGT' \
    --workdir /src \
    ssm_mine_veng



## Enter to container
docker exec -it ssm_mine_gold_veng_california bash



## Exec matlab
docker exec -it -w /src ssm_mine_gold_veng_california ./run_A_SAOCOM_HUMEDAD_QUAD.sh /opt/mcr/v95

