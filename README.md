# srst18
Our tinkerings

todo:
- [x] redo morph feature set
- [ ] Rerun Open NLP tests
- [ ] Run AMR tests
- [ ] clean up beam_search.py --- cancelled
- [ ] Change the LSTM to handle UNKs and remove the preprocessing step in beamsearch.py---cancelled

[Slack chat](https://srst18.slack.com/)

[Shared task data](http://taln.upf.edu/pages/msr2018-ws/Final4.zip)

[Currently trained LSTM LM models](https://dlk.sdf.org/models.tar.xz)

[Current menagerie of data](https://dlk.sdf.org/data.tar.xz)

#### LSTM Documentation ####
Originally from [my fork of some pytorch examples](https://github.com/DavidLKing/examples).
# Word-level language modeling RNN

This example trains a multi-layer RNN (Elman, GRU, or LSTM) on a language modeling task.
By default, the training script uses the Wikitext-2 dataset, provided.
The trained model can then be used by the generate script to generate new text.

```bash
python main.py --cuda --epochs 6        # Train a LSTM on Wikitext-2 with CUDA, reaching perplexity of 117.61
python main.py --cuda --epochs 6 --tied # Train a tied LSTM on Wikitext-2 with CUDA, reaching perplexity of 110.44
python main.py --cuda --tied            # Train a tied LSTM on Wikitext-2 with CUDA for 40 epochs, reaching perplexity of 87.17
python generate.py                      # Generate samples from the trained LSTM model.
```

The model uses the `nn.RNN` module (and its sister modules `nn.GRU` and `nn.LSTM`)
which will automatically use the cuDNN backend if run on CUDA with cuDNN installed.

During training, if a keyboard interrupt (Ctrl-C) is received,
training is stopped and the current model is evaluated against the test dataset.

The `main.py` script accepts the following arguments:

```bash
optional arguments:
  -h, --help         show this help message and exit
  --data DATA        location of the data corpus
  --model MODEL      type of recurrent net (RNN_TANH, RNN_RELU, LSTM, GRU)
  --emsize EMSIZE    size of word embeddings
  --nhid NHID        number of hidden units per layer
  --nlayers NLAYERS  number of layers
  --lr LR            initial learning rate
  --clip CLIP        gradient clipping
  --epochs EPOCHS    upper epoch limit
  --batch-size N     batch size
  --bptt BPTT        sequence length
  --dropout DROPOUT  dropout applied to layers (0 = no dropout)
  --decay DECAY      learning rate decay per epoch
  --tied             tie the word embedding and softmax weights
  --seed SEED        random seed
  --cuda             use CUDA
  --log-interval N   report interval
  --save SAVE        path to save the final model
  --train 0/1        train the model (0 = eval, 1 = train)
  --load LOAD        load a previously trained model
  --rank RANK        output scores for every line in the test file (results.tsv)
```

With these arguments, a variety of models can be tested.
As an example, the following arguments produce slower but better models:

```bash
python main.py --cuda --emsize 650 --nhid 650 --dropout 0.5 --epochs 40 --train 1           # Test perplexity of 80.97
python main.py --cuda --emsize 650 --nhid 650 --dropout 0.5 --epochs 40 --tied --train 1    # Test perplexity of 75.96
python main.py --cuda --emsize 1500 --nhid 1500 --dropout 0.65 --epochs 40 --train 1        # Test perplexity of 77.42
python main.py --cuda --emsize 1500 --nhid 1500 --dropout 0.65 --epochs 40 --tied --train 1 # Test perplexity of 72.30
```

Perplexities on PTB are equal or better than
[Recurrent Neural Network Regularization (Zaremba et al. 2014)](https://arxiv.org/pdf/1409.2329.pdf)
and are similar to [Using the Output Embedding to Improve Language Models (Press & Wolf 2016](https://arxiv.org/abs/1608.05859) and [Tying Word Vectors and Word Classifiers: A Loss Framework for Language Modeling (Inan et al. 2016)](https://arxiv.org/pdf/1611.01462.pdf), though both of these papers have improved perplexities by using a form of recurrent dropout [(variational dropout)](http://papers.nips.cc/paper/6241-a-theoretically-grounded-application-of-dropout-in-recurrent-neural-networks).
