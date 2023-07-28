# Whisper with Stable Timestamps

This is a wrapper of [stable-ts](https://github.com/jianfch/stable-ts) for deployment on [Replicate](https://replicate.com/).

## Deploying to Replicate

The most up-to-date documentation is here: https://replicate.com/docs/guides/push-a-model

1) Fire up the cheapest GPU machine on [lambdalabs](https://cloud.lambdalabs.com/instances).

2) SSH into the instance

3) Install cog:

```shell
# this version fixes https://github.com/replicate/cog/issues/1162#issuecomment-1622248885
sudo curl -o /usr/local/bin/cog -L https://github.com/replicate/cog/releases/download/v0.8.0-beta11/cog_`uname -s`_`uname -m`
sudo chmod +x /usr/local/bin/cog
```

4) Clone this repo and cd into it

5) Download the models to the Docker container:
```shell
sudo cog run script/download_models.py
```

6) Test by building the container and running prediction on the included sample file:
```shell
sudo cog predict -i audio_path=@testing-1-2-3.mp3 -i language=en
```

You may also want to try with your own uploaded audio. Send it to the server with `scp`:

    scp -i <your_key_rsa> <your_audio>.mp3 ubuntu@<machine IP>:/home/ubuntu/whisper-ts-cog/<your_audio>.mp3

7) Push to replicate:
```shell
sudo cog login
sudo cog push
```

If you get `name unknown: The model https://replicate.com/wordscenes/whisper-stable-ts does not exist`, then you forgot to use `sudo` in `cog push`!

If you get `You are not logged in to Replicate. Run 'cog login' and try again.`, then you forgot to use `sudo` in `cog login`!

8) Go to https://replicate.com/wordscenes/whisper-stable-ts/versions, grab the latest version ID, and replace it in any code that calls this API (unfortunately you can't just call the latest version :( ).

