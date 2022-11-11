import flet as ft

md = '''# Model selection and validation

In a previous lecture, we discussed the ridge regression estimate

$$
\hat{\boldsymbol{\theta}}_{\text {ridge }}=\arg \min _{\boldsymbol{\theta}}\|\mathbf{y}-\mathbf{X} \boldsymbol{\theta}\|_2^2+\lambda\|\boldsymbol{\theta}\|_2^2,
$$

and found that the regularization parameter $\lambda$ enables trading off the bias and variance of the estimator. Note that the estimate $\hat{\boldsymbol{\theta}}_{\text {ridge }}$ is parameterized by $\lambda$, and when computing $\hat{\boldsymbol{\theta}}_{\text {ridge }}$, we do not optimize over $\lambda$. For this reason, it is called a **hyperparamete**r. Almost all machine learning method have hyperparameters. Besides obvious hyperparameters like the regularization parameter in ridge regression, the following can also be regarded as hyperparameters that we wish to choose well:

- Which model to choose, for example a linear model.
- For a fixed model, their parameters. For example, the number of layers of a deep neural network, its activations functions etc.
- Which features to include or exclude.

The performance of our method often critically depends on the choice of the hyperparameters. This raises the question: <u>How can we choose the hyperparameters in a principled manner, and assess the performance of the resulting model?</u>

## The statistical learning setup

In order to fit a model, we typically minimize a quantity that captures how well the model predicts past data, but we actually care about how well the model predicts unseen data. <u>In order to asses how well a model predicts unseen data it is useful to consider the statistical learning setup.</u>

Suppose that examples $(\mathbf{x}, y)$ are drawn i.i.d. from some (unknown) distribution. For example, this distribution could be determined by $y=h^*(\mathbf{x})+z$, where $h^*$ is a fixed regression function (say $h^*(\mathbf{x})=\left\langle\mathbf{x}, \boldsymbol{\theta}^*\right\rangle$, and $\mathbf{x}$ and $z$ are drawn i.i.d. from Gaussian distributions. Given a function $h$, we measure the error between the observation $y$ and the estimate $\hat{y}=h(\mathbf{x})$ with a loss function

$$
\text { loss: } \mathbb{R} \times \mathbb{R} \rightarrow \mathbb{R}
$$

For example, $\operatorname{loss}(z, y)=(z-y)^2$ is the quadratic loss popular in regression. Consider a class of functions $\mathcal{H}$. The (true or population) risk of a function $h \in \mathcal{H}$ in this class is defined as

$$
R(h)=\mathbb{E}[\operatorname{loss}(h(\mathbf{x}), y)],
$$

where the expectation is over the distribution of the data. Ideally, we would like to find the function in our hypothesis class that minimizes the risk:

$$
h^*=\arg \min _{h \in \mathcal{H}} R(h) .
$$

Unfortunately, it is impossible to compute the expectation because we don't know the joint distribution of $(\mathbf{x}, y)$.

## Training, validation and test errors

We do, however, have access to a set of examples $\mathcal{D}=\left\{\left(\mathbf{x}_1, y_1\right), \ldots,\left(\mathbf{x}_n, y_n\right)\right\}$.

**<u>Training and testing:</u>** First, suppose our goal is to train a model that does not have hyperparameters and then predict how well it performs on new examples. Towards this goal, we first split our dataset into two non-overlapping sets $\mathcal{D}_{\text {train }}$ and $\mathcal{D}_{\text {test }}$ called the training set and the test set.
The estimate
![](https://i.imgur.com/ly3SU9c.png)

is called the training error. Here, $\left|\mathcal{D}_{\text {train }}\right|$ stands for the cardinality of the set $\left|\mathcal{D}_{\text {train }}\right|$, i.e., the number of examples in the training set.

Almost exclusively, we fit a model by minimizing the training error, or a regularized version thereof. For example, linear regression fits a model by minimizing the training error and ridge regression fits a model by minimizing the training error regularized with the penalty $\lambda\|\boldsymbol{\theta}\|_2^2$. Note that the training error $\hat{R}\left(h, \mathcal{D}_{\text {train }}\right)$ can be viewed as an estimate of the true risk computed based on the training set.

Given a model trained on the training set, we cannot use the training error to estimate the population risk $R(\hat{h})$ of a function $\hat{h}$ trained on the training set. The reason is that $\hat{h}$ is a function of $\mathcal{D}_{\text {train }}$. We can, however, use the test error to estimate the expected risk:

$$
\hat{R}\left(h, \mathcal{D}_{\text {test }}\right)=\frac{1}{\left|\mathcal{D}_{\text {test }}\right|} \sum_{(\mathbf{x}, y) \in \mathcal{D}_{\text {test }}} \operatorname{loss}(h(\mathbf{x}), y)
$$

The test error $\hat{R}\left(\hat{h}, \mathcal{D}_{\text {test }}\right)$ is an unbiased estimate of the population risk, because $\hat{h}$ is independent of the test set.

The question that remains is: How large does the test set need to be? It needs to be sufficiently large so that the test error is a good estimate of the population risk. More formally, under mild assumptions on the risk and estimator (specifically, that it is bounded), we have by Hoeffding's inequality for a set $\mathcal{D}$ with $n$ i.i.d. examples for any $\delta>0$ that

$$
\mathrm{P}\left[|\hat{R}(h, \mathcal{D})-R(h)| \leq O\left(\sqrt{\frac{\log (1 / \delta)}{n}}\right)\right] \geq 1-\delta .
$$

**In words, the larger our test set, the better our estimate of the true risk.** 
**Moreover, doubling the size of the test set improves the estimate by a factor of $\sqrt{1 / 2}$.**

The parameter $\delta$ is the probability that the estimate is far from its mean, think about this as a very small number, say $10^{-8}$.

**<u>Training, model selection, and testing:</u>** Next, suppose we want to train a method with a number of hyperparameter configurations $i=1, \ldots, K$. For example, we wish to train a ridge regression estimate for $K$ different choices of the hyperparameter $\lambda$, determine which one performs the best, and then determine the performance we expect (i.e., estimate the risk).

Towards this goal, we split the set of examples into three disjoint sets: a training set $\mathcal{D}_{\text {train }}$, a validation set $\mathcal{D}_{\text {val }}$, and a test set $\mathcal{D}_{\text {test }}$. We then perform the following procedure:

- For all choices of hyperparameter configurations $i=1, \ldots, K$ :
	- Train model $\hat{\boldsymbol{\theta}}_i$ on $\mathcal{D}_{\text {train }}$
	- Compute validation error for model $\hat{\boldsymbol{\theta}}_i$ on $\mathcal{D}_{\text {val }}$
- Select model $\hat{\boldsymbol{\theta}}_i$ with the smallest validation error $\hat{R}\left(\hat{\boldsymbol{\theta}}_i, \mathcal{D}_{\text {val }}\right)$ as the estimate for the best performing model
- Report the final performance as $\hat{R}\left(\mathcal{D}_{\text {test }}, \hat{\boldsymbol{\theta}}_i\right)$

With this procedure, we do have to be mindful of the fact that we are re-using the validation set many times. This has to be taken into account when choosing the size of the validation set. This procedure can go wrong: 

- If the validation set is too small, then just by chance a hyperparameter configuration works well. 
- If the number of hyperparameter configurations is extremely large, specifically exponential in the size of the validation set, this will happen and would be an issue.

## k-fold cross validation
Cross validation is a method for estimating the risk of a model trained on a training set based on a finite and potentially small pool of examples $\mathcal{D}$. **The idea is to repeatedly split the set $\mathcal{D}$ into test and training sets.** The most popular variant of this idea is $k$-fold cross validation, which consists of the following steps:

- Shuffle the data and partition it into $k$ equally sized or near equally sized subsets $\mathcal{D}_1, \ldots, \mathcal{D}_k$. If the data is drawn i.i.d., shuffling would not be necessary, but remember that assuming the data is drawn i.i.d. is just a modeling assumption not necessarily true in practice.
- For each subset $i$, train the model on the union of all subsets but $\mathcal{D}_i$, i.e., on $\mathcal{D} \backslash \mathcal{D}_i$, and evaluate the model using block $i$ by computing the validation error. This gives the $i$-th estimate of the risk. **每次选择$D_{i}$作为验证集**
- Obtain a final estimate of the risk as the average of the so-obtained $k$ estimates.

Using this methodology, the model is always evaluated on a different set of points than it is trained out. So how do we choose $k$ ? Larger values of $k$ provide a better estimate of the true error that we expect when training on a training set with $n$ points, but also requires more computation. To see this suppose we set $k=n$, then we train on $n-1$ points, but also need to fit our model $n$ many times, which can be very costly. How to choose $k$ in practice depends on how one want to balance this tradeoff; **a common value for $k$ in practice is 10** .

Let's look at an example following Hastie et al. [HTF09], section 7.10.2. Consider a classification or regression problem with a large number of features. Suppose we perform the following steps:

- Select a number of relevant features by correlating them with the observations, and select the features that are highly correlated.
- Use only this subset of features, and train a classification or regression model, for example ridge regression.
- Use cross-validation to estimate the unknown hyperparameters (e.g., the regularization parameter of ridge regression) and to estimate the prediction error of the final model.

*Is this a correct application of cross-validation, and if not, what can go wrong?？*

Suppose there are $n=50$ examples and originally there are 5000 features that are independent of the labels. Assume both class labels are equally likely, then the true error rate of any classifier is at least $50 \%$. Hastie et al. [HTF09] carried out the above steps and the average cross-validation error was 3\%, a significant underestimation of the error rate. What happened here is that just by chance, features are highly correlated with the data. The right way to apply cross validation in the example above is the following:

- Divide the examples into $k$ equally sized sets at random.
- For each set $i$, using all examples but those in set $i$, i) find a set of good predictor that are strongly correlated with the labels, ii) use only this set of predictors to build a model, and iii) use the classifier to predict the class labels in fold $i$.
- Accumulate the error estimates from each fold to produce the cross-validation estimate of the prediction error.


## Bootstrap
Suppose we are interested in associating a confidence interval, standard error, or variance estimate with our learning algorithms. As a concrete example, suppose we are interested in estimating the variance of a learning algorithm $\hat{h}$ for a given example $\mathbf{x}$:

$$
\text{Var}[\hat{h}(\mathbf{x})]=\mathbb{E}_{\mathcal{D}}\left[\left(\hat{h}_{\mathcal{D}}-\mathbb{E}\left[\hat{h}_{\mathcal{D}}(\mathbf{x})\right]\right)^2\right] .
$$

Suppose, as before that the examples $(y, \mathbf{x})$ in $\mathcal{D}$ are drawn from some joint distribution. In order to estimate this quantity, we can sample datasets $\mathcal{D}_1, \ldots, \mathcal{D}_b$, each containing $n$ examples drawn uniformly at random from the joint distribution, and apply the learning algorithm to those datasets. That yields hypothesis $\hat{h}_1, \ldots, \hat{h}_b$. Based on those, we can estimate the mean at a point $\mathbf{x}$ as
![](https://i.imgur.com/5zdnw0O.png)

and the variance as
$$
\text{Var}[\hat{h}(\mathbf{x})]=\frac{1}{b} \sum_{i=1}^b\left(h_{\mathcal{D}_i}(\mathbf{x})-\hat{\mu}(\mathbf{x})\right)^2 .
$$
While statistically sound, this method for estimating the variance of the estimator is not practically, we would need to sample a large number of examples.

The bootstrap, proposed by Efron in 1979 offers a more practical approach. The basic idea of bootstrapping is that in absence of any other information about the unknown distribution, all the information about the distribution we have is contained in the observed sample $\mathcal{D}$. Hence resampling from $\mathcal{D}$ is a good guide to see what can be expected if we would resample from the original distribution.

For the concrete example above, we would sample a dataset $\mathcal{D}$ from the original, joint distribution, and then resample $b$ many datasets $\mathcal{D}_1, \ldots, \mathcal{D}_b$, all containing $n$ samples, by drawing $n$ examples each uniformly at random with replacement from $\mathcal{D}$. Then, we would estimate the variance as above.

> Efron 在 1979 年提出的 bootstrap 提供了一种更实用的方法。 自举的基本思想是，在没有关于未知分布的任何其他信息的情况下，我们所拥有的关于分布的所有信息都包含在观察到的样本 $\mathcal{D}$ 中。 因此，从 $\mathcal{D}$ 重新采样是一个很好的指南，可以很好地了解如果我们从原始分布重新采样会发生什么。
对于上面的具体示例，我们将从原始联合分布中采样数据集 $\mathcal{D}$，然后通过从 $\mathcal{D}$ 中随机均匀抽取 $n$ 个样本(若采集到相同的样本则替换)（重复$b$次）
重新采样 $b$ 多个数据集 $\mathcal{D}_1,\ldots,\mathcal{D}_b$，每个包含 $n$ 个样本，。 然后，我们将如上所述估计方差。



Reading: Chapter 7 in [HTF09].

# References
[HTF09] T. J. Hastie, R. J. Tibshirani, and J. J. H. Friedman. The elements of statistical learning. Springer, 2009.'''

def home(page: ft.Page):
    page.add(ft.Markdown(md))
    page.scroll = "always"

if __name__ == '__main__':
    ft.app(target=home)