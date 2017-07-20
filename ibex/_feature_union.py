from __future__ import absolute_import

import pandas as pd
from sklearn import base
from sklearn import pipeline

from ._frame_mixin import FrameMixin


# Tmp Ami - take care of weights
# Tmp Ami - derive from appropriate sklearn mixins
class FeatureUnion(base.BaseEstimator, base.TransformerMixin, FrameMixin):
    """
    - Pandas version -
    Concatenates results of multiple transformer objects.
    This estimator applies a list of transformer objects in parallel to the
    input data, then concatenates the results. This is useful to combine
    several feature extraction mechanisms into a single transformer.

    Arguments:

    transformer_list: list of (string, transformer) tuples.
        List of transformer objects to be applied to the data.
        The first half of each tuple is the name of the transformer.

    n_jobs: int, optional.
        Number of jobs to run in parallel (default 1).

    transformer_weights: dict, optional.
        Multiplicative weights for features per transformer.
        Keys are transformer names, values the weights.
    """
    def __init__(self, transformer_list, n_jobs=1, transformer_weights=None):
        FrameMixin.__init__(self)

        self._feature_union = pipeline.FeatureUnion(
            transformer_list,
            n_jobs,
            transformer_weights)

    def fit_transform(self, x, y):
        """
        Same signature as any sklearn step.
        """
        xt = self._feature_union.fit_transform(
            x,
            y)

        return pd.DataFrame(xt, index=x.index)

    def fit(self, x, y):
        """
        Same signature as any sklearn step.
        """
        self._feature_union.fit(
            x,
            y)

        return self

    def transform(self, x):
        """
        Same signature as any sklearn step.
        """
        xt = self._feature_union.transform(x)

        return pd.DataFrame(xt, index=x.index)

    @property
    def transformer_list(self):
        return self._feature_union.transformer_list

    def __getitem__(self, ind):
        return self.transformer_list[ind][1]
