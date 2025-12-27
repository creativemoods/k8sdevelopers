FROM golang:1.16 AS builder
WORKDIR /go/src/training/helloworld/
RUN go mod init
COPY app.go ./
RUN CGO_ENABLED=0 go build -a -installsuffix cgo -o app .

FROM alpine:latest  
RUN adduser -S -H myuser -h /
USER myuser
WORKDIR /
COPY --from=builder --chown=myuser:nogroup /go/src/training/helloworld/app ./
CMD ["./app"]
