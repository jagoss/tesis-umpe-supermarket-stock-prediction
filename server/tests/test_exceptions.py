"""Tests for domain exception hierarchy."""
from __future__ import annotations

from server.domain import DomainError, PredictionError, ValidationError


class TestDomainError:
    def test_message(self) -> None:
        err = DomainError("something went wrong")
        assert str(err) == "something went wrong"

    def test_cause(self) -> None:
        original = RuntimeError("root cause")
        err = DomainError("wrapper", cause=original)
        assert err.__cause__ is original

    def test_cause_defaults_to_none(self) -> None:
        err = DomainError("no cause")
        assert err.__cause__ is None

    def test_is_exception(self) -> None:
        assert issubclass(DomainError, Exception)


class TestValidationError:
    def test_inherits_domain_error(self) -> None:
        assert issubclass(ValidationError, DomainError)

    def test_message_and_cause(self) -> None:
        err = ValidationError("bad input", cause=ValueError("details"))
        assert str(err) == "bad input"
        assert isinstance(err.__cause__, ValueError)

    def test_catchable_as_domain_error(self) -> None:
        try:
            raise ValidationError("test")
        except DomainError as e:
            assert str(e) == "test"


class TestPredictionError:
    def test_inherits_domain_error(self) -> None:
        assert issubclass(PredictionError, DomainError)

    def test_message(self) -> None:
        err = PredictionError("model failed")
        assert str(err) == "model failed"

    def test_catchable_as_domain_error(self) -> None:
        try:
            raise PredictionError("fail")
        except DomainError as e:
            assert str(e) == "fail"
