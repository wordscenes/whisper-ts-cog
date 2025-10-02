# Whisper with Stable Timestamps

This is a wrapper of [stable-ts](https://github.com/jianfch/stable-ts) for deployment on [Replicate](https://replicate.com).

## Deploying to Replicate

The most up-to-date documentation is here: https://replicate.com/docs/guides/push-a-model

1) Fire up the cheapest GPU machine on [Lambda](https://cloud.lambda.ai/instances). You should also attach a filesystem.

Note: The Lambda ARM64 instances have issues building the image as of October 2025. Use x86_64.

2) SSH into the instance, or use LambdaLab's Cloud IDE and open a terminal.

3) Install cog:

```shell
sudo curl -o /usr/local/bin/cog -L https://github.com/replicate/cog/releases/download/v0.8.6/cog_`uname -s`_`uname -m`
sudo chmod +x /usr/local/bin/cog
```

4) Clone this repo and cd into it

```shell
cd [filesystem name] # if you attached a filesystem
git clone https://github.com/wordscenes/whisper-ts-cog.git
cd whisper-ts-cog
```

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

You should also double-check the printed module versions to make sure they're what you meant to use.

You should also check with a more difficult file; we do not include it here for copyright reasons, but internally we test with the first 5 minutes of Shrek in Japanese. Send the file to the server with `scp` (taking care not to put it in the `whisper-ts-cog` directory, as that will will include it in the Docker image if you build again):

    scp -i <your_key_rsa> <your_audio>.mp3 ubuntu@<machine IP>:/home/ubuntu/<your_audio>.mp3

Transcribing Shrek takes 2m6s, with 36s used for startup. Also note that the first word after the long song is given a timespan consisting of the previous 20s. TODO: Not sure what to do about that right now.

7) Push to replicate:
```shell
sudo cog login
sudo cog push
```

If you get `name unknown: The model https://replicate.com/wordscenes/whisper-stable-ts does not exist`, then you forgot to use `sudo` in `cog push`!

If you get `You are not logged in to Replicate. Run 'cog login' and try again.`, then you forgot to use `sudo` in `cog login`!

8) Go to https://replicate.com/wordscenes/whisper-stable-ts/versions, grab the latest version ID, and replace it in any code that calls this API (unfortunately you can't just call the latest version :( ).

## Known Issues

You might deploy your image only to find that it fails to run with a message stating that `libcuda.so` could not be found. I do not know what causes this. You can easily see that libcuda.so is present in the image by running:

```shell
sudo docker image ls
sudo docker run -it [image_id] bash -c "find / -type f -name libcuda.so"
```

naklecha on Replicate's Discord said that this is caused by LambdaLabs' machine having a memory issue, causing the file to be excluded from the image, which doesn't sound plausible to me. They say that the fix for them was to just delete and prune all of the images on the instance and build again. I tried this with no luck.

Removing `demucs=True` from the download_models.py script did not yield a working image, either.

I've opened an issue here: https://github.com/replicate/cog/issues/1448.

TODO: follow-up and deploy image when this issue is resolved.

## Rejected Experiments

* Whisper model "large-v3" does horribly on the Shrek test, replacing many phrases with "ご視聴ありがとうございました" (others have also reported "thank you for watching" hallucinations in English). See https://deepgram.com/learn/whisper-v3-results for some validating evidence that this model severely underperforms vs. "large-v2".
* [`faster-whisper`](https://github.com/SYSTRAN/faster-whisper) (version "0.10.0") degrades accuracy on the Shrek test, omitting one sentence at the end of the clip ("よし、もう満杯だ"), as well as reducing the expressiveness of the onomatopetic katakana expressions. It is faster, but we want accuracy.
