UV = uv
CACHE = $(shell find . -name ".mypy_cache" -o -name "__pycache__")
DIR = src

C_RESET		= \033[0m
C_GREEN		= \033[032m
C_BLUE		= \033[034m
C_MAGENTA	= \033[035m

install:
	@echo "$(C_BLUE)Installing depedencies...$(C_RESET)"
	@$(UV) sync
	@echo "$(C_GREEN)Depedencies Installed$(C_RESET)"

run:
	@echo "$(C_BLUE)Running the program...$(C_RESET)"
	@$(UV) run python3 -m $(DIR)

debug:
	@echo "$(C_BLUE)Debugging the program...$(C_RESET)"
	@$(UV) run python3 -m pdb -m $(DIR)

clean:
	@echo "$(C_BLUE)Removing artifact...$(C_RESET)"
	@rm -rf $(CACHE)
	@echo "$(C_GREEN)Artifact Removed$(C_RESET)"

lint:
	@echo "$(C_BLUE)Checking flake8...$(C_RESET)"
	@$(UV) run flake8 $(DIR)
	@echo "$(C_MAGENTA)flake8 is good$(C_RESET)"
	@echo "$(C_BLUE)Checking mypy...$(C_RESET)"
	@$(UV) run mypy $(DIR) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
	@echo "$(C_MAGENTA)mypy is good$(C_RESET)"
	@echo "$(C_GREEN)Lint check successfull$(C_RESET)"

lint-strict:
	@echo "$(C_BLUE)Checking flake8...$(C_RESET)"
	@$(UV) run flake8 $(DIR)
	@echo "$(C_MAGENTA)flake8 is good$(C_RESET)"
	@echo "$(C_BLUE)Checking mypy --strict...$(C_RESET)"
	@$(UV) run mypy $(DIR) --strict
	@echo "$(C_MAGENTA)mypy is good$(C_RESET)"
	@echo "$(C_GREEN)Lint check successfull$(C_RESET)"


