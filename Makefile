docker-build:
	@echo "Building the Docker image..."
	@docker build -t scrapping-viper .
docker-up:
	@echo "Starting the Docker container..."
	@docker run -d --name scrapping-viper-container \
	-e VIPER_USER=antofa4 \
	-e VIPER_PASSWORD=cuartacba22 \
	-e DB_URL="mysql+mysqlconnector://root:7147@host.docker.internal:3306/bomberos" \
	-e EMAIL=botbombaprat@gmail.com \
	-e EMAIL_PASSWORD="okdryymxfcyhcziz" \
	-e EMAIL_TO=teniente2@bombaprat.cl \
	scrapping-viper
docker-run:
	@echo "Running the scrapping script inside the Docker container..."
	@docker run -d --name scrapping-viper-runner \