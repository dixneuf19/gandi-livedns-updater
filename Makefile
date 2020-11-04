.PHONY: build push release deploy

DOCKER_REPOSITERY="dixneuf19"
IMAGE_NAME="gandi-livedns-updater"
IMAGE_TAG="v1"
DOCKER_IMAGE_PATH="$(DOCKER_REPOSITERY)/$(IMAGE_NAME):$(IMAGE_TAG)"
APP_NAME="gandi-livedns-updater"

build:
	docker buildx build -t $(DOCKER_IMAGE_PATH) --platform linux/arm64 .

push:
	docker buildx build -t $(DOCKER_IMAGE_PATH) --platform linux/arm64 --push .

release: build push

deploy:
	kubectl apply -f gandi-livedns-updater.yaml

delete:
	kubectl delete -f gandi-livedns-updater.yaml

secret:
	kubectl create secret generic ${APP_NAME} --from-env-file=.env
