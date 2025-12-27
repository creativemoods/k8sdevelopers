FROM golang:1.16 AS builder
WORKDIR /go/src/training/helloworld/
RUN go mod init
COPY app.go ./
RUN CGO_ENABLED=0 go build -a -installsuffix cgo -o app .

FROM alpine:latest  
WORKDIR /root/
COPY --from=builder /go/src/training/helloworld/app ./
CMD ["./app"]
