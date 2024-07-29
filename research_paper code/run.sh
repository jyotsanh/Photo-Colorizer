#!/usr/bin/env bash
set -e

venv=${1}
post_process=${2}
saturation_value=${3}
render_factor=${4}


if [ ! -d "$venv" ]; then
  echo "Virtualenv not found" > demo_failure.txt
  exit 0
else
  source $venv/bin/activate
fi

echo main.py --post_process=$post_process --saturation_value=$saturation_value --render_factor=$render_factor --img=input_0.png --pretrained=$bin/training/model.pth --normalize=True

main.py --post_process=$post_process --saturation_value=$saturation_value --render_factor=$render_factor --img=input_0.png --pretrained=$bin/training/model.pth --normalize=True