FROM pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime


RUN pip install stable-ts
RUN pip install demucs
RUN pip install flask

ADD testing-1-2-3.mp3 /root/testing-1-2-3.mp3

# Run this to pre-download the models...no easy way to explicitly do this yet!
RUN stable-ts \
  /root/testing-1-2-3.mp3 \
  --model=large-v2 \
  --language=ja \
  --demucs=True \
  --regroup=True \
  # --vad=True \  not working for the mp3 file provided
  --beam_size 5 --temperature_increment_on_fallback 0.2 --best_of 5 \
  -o test.json

ADD whisperHttpServer.py /root/whisperHttpServer.py



ENTRYPOINT ["stable-ts"]

# ENTRYPOINT ["python"]
# CMD ["/root/whisperHttpServer.py"]