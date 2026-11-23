# Project

## Image to video (free)

`i2v.py` sends an image and a prompt to a free Hugging Face Space running Wan 2.2 (`zerogpu-aoti/wan2-2-fp8da-aoti-faster`) and saves the video.

```sh
pip install gradio_client
export HF_TOKEN=hf_...   # free, read-only: https://huggingface.co/settings/tokens
python3 i2v.py photo.jpg "slow dolly-in, leaves drifting in the wind" -o clip.mp4 --seconds 3.5
```

Free Spaces come with a small daily GPU quota. Without `HF_TOKEN` you get almost none. With a free account token you get a few clips a day. If the Space is busy, your job waits in its queue. If the Space goes away, pick another Wan or LTX image-to-video Space and update `SPACE` and the `predict()` call in `i2v.py`.

Tests: `python3 -m unittest test_i2v`
