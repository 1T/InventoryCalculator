tests = tests
package = inventorycalculator

test:
	py.test

coverage:
	py.test --cov $(package) --cov-report term-missing --cov-fail-under 80 $(tests)

.PHONY: htmlcov
htmlcov:
	py.test --cov $(package) --cov-report html $(tests)
	open htmlcov/index.html
