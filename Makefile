run:
	watchmedo auto-restart \
	--directory=. \
	--pattern="*.py" \
	--recursive \
	-- python main.py 

# make run

test:
	pytest

# make test