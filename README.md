#NLP tasks
##Task1:  Word2Vec
### About
This implementation basicly refereced tensorflow's word2vec implementation of the [Skip-Gram](https://www.tensorflow.org/tutorials/word2vec) model.And implement a Contninus Bag of Words(CBOW) model.
According to the main difference of above two model, I just change the **generate_batch(...)** function int the **word2vec_fns.py** 

### Usage
1.Get embeddings,If this completes without error, you should see a file called CBOW_Embeddings.npy in the current directory, which you will need to submit along with your version of word2vec_fns.py:
```
> python3 word2vec_cbow.py
```
2.Plot embeddings:
```
python3 plot_embeddings.py
```
And you should see this:



