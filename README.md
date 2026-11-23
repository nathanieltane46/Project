# Project

## Image to video

`i2v.py` sends an image and a prompt to a Replicate model and saves the video. It uses only the Python standard library.

```sh
export REPLICATE_API_TOKEN=r8_...   # https://replicate.com/account/api-tokens
python3 i2v.py photo.jpg "slow dolly-in, leaves drifting in the wind" -o clip.mp4
```

The default model is `wan-video/wan-2.2-i2v-fast`. Use `--model owner/name` for another model. If that model names its image input something other than `image` (Kling uses `start_image`), add `--image-key start_image`. Each run is billed to your Replicate account.

Tests: `python3 -m unittest test_i2v`
