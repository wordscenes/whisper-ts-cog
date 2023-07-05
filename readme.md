https://replicate.com/docs/guides/push-a-model

Install cog:

# this version fixes https://github.com/replicate/cog/issues/1162#issuecomment-1622248885
sudo curl -o /usr/local/bin/cog -L https://github.com/replicate/cog/releases/download/v0.8.0-beta11/cog_`uname -s`_`uname -m`
sudo chmod +x /usr/local/bin/cog

Build container and run prediction:

sudo cog predict -i audio_path=@testing-1-2-3.mp3 -i language=en

TODO:
* Fix CUDA issue so that running works
* Pre-download model into image so that running is quick.
* Why sudo everywhere?
