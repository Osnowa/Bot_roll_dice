run:
	watchmedo auto-restart \
	--directory=. \
	--pattern="*.py" \
	--recursive \
	-- python main.py 

# make run

test:
	pytest --cov

# make test