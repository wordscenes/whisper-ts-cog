# Whisper with Stable Timestamps

This is a wrapper of [stable-ts](https://github.com/jianfch/stable-ts) for deployment on [Replicate](https://replicate.com/).

## Deploying to Replicate

The most up-to-date documentation is here: https://replicate.com/docs/guides/push-a-model

1) Fire up the cheapest GPU machine on [lambdalabs](https://cloud.lambdalabs.com/instances). You can pick a cheap GPU machine if it's available. You should also attach a filesystem.

2) SSH into the instance

3) Install cog:

```shell
# this version fixes https://github.com/replicate/cog/issues/1162#issuecomment-1622248885
sudo curl -o /usr/local/bin/cog -L https://github.com/replicate/cog/releases/download/v0.8.0-beta11/cog_`uname -s`_`uname -m`
sudo chmod +x /usr/local/bin/cog
```

4) Clone this repo and cd into it

    git clone https://github.com/garfieldnate/whisper-ts-cog.git
    cd whisper-ts-cog

5) Download the models to the Docker container:
```shell
sudo cog run script/download_models.py
```

If you get `nvidia-container-cli: requirement error: unsatisfied condition: cuda>=11.8, please update your driver to a newer version, or use an earlier cuda container: unknown`, then you didn't attach a file system. (I guess it runs out of memory or something. It's a stupid error message 🤷.)

6) Test by building the container and running prediction on the included sample file:
```shell
sudo cog predict -i audio_path=@testing-1-2-3.mp3 -i language=en
```

Judging manually, the roughly expected timestamps are:

* testing: .55-.9
* one: .9-1.05
* two: 1.05-1.2
* three: 1.2-1.45

You may also want to try with your own uploaded audio. Send it to the server with `scp`:

    scp -i <your_key_rsa> <your_audio>.mp3 ubuntu@<machine IP>:/home/ubuntu/whisper-ts-cog/<your_audio>.mp3

Testing on our internal subtitle test file, prediction takes 2m6s, with 36s used for startup. Also note that the first word after the long song is given a timespan consisting of the previous 20s. Not sure what to do about that right now.

7) Push to replicate:
```shell
sudo cog login
sudo cog push
```

If you get `name unknown: The model https://replicate.com/wordscenes/whisper-stable-ts does not exist`, then you forgot to use `sudo` in `cog push`!

If you get `You are not logged in to Replicate. Run 'cog login' and try again.`, then you forgot to use `sudo` in `cog login`!

8) Go to https://replicate.com/wordscenes/whisper-stable-ts/versions, grab the latest version ID, and replace it in any code that calls this API (unfortunately you can't just call the latest version :( ).

