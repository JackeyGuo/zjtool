# prepare envirment

```bash
docker run -itd --name fastdfs --network=host -v /hd10t/fastdfs_data:/data --network=host -e GO_FASTDFS_DIR=/data sjqzhang/go-fastdfs
# you can modify /hd10t/fastdfs_data/confg file and restart container.
```

# usage:

```bash
zjtool fastdfs upload -f abc.txt -s nvaidia -t v1
zjtool fastdfs download --md5 [md5]
```