import random
from typing import List

import pytest

from nlptest.behavior import SequenceClassificationBehavior, SpanClassificationBehavior
from nlptest.types import BehaviorType, TaskType, Span


@pytest.fixture
def random_class():
    return random.randint(0, 10)


@pytest.fixture
def random_span():
    return Span(start=random.randint(0, 100), end=random.randint(100, 200), label=random.randint(0, 4))


@pytest.fixture
def text_sample():
    return "My name is Wolfgang and I live in Berlin"


class TestSequenceClassificationBehavior:
    """"""

    @staticmethod
    def predict_fn(list_text: List[str]):
        return [random.randint(0, 10)] * len(list_text)

    def test_run(self, text_sample, random_class):
        n_samples = 5
        behavior = SequenceClassificationBehavior(
            name="Test sequence classification",
            test_type=BehaviorType.invariance,
            task_type=TaskType.sequence_classification,
            samples=[text_sample] * n_samples,
            labels=[random_class] * n_samples,
            predict_fn=self.predict_fn
        )
        behavior.run()
        assert len(behavior.outputs) == n_samples
        assert all([b.y_pred is not None for b in behavior.outputs])

        with pytest.raises(ValueError):
            behavior.run()

    def test_save_and_load(self, text_sample, random_class):
        """"""
        n_samples = 5
        behavior = SequenceClassificationBehavior(
            name="Test sequence classification",
            test_type=BehaviorType.invariance,
            task_type=TaskType.sequence_classification,
            samples=[text_sample] * n_samples,
            labels=[random_class] * n_samples,
            predict_fn=self.predict_fn
        )
        behavior.run()
        behavior.to_file("tmp_data/")
        output0 = behavior.outputs

        new_behavior = SequenceClassificationBehavior.from_file(
            "tmp_data/Test_sequence_classification.pkl",
            self.predict_fn
        )
        new_behavior.run()
        output1 = behavior.outputs

        assert output0 == output1


class TestSpanClassificationBehavior:
    """"""

    @staticmethod
    def predict_fn(list_text: List[str]):
        return [[Span(start=0, end=10, label=1), Span(start=20, end=30, label=1)], ] * len(list_text)

    def test_run(self, text_sample, random_span):
        n_samples = 5
        behavior = SpanClassificationBehavior(
            name="Test span classification",
            test_type=BehaviorType.invariance,
            task_type=TaskType.span_classification,
            samples=[text_sample] * n_samples,
            labels=[[random_span, ] * 4] * n_samples,
            predict_fn=self.predict_fn
        )
        behavior.run()
        assert len(behavior.outputs) == n_samples
        assert all([b.y_pred is not None for b in behavior.outputs])

        with pytest.raises(ValueError):
            behavior.run()

    def test_save_and_load(self, text_sample, random_span):
        """"""
        n_samples = 5
        behavior = SpanClassificationBehavior(
            name="Test span classification",
            test_type=BehaviorType.invariance,
            task_type=TaskType.span_classification,
            samples=[text_sample] * n_samples,
            labels=[[random_span, ] * 4] * n_samples,
            predict_fn=self.predict_fn
        )
        behavior.run()
        behavior.to_file("tmp_data/")
        output0 = behavior.outputs

        new_behavior = SpanClassificationBehavior.from_file(
            "tmp_data/Test_span_classification.pkl",
            self.predict_fn
        )
        new_behavior.run()
        output1 = behavior.outputs

        assert output0 == output1
