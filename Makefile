runner-image:
	docker pull ubuntu:jessie

plygrnd-image: web/Dockerfile
	docker build -t lhcb/playground web/

plygrnd: plygrnd-image
	docker run --net=host -d -e CONFIGPROXY_AUTH_TOKEN=devtoken \
		--name=plygrnd \
		-v /var/run/docker.sock:/docker.sock lhcb/playground python web/orchestrate.py

dev: plygrnd

#cleanup:
#	-docker stop `docker ps | awk //{print $1}`
#	-docker rm   `docker ps -aq`
