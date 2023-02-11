# write-with-gpt2
A simple text editor with suggestions generated from a Cantonese GPT2 model

The model can be found [here](https://huggingface.co/jed351/gpt2_base_zh-hk-shikoto)

It is a GPT2 model finetuned on a dataset of some Cantonese online novels. The model is trained on an Nvidia Quadro RTX6000 for 60hours. 

The text editor was based on [this](https://www.thepythoncode.com/article/text-editor-using-tkinter-python).

**Note: The model is not perfect. It is only trained on 700MB of data. The training data might includes inappropriate language.**

## Installation
1. Install huggingface transformers according to the instructions [here](https://huggingface.co/docs/transformers/installation)

Note: you have to install [pytorch](https://pytorch.org/get-started/locally/) separately

2. Download the model from [here](https://huggingface.co/jed351/gpt2_base_zh-hk-shikoto/blob/main/pytorch_model.bin) and put it in the directory `write-with-gpt2/gpt2-base`


## Functionalities
1. Change the font size
2. Undo the generated text with control z (I still haven't figured out how to properly implement an undo function, but it works for undoing the generated text)