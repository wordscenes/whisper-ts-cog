https://replicate.com/docs/guides/push-a-model

Install cog:

# this version fixes https://github.com/replicate/cog/issues/1162#issuecomment-1622248885
sudo curl -o /usr/local/bin/cog -L https://github.com/replicate/cog/releases/download/v0.8.0-beta11/cog_`uname -s`_`uname -m`
sudo chmod +x /usr/local/bin/cog

Build container and run prediction:

sudo cog predict -i audio_path=@testing-1-2-3.mp3 -i language=en

Currently fails:

```
File "/root/.pyenv/versions/3.11.4/lib/python3.11/site-packages/torch/nn/modules/conv.py", line 309, in _conv_forward
return F.conv1d(input, weight, bias, self.stride,
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
RuntimeError: GET was unable to find an engine to execute this computation
panic: runtime error: invalid memory address or nil pointer dereference
[signal SIGSEGV: segmentation violation code=0x1 addr=0x0 pc=0x8956f1]
```

TODO:
* Fix CUDA issue so that running works
* Pre-download model into image so that running is quick.
* Why sudo everywhere?
