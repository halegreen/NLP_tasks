
# NLP tasks
## Task1:  Word2Vec
### About
This implementation basicly refereced tensorflow's word2vec implementation of the [Skip-Gram](https://www.tensorflow.org/tutorials/word2vec) model.And implement a Contninus Bag of Words(CBOW) model.
According to the main difference of above two model, I just change the **generate_batch(...)** function in **word2vec_fns.py**. 

### Usage
1.Get embeddings,If this completes without error, you should see a file called CBOW_Embeddings.npy in the current directory:
```
> python3 word2vec_cbow.py
```
2.Plot embeddings:
```
> python3 plot_embeddings.py
```
And you should see this:
![](https://raw.githubusercontent.com/ZoeShaw101/NLP_tasks/master/Word2Vec_CBOW/docs/tsne_embeddings.png)


## Task2: Chinese Word Segmenter
### About
This is a chinese segmenter implemented using the Max-Probability model.

### Usage
1.Get word dict
```
python CreateDict.py
```
2. run segmenter
```
python Segmenter.py
```

### To-do
Using some more complex model, sach as RCF, LSTM...etc.







